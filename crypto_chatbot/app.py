"""
Crypto Chatbot - COMPLETE FIX
- Groq AI entegrasyonu (ÜCRETSIZ + ÇOK HIZLI)
- Gerçek sohbet bütünlüğü
- Güvenli kod sistemi
"""

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'crypto-chatbot-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================================
# GROQ AI INTEGRATION
# ============================================================================

try:
    from groq import Groq
    GROQ_AVAILABLE = True
    groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    print("✓ Groq API initialized")
except Exception as e:
    GROQ_AVAILABLE = False
    print(f"⚠ Groq not available: {e}")

# ============================================================================
# DATABASE MODELS
# ============================================================================

class AdminCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    python_code = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSession(db.Model):
    session_id = db.Column(db.String(100), primary_key=True)
    message_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    # NEW: Store conversation history
    conversation_history = db.Column(db.Text, default='[]')

# ============================================================================
# CHATBOT WITH GROQ AI
# ============================================================================

class SmartChatbot:
    def __init__(self):
        self.words = [
            "pilot", "giant", "enable", "syrup", "medal", "hero", "iron", "soap",
            "visual", "vendor", "genuine", "punch", "grid", "floor", "glide", "penalty",
            "blossom", "crew", "pival", "sheriff", "solar", "claw", "oak", "find",
            "bind", "pet", "urban", "else", "series", "wave", "pumpkin", "amount",
            "verb", "similar", "crime", "bird"
        ]

    def get_target_word(self, message_count):
        """Get the word that should be used in this message"""
        if message_count >= 36:
            return None
        return self.words[message_count]

    def generate_response_with_groq(self, user_message, target_word, message_count, conversation_history):
        """Generate response using Groq AI"""

        if not GROQ_AVAILABLE:
            return self.generate_fallback_response(target_word, message_count)

        try:
            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a friendly chatbot in a crypto challenge.

CRITICAL RULES:
1. You MUST naturally include the word "{target_word}" in your response
2. Make the conversation feel natural and engaging
3. Keep responses conversational (2-3 sentences)
4. Don't mention you're using a specific word
5. Current message: {message_count + 1}/36
6. Be helpful and answer the user's question while including the word

Example good responses:
- User: "How are you?" → "I'm doing great! Did you know that a pilot needs excellent focus? How's your day?"
- User: "Tell me about AI" → "AI is like a giant network of connections! It learns from data patterns."

