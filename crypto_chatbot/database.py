from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class UserSession(db.Model):
    """Kullanıcı oturum bilgilerini saklar"""
    __tablename__ = 'user_sessions'

    session_id = db.Column(db.String(100), primary_key=True)
    message_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<UserSession {self.session_id}>'


class AdminCode(db.Model):
    """Admin panelden düzenlenebilir Python kodunu saklar"""
    __tablename__ = 'admin_codes'

    id = db.Column(db.Integer, primary_key=True)
    python_code = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<AdminCode {self.id}>'


def init_db(app):
    """
    Veritabanını başlatır ve gerekli tabloları oluşturur.
    AdminCode tablosu boşsa varsayılan kod ekler.
    """
    db.init_app(app)

    with app.app_context():
        # Tabloları oluştur
        db.create_all()

        # AdminCode tablosu boşsa varsayılan kod ekle
        if AdminCode.query.count() == 0:
            default_code = AdminCode(
                python_code="# Admin panelden Python kodunuzu girin",
                updated_at=datetime.utcnow()
            )
            db.session.add(default_code)
            db.session.commit()
            print("Varsayılan admin kodu eklendi.")
        else:
            print("AdminCode tablosu zaten dolu.")
