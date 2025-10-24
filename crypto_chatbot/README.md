# 🔐 Crypto Chatbot

A progressive word disclosure chatbot system that reveals seed phrase words naturally through conversation. Users chat naturally with an AI-powered bot, and after 36 messages, they can request their Python code.

## ✨ Features

- **Progressive Word Disclosure**: Each message naturally includes one of 36 seed phrase words
- **OpenAI Integration**: GPT-4o-mini powered conversations with natural word embedding
- **Fallback Mode**: Continues to work without OpenAI API key
- **Session Management**: Persistent user sessions with SQLite database
- **Admin Panel**: Live statistics and Python code configuration
- **Modern UI**: Responsive chat interface with gradient design
- **Real-time Progress**: Visual progress bar and message counter
- **Code Delivery**: Formatted Python code delivery after sequence completion

## 📝 The 36-Word List

The system uses these 36 words in sequence:

| # | Word | # | Word | # | Word | # | Word |
|---|------|---|------|---|------|---|------|
| 1 | pilot | 10 | vendor | 19 | pival | 28 | else |
| 2 | giant | 11 | genuine | 20 | sheriff | 29 | series |
| 3 | enable | 12 | punch | 21 | solar | 30 | wave |
| 4 | syrup | 13 | grid | 22 | claw | 31 | pumpkin |
| 5 | medal | 14 | floor | 23 | oak | 32 | amount |
| 6 | hero | 15 | glide | 24 | find | 33 | verb |
| 7 | iron | 16 | penalty | 25 | bind | 34 | similar |
| 8 | soap | 17 | blossom | 26 | pet | 35 | crime |
| 9 | visual | 18 | crew | 27 | urban | 36 | bird |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (optional, fallback mode available)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd crypto_chatbot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

Edit the `.env` file and add at least one AI API key:

#### Option A: FREE AI APIs (Recommended - Much Faster!)

**🚀 Groq API (FASTEST - 300+ tokens/sec)**
1. Visit https://console.groq.com
2. Create free account
3. Generate API key
4. Add to `.env`: `GROQ_API_KEY=your-key-here`

**🤗 Hugging Face (Free 1000 req/hour)**
1. Visit https://huggingface.co/settings/tokens
2. Create token
3. Add to `.env`: `HUGGINGFACE_API_KEY=your-token-here`

**🌐 Together AI (Free $25 credit)**
1. Visit https://api.together.xyz
2. Sign up
3. Get API key
4. Add to `.env`: `TOGETHER_API_KEY=your-key-here`

**💬 Cohere (Free tier)**
1. Visit https://dashboard.cohere.com/api-keys
2. Create API key
3. Add to `.env`: `COHERE_API_KEY=your-key-here`

#### Option B: OpenAI (Paid)

```
OPENAI_API_KEY=your-openai-api-key-here
```

**Note**: If no API key is provided, the system will run in fallback mode with pre-generated responses. For best experience, use Groq API (fastest and free!).

### Step 4: Run the Application

```bash
python app.py
```

The application will be available at:
- **Chat Interface**: http://localhost:5000/
- **Admin Panel**: http://localhost:5000/admin

## 📖 Usage Guide

### For Users

1. **Start Chatting**: Open the chat interface and start a conversation
2. **Natural Conversation**: Chat naturally about any topic
3. **Progress Tracking**: Watch the progress bar fill up (0-36 messages)
4. **Complete Sequence**: After 36 messages, type "show code" or "give code"
5. **Receive Code**: Get your formatted Python code

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin`
2. **View Statistics**:
   - Total Sessions: All user sessions created
   - Active Sessions: Sessions active in last 24 hours
   - Completed Sequences: Users who reached 36 messages
3. **Edit Python Code**: Modify the code that users receive
4. **Save Changes**: Click "Save Code" to update

## 🧪 Test Scenario

To test the complete flow:

1. **Open Chat**: Visit http://localhost:5000/
2. **Send Messages**: Type 36 different messages
3. **Observe Words**: Each bot response includes one seed word
4. **Request Code**: After message 36, type "show code"
5. **Verify Code**: Check that the Python code is displayed
6. **Admin Check**: Visit `/admin` to see statistics updated

Example test messages:
```
1. "Hello, how are you?"
2. "Tell me about the weather"
3. "What's your favorite color?"
... continue to 36 messages ...
36. "Thank you for chatting"
37. "show code"
```

## 🛠️ Technical Stack

### Backend
- **Flask 3.0.0**: Web framework
- **SQLAlchemy 3.1.1**: Database ORM
- **OpenAI 1.12.0**: AI conversation engine
- **Python-dotenv 1.0.0**: Environment configuration

### Frontend
- **Vanilla JavaScript**: No frameworks, pure JS
- **CSS3**: Modern gradient designs and animations
- **HTML5**: Semantic markup

### Database
- **SQLite**: Lightweight embedded database
- **Tables**: UserSession, AdminCode

### AI Model
- **GPT-4o-mini**: OpenAI's efficient model
- **Temperature**: 0.8 for natural variety
- **Context**: 20-message conversation memory

## 📁 Project Structure

```
crypto_chatbot/
├── app.py                  # Flask application and routes
├── chatbot.py              # ChatbotEngine and AI logic
├── database.py             # SQLAlchemy models
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── .gitignore             # Git ignore rules
├── templates/
│   ├── chat.html          # Chat interface
│   └── admin.html         # Admin panel
├── static/
│   └── chat.js            # Chat client JavaScript
├── README.md              # This file
├── BAŞLANGIÇ.md           # Turkish quick start guide
└── test_system.py         # System tests
```

## 🔒 Security Notes

### Important Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **SECRET_KEY**: Change the default secret key in production
3. **API Keys**: Keep OpenAI API keys secure
4. **Admin Access**: Implement authentication for admin panel in production
5. **Input Validation**: All user inputs are validated and sanitized
6. **Database**: SQLite is suitable for development; use PostgreSQL for production

### Production Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Add admin authentication
- [ ] Use production-grade database (PostgreSQL/MySQL)
- [ ] Enable HTTPS
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Add logging and monitoring
- [ ] Regular security audits

## ⚙️ Customization Options

### Changing the Word List

Edit `chatbot.py` and modify the `WORDS` list:

```python
WORDS = [
    "your", "custom", "word", "list", ...
]
```

**Note**: Must be exactly 36 words.

### Adjusting AI Behavior

In `chatbot.py`, modify the `_generate_with_openai` method:

```python
response = self.client.chat.completions.create(
    model="gpt-4o-mini",  # Change model
    temperature=0.8,       # Adjust creativity (0.0-2.0)
    max_tokens=500         # Adjust response length
)
```

### Customizing the UI

- **Colors**: Edit gradient colors in `templates/chat.html` and `admin.html`
- **Progress Bar**: Modify `.progress-bar` styles
- **Message Appearance**: Customize `.message-content` classes

### Default Python Code

The default code shown to users can be set in the Admin Panel or by modifying `database.py`:

```python
default_code = AdminCode(
    python_code="# Your custom default code here",
    updated_at=datetime.utcnow()
)
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete and recreate database
rm chatbot.db
python app.py  # Database auto-creates on startup
```

### OpenAI API Errors
- Check API key in `.env` file
- Verify API key has credits
- System will fallback automatically

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For questions or support, please open an issue in the repository.

---

**⚠️ Disclaimer**: This is a demonstration project. For production use, implement proper security measures, authentication, and follow best practices for web application deployment.