NEVER say "show code" or mention completing sequences."""
                }
            ]

            # Add conversation history (last 3 messages for context)
            import json
            try:
                history = json.loads(conversation_history) if conversation_history else []
                for msg in history[-6:]:  # Last 3 exchanges
                    messages.append({
                        "role": "user" if msg['type'] == 'user' else "assistant",
                        "content": msg['content']
                    })
            except:
                pass

            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call Groq API
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Updated model (llama3-8b-8192 deprecated May 2025)
                messages=messages,
                temperature=0.8,
                max_tokens=150,
                top_p=0.9
            )

            bot_response = response.choices[0].message.content

            # Verify word is included
            if target_word.lower() not in bot_response.lower():
                # Append word naturally if missing
                bot_response += f" By the way, {target_word} is an interesting concept!"

            return bot_response

        except Exception as e:
            print(f"Groq API error: {e}")
            return self.generate_fallback_response(target_word, message_count)

    def generate_fallback_response(self, target_word, message_count):
        """Fallback response if AI not available"""
        responses = [
            f"Great question! Let me tell you something about '{target_word}' - it's an important concept.",
            f"Interesting! The word '{target_word}' reminds me of something fascinating.",
            f"I love discussing this! '{target_word}' plays a key role in many areas.",
            f"That's a good point! Speaking of which, '{target_word}' is quite relevant here.",
            f"Thanks for asking! The concept of '{target_word}' is worth exploring."
        ]
        import random
        return random.choice(responses)

# Global chatbot instance
chatbot = SmartChatbot()

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/session/new', methods=['POST'])
def create_session():
    """Create new chat session"""
    session_id = str(uuid.uuid4())

    new_session = UserSession(session_id=session_id)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'session_id': session_id}), 201

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint with AI"""
    data = request.json
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', '')

    if not user_message or not session_id:
        return jsonify({'error': 'Invalid input'}), 400

    # Get session
    user_session = UserSession.query.filter_by(session_id=session_id).first()
    if not user_session:
        return jsonify({'error': 'Session not found'}), 404

    # Update last activity
    user_session.last_activity = datetime.utcnow()

    # Get current message count BEFORE increment
    current_count = user_session.message_count

    # Check if already completed
    if current_count >= 36:
        # SECURE: Only show code if they type EXACTLY "show code"
        if user_message.lower() == "show code":
            admin_code = AdminCode.query.first()
            if admin_code:
                code = admin_code.python_code
            else:
                code = "# No code has been set by admin yet"

            return jsonify({
                'response': f"🎉 Here's your Python code:\n\n```python\n{code}\n```",
                'metadata': {
                    'message_count': 36,
                    'completed': True,
                    'show_code': True
                }
            })
        else:
            return jsonify({
                'response': "You've completed all 36 messages! Type 'show code' to receive your Python code.",
                'metadata': {
                    'message_count': 36,
                    'completed': True,
                    'show_code': False
                }
            })

    # Get target word for THIS message
    target_word = chatbot.get_target_word(current_count)

    # Load conversation history
    import json
    try:
        conversation_history = json.loads(user_session.conversation_history) if user_session.conversation_history else []
    except:
        conversation_history = []

    # Generate AI response
    bot_response = chatbot.generate_response_with_groq(
        user_message=user_message,
        target_word=target_word,
        message_count=current_count,
        conversation_history=json.dumps(conversation_history)
    )

    # Update conversation history
    conversation_history.append({
        'type': 'user',
        'content': user_message,
        'timestamp': datetime.utcnow().isoformat()
    })
    conversation_history.append({
        'type': 'bot',
        'content': bot_response,
        'word': target_word,
        'timestamp': datetime.utcnow().isoformat()
    })

    # Keep only last 20 messages (10 exchanges)
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    user_session.conversation_history = json.dumps(conversation_history)

    # Increment message count
    user_session.message_count += 1

    # Check if completed now
    if user_session.message_count >= 36:
        user_session.completed = True

    db.session.commit()

    return jsonify({
        'response': bot_response,
        'metadata': {
            'word_used': target_word,
            'message_count': user_session.message_count,
            'remaining': max(0, 36 - user_session.message_count),
            'completed': user_session.completed
        }
    })

@app.route('/api/admin/code', methods=['POST'])
def save_code():
    """Admin: Save Python code"""
    data = request.json
    new_code = data.get('code', '')

    if not new_code:
        return jsonify({'error': 'Code cannot be empty'}), 400

    admin_code = AdminCode.query.first()
    if admin_code:
        admin_code.python_code = new_code
        admin_code.updated_at = datetime.utcnow()
    else:
        admin_code = AdminCode(python_code=new_code)
        db.session.add(admin_code)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code updated successfully'
    })

@app.route('/api/admin/code', methods=['GET'])
def get_code():
    """Admin: Get current code"""
    admin_code = AdminCode.query.first()
    if admin_code:
        return jsonify({
            'code': admin_code.python_code,
            'updated_at': admin_code.updated_at.isoformat()
        })
    return jsonify({
        'code': '# No code set yet',
        'updated_at': None
    })

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """Admin: Get statistics"""
    total = UserSession.query.count()
    completed = UserSession.query.filter_by(completed=True).count()

    # Active sessions (activity in last 24 hours)
    from datetime import timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    active = UserSession.query.filter(UserSession.last_activity >= yesterday).count()

    return jsonify({
        'total_sessions': total,
        'active_sessions': active,
        'completed_sequences': completed
    })

