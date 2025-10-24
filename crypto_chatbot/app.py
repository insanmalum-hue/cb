import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from database import db, UserSession, AdminCode, init_db
from chatbot import ChatbotEngine

# .env dosyasını yükle
load_dotenv()

# Flask app oluştur
app = Flask(__name__)

# Konfigürasyon
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database'i başlat
init_db(app)

# Chatbot engine'i başlat
chatbot = ChatbotEngine()


# ============================================================================
# CHAT ROUTES
# ============================================================================

@app.route('/')
def index():
    """Ana sayfa - chat arayüzü"""
    return render_template('chat.html')


@app.route('/api/session/new', methods=['POST'])
def create_session():
    """
    Yeni bir kullanıcı oturumu oluşturur.

    Returns:
        JSON: {session_id: str}
    """
    try:
        # Yeni session ID oluştur
        session_id = str(uuid.uuid4())

        # Veritabanına kaydet
        new_session = UserSession(
            session_id=session_id,
            message_count=0,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        db.session.add(new_session)
        db.session.commit()

        return jsonify({'session_id': session_id}), 201

    except Exception as e:
        print(f"Session oluşturma hatası: {e}")
        return jsonify({'error': 'Session oluşturulamadı'}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Kullanıcı mesajını işler ve bot cevabı döndürür.

    Request JSON:
        {
            "message": str,
            "session_id": str
        }

    Returns:
        JSON: {
            "response": str,
            "metadata": {
                "word_used": str,
                "message_count": int,
                "remaining": int
            }
        }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message or not session_id:
            return jsonify({'error': 'Mesaj ve session_id gerekli'}), 400

        # Session kontrolü
        user_session = UserSession.query.filter_by(session_id=session_id).first()
        if not user_session:
            return jsonify({'error': 'Geçersiz session'}), 404

        # Son aktiviteyi güncelle
        user_session.last_activity = datetime.utcnow()

        # Mesaj sayısını kontrol et
        current_count = user_session.message_count

        # 36 mesaj tamamlandıysa
        if current_count >= 36:
            # Kod isteği mi?
            if chatbot.is_code_request(user_message):
                # AdminCode'dan kodu al
                admin_code = AdminCode.query.first()
                if admin_code:
                    response = chatbot.format_code_response(
                        admin_code.python_code,
                        current_count
                    )
                else:
                    response = "Code not found. Please contact admin."
            else:
                response = "You've completed all 36 messages! Type 'show code' to receive your Python code."

            db.session.commit()
            return jsonify({
                'response': response,
                'metadata': {
                    'word_used': None,
                    'message_count': current_count,
                    'remaining': 0
                }
            })

        # 36'dan az mesaj varsa
        target_word = chatbot.get_target_word(current_count)

        # Bot cevabı üret
        bot_response = chatbot.generate_response(
            user_message,
            target_word,
            session_id
        )

        # Mesaj sayısını artır
        user_session.message_count += 1
        db.session.commit()

        # Metadata hazırla
        remaining = 36 - user_session.message_count

        return jsonify({
            'response': bot_response,
            'metadata': {
                'word_used': target_word,
                'message_count': user_session.message_count,
                'remaining': remaining
            }
        })

    except Exception as e:
        print(f"Chat hatası: {e}")
        db.session.rollback()
        return jsonify({'error': 'Bir hata oluştu'}), 500


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
def admin():
    """Admin paneli sayfası"""
    return render_template('admin.html')


@app.route('/admin/api/code', methods=['GET'])
def get_admin_code():
    """
    Admin panelindeki Python kodunu döndürür.

    Returns:
        JSON: {
            "code": str,
            "updated_at": str
        }
    """
    try:
        admin_code = AdminCode.query.first()

        if admin_code:
            return jsonify({
                'code': admin_code.python_code,
                'updated_at': admin_code.updated_at.isoformat()
            })
        else:
            return jsonify({
                'code': '# No code found',
                'updated_at': None
            })

    except Exception as e:
        print(f"Admin kod okuma hatası: {e}")
        return jsonify({'error': 'Kod okunamadı'}), 500


@app.route('/admin/api/code', methods=['POST'])
def update_admin_code():
    """
    Admin panelindeki Python kodunu günceller.

    Request JSON:
        {
            "code": str
        }

    Returns:
        JSON: {"success": bool}
    """
    try:
        data = request.get_json()
        new_code = data.get('code', '').strip()

        if not new_code:
            return jsonify({'error': 'Kod boş olamaz'}), 400

        # İlk kaydı bul veya oluştur
        admin_code = AdminCode.query.first()

        if admin_code:
            admin_code.python_code = new_code
            admin_code.updated_at = datetime.utcnow()
        else:
            admin_code = AdminCode(
                python_code=new_code,
                updated_at=datetime.utcnow()
            )
            db.session.add(admin_code)

        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        print(f"Admin kod güncelleme hatası: {e}")
        db.session.rollback()
        return jsonify({'error': 'Kod güncellenemedi'}), 500


@app.route('/admin/api/stats', methods=['GET'])
def get_stats():
    """
    Sistem istatistiklerini döndürür.

    Returns:
        JSON: {
            "total_sessions": int,
            "active_sessions": int,
            "completed_sequences": int
        }
    """
    try:
        # Toplam session sayısı
        total_sessions = UserSession.query.count()

        # Aktif session'lar (son 24 saatte aktivite gösteren)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        active_sessions = UserSession.query.filter(
            UserSession.last_activity >= yesterday
        ).count()

        # Tamamlanmış sekanslar (36 mesaja ulaşanlar)
        completed_sequences = UserSession.query.filter(
            UserSession.message_count >= 36
        ).count()

        return jsonify({
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'completed_sequences': completed_sequences
        })

    except Exception as e:
        print(f"İstatistik hatası: {e}")
        return jsonify({'error': 'İstatistikler alınamadı'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CRYPTO CHATBOT BAŞLATILIYOR")
    print("=" * 60)
    print("Server: http://0.0.0.0:5000")
    print("Chat Arayüzü: http://localhost:5000/")
    print("Admin Panel: http://localhost:5000/admin")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