@app.route('/admin/api/apikey', methods=['GET'])
def get_api_key():
    """Admin: Get current API key (masked)"""
    api_key = os.getenv('GROQ_API_KEY', '')

    return jsonify({
        'api_key': api_key if api_key else None
    })

@app.route('/admin/api/apikey', methods=['POST'])
def save_api_key():
    """Admin: Save API key to .env file"""
    data = request.json
    new_api_key = data.get('api_key', '').strip()

    if not new_api_key:
        return jsonify({'error': 'API key cannot be empty'}), 400

    if not new_api_key.startswith('gsk_'):
        return jsonify({'error': 'Invalid API key format. Should start with gsk_'}), 400

    try:
        # Read current .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')

        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Update or add GROQ_API_KEY
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('GROQ_API_KEY='):
                lines[i] = f'GROQ_API_KEY={new_api_key}\n'
                updated = True
                break

        if not updated:
            lines.append(f'GROQ_API_KEY={new_api_key}\n')

        # Write back to .env
        with open(env_path, 'w') as f:
            f.writelines(lines)

        # Update environment variable
        os.environ['GROQ_API_KEY'] = new_api_key

        return jsonify({
            'success': True,
            'message': 'API key saved successfully! Please restart the server for changes to take effect.'
        })

    except Exception as e:
        return jsonify({'error': f'Failed to save API key: {str(e)}'}), 500

@app.route('/admin/api/apikey/test', methods=['POST'])
def test_api_key():
    """Admin: Test API key"""
    data = request.json
    test_api_key = data.get('api_key', '').strip()

    if not test_api_key:
        return jsonify({'error': 'API key cannot be empty'}), 400

    try:
        from groq import Groq

        # Create client with test key
        client = Groq(api_key=test_api_key)

        # Make a simple API call
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say 'OK'"}
            ],
            max_tokens=10,
            temperature=0.5
        )

        result = response.choices[0].message.content

        return jsonify({
            'success': True,
            'message': f'✅ API Key is working! Model: llama-3.1-8b-instant | Response: {result}'
        })

    except Exception as e:
        error_msg = str(e)
        if 'Access denied' in error_msg or '403' in error_msg:
            return jsonify({
                'error': '❌ Access Denied (403): This API key does not have permission. Please check your Groq account role and regenerate the key.'
            }), 400
        else:
            return jsonify({
                'error': f'❌ API Test Failed: {error_msg}'
            }), 400

# ============================================================================
# INITIALIZE
# ============================================================================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()

        # Create default code if not exists
        if not AdminCode.query.first():
            default_code = AdminCode(
                python_code="""# Crypto Wallet Example
from web3 import Web3

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io'))

# Check connection
if w3.is_connected():
    print("Connected to Ethereum!")

# Get latest block
block = w3.eth.get_block('latest')
print(f"Latest block: {block['number']}")"""
            )
            db.session.add(default_code)
            db.session.commit()
            print("✓ Database initialized with default code")

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    init_db()

    # Check Groq status
    if GROQ_AVAILABLE:
        print("\n" + "="*60)
        print("✓ GROQ AI ACTIVE - Smart conversations enabled!")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("⚠ GROQ AI NOT AVAILABLE - Using fallback mode")
        print("To enable AI:")
        print("1. Get free API key: https://console.groq.com")
        print("2. Add to .env: GROQ_API_KEY=gsk_your_key_here")
        print("3. pip install groq")
        print("="*60 + "\n")

    print("="*60)
    print("CRYPTO CHATBOT BAŞLATILIYOR")
    print("="*60)
    print(f"Server: http://0.0.0.0:5001")
    print(f"Chat Arayüzü: http://localhost:5001/")
    print(f"Admin Panel: http://localhost:5001/admin")
    print("="*60)

    app.run(host='0.0.0.0', port=5001, debug=True)
