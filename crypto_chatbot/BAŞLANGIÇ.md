# 🔐 Crypto Chatbot - Hızlı Başlangıç Rehberi

Crypto Chatbot, kullanıcılarla doğal sohbet ederken 36 kelimelik bir seed phrase'i ilerleyici şekilde açığa çıkaran akıllı bir chatbot sistemidir.

## 🚀 5 Adımda Kurulum

### Adım 1: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

**Gerekli Paketler:**
- Flask 3.0.0 (Web framework)
- Flask-SQLAlchemy 3.1.1 (Veritabanı)
- OpenAI 1.12.0 (AI motoru)
- python-dotenv 1.0.0 (Çevre değişkenleri)

### Adım 2: Çevre Değişkenlerini Ayarlayın

`.env` dosyasını düzenleyin:

```
SECRET_KEY=crypto-secret-key-12345-change-in-production
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Not:** OpenAI API anahtarınız yoksa boş bırakın. Sistem otomatik olarak fallback moduna geçecektir.

### Adım 3: Uygulamayı Başlatın

```bash
python app.py
```

Başarılı başlatma mesajı:
```
============================================================
CRYPTO CHATBOT BAŞLATILIYOR
============================================================
Server: http://0.0.0.0:5000
Chat Arayüzü: http://localhost:5000/
Admin Panel: http://localhost:5000/admin
============================================================
```

### Adım 4: Chat Arayüzünü Açın

Tarayıcınızda açın: **http://localhost:5000/**

### Adım 5: Chatbot ile Konuşun

Hoş geldiniz mesajını göreceksiniz. Doğal bir şekilde sohbet etmeye başlayın!

## 📱 Nasıl Kullanılır?

### Kullanıcı Olarak

1. **Sohbet Başlatın**
   - Chat arayüzünü açın
   - "Hello" veya "Merhaba" ile başlayın

2. **Doğal Konuşun**
   - Herhangi bir konu hakkında konuşabilirsiniz
   - Hava durumu, hobiler, teknoloji, vb.
   - Bot her cevabında bir seed kelimesi kullanacak

3. **İlerlemeyi İzleyin**
   - Üstteki progress bar'ı takip edin
   - "Message X/36" göstergesini kontrol edin
   - Kalan mesaj sayısını görün

4. **Sekansı Tamamlayın**
   - 36 mesaj gönderdikten sonra
   - "show code" veya "kod göster" yazın

5. **Kodunuzu Alın**
   - Python kodunuz formatlanmış şekilde görünecek
   - Kopyalayıp kullanabilirsiniz

### Yönetici Olarak

1. **Admin Panele Giriş**
   - http://localhost:5000/admin adresini açın

2. **İstatistikleri Görüntüleyin**
   - **Total Sessions**: Oluşturulan toplam oturum
   - **Active Sessions**: Son 24 saatte aktif oturumlar
   - **Completed Sequences**: 36 mesajı tamamlayanlar
   - Her 15 saniyede otomatik güncellenir

3. **Python Kodunu Düzenleyin**
   - Kod editöründe Python kodunuzu yazın
   - Kullanıcılara gösterilecek kodu özelleştirin
   - Monospace font ile rahat düzenleme

4. **Değişiklikleri Kaydedin**
   - "💾 Save Code" butonuna tıklayın
   - Başarı mesajını bekleyin
   - Last updated zamanı güncellenecek

5. **Kodu Yeniden Yükleyin**
   - "🔄 Reload" butonu ile mevcut kodu geri yükleyin
   - Yaptığınız değişiklikleri iptal edebilirsiniz

## 📊 36 Kelime Tablosu

Sistemin kullandığı 36 kelime sırasıyla:

| Sıra | Kelime | Sıra | Kelime | Sıra | Kelime | Sıra | Kelime |
|------|--------|------|--------|------|--------|------|--------|
| 1 | pilot | 10 | vendor | 19 | pival | 28 | else |
| 2 | giant | 11 | genuine | 20 | sheriff | 29 | series |
| 3 | enable | 12 | punch | 21 | solar | 30 | wave |
| 4 | syrup | 13 | grid | 22 | claw | 31 | pumpkin |
| 5 | medal | 14 | floor | 23 | oak | 32 | amount |
| 6 | hero | 15 | glide | 24 | find | 33 | verb |
| 7 | iron | 16 | penalty | 25 | bind | 34 | similar |
| 8 | soap | 17 | blossom | 26 | pet | 35 | crime |
| 9 | visual | 18 | crew | 27 | urban | 36 | bird |

**Not:** Kelimeler kullanıcının her mesajına verilen bot cevabında doğal bir şekilde yerleştirilir.

## 💡 İpuçları

### Kullanıcılar İçin

1. **Doğal Konuşun**
   - Kısa cümleler yerine detaylı sorular sorun
   - Bot'un cevaplarını okuyun, içlerinde gizli kelimeler var
   - Normal bir konuşma gibi davranın

2. **Progress'i Takip Edin**
   - Progress bar'ı gözlemleyin
   - Kalan mesaj sayısına dikkat edin
   - Son 5 mesajda hint değişir

3. **Kod İsteme**
   - 36 mesaj sonrası bu komutlardan birini kullanın:
     - "show code"
     - "give code"
     - "kod göster"
     - "kod ver"

4. **Session Yönetimi**
   - Tarayıcınızı kapatıp açsanız bile session devam eder
   - localStorage kullanılır
   - Her kullanıcının kendi session'ı vardır

### Yöneticiler İçin

1. **Kod Örnekleri**
   - Seed phrase oluşturma kodu
   - Wallet oluşturma scripti
   - Kripto işlem örnekleri

2. **Güvenlik**
   - Gerçek private key'leri koymayın
   - Örnek/demo kodları kullanın
   - Üretim ortamında admin panele kimlik doğrulama ekleyin

3. **İzleme**
   - İstatistikleri düzenli kontrol edin
   - Completed sequences sayısını takip edin
   - Active sessions ile kullanıcı aktivitesini görün

## 🐛 Sorun Giderme

### Veritabanı Hatası

**Sorun:** "database is locked" veya benzeri hatalar

**Çözüm:**
```bash
rm chatbot.db
python app.py
```

### OpenAI API Hatası

**Sorun:** "OpenAI API error" veya "401 Unauthorized"

**Çözüm:**
1. `.env` dosyasındaki API anahtarını kontrol edin
2. OpenAI hesabınızda kredi olduğundan emin olun
3. API anahtarını yenileyin
4. Yoksa boş bırakın, fallback mode çalışacak

### Port Zaten Kullanımda

**Sorun:** "Address already in use" hatası

**Çözüm:**
```bash
# app.py'de portu değiştirin
app.run(debug=True, host='0.0.0.0', port=5001)
```

veya çalışan process'i sonlandırın:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Session Kayboldu

**Sorun:** Progress sıfırlandı

**Çözüm:**
1. localStorage'ı temizleyin (F12 > Application > Local Storage)
2. Sayfayı yenileyin
3. Yeni session otomatik oluşturulacak

### Bot Cevap Vermiyor

**Sorun:** Typing indicator dondu

**Çözüm:**
1. Console'u açın (F12)
2. Network hatalarını kontrol edin
3. Sayfayı yenileyin
4. Backend loglarını kontrol edin

### Admin Panel Açılmıyor

**Sorun:** 404 veya 500 hatası

**Çözüm:**
1. URL'yi kontrol edin: `http://localhost:5000/admin`
2. Flask uygulamasının çalıştığından emin olun
3. Terminal'de hata mesajlarını kontrol edin

## 🔧 Gelişmiş Özelleştirme

### Kelime Listesini Değiştirme

`chatbot.py` dosyasını düzenleyin:

```python
WORDS = [
    "kendi", "özel", "kelime", "listeniz", ...  # 36 kelime
]
```

### AI Davranışını Ayarlama

```python
# chatbot.py - _generate_with_openai metodunda
response = self.client.chat.completions.create(
    model="gpt-4o-mini",        # Model seçimi
    temperature=0.8,             # Yaratıcılık (0.0-2.0)
    max_tokens=500               # Maksimum cevap uzunluğu
)
```

### Arayüz Renklerini Değiştirme

`templates/chat.html` ve `admin.html` dosyalarında:

```css
/* Gradient renkleri */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Değiştirin: */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Varsayılan Kodu Ayarlama

Admin panelden düzenleyin veya `database.py` dosyasında:

```python
default_code = AdminCode(
    python_code="""
# Kendi varsayılan kodunuz
print('Merhaba Dünya!')
""",
    updated_at=datetime.utcnow()
)
```

## 📞 Destek

Sorularınız veya sorunlarınız için:
- GitHub Issues: Repository'de issue açın
- Dokümantasyon: README.md dosyasını inceleyin
- Loglar: Terminal çıktılarını kontrol edin

## 🎯 Test Senaryosu

Tam akışı test etmek için:

1. Uygulamayı başlatın
2. Chat arayüzünü açın
3. 36 farklı mesaj gönderin
4. Her bot cevabında bir kelime arayın
5. 36. mesajdan sonra "show code" yazın
6. Python kodunun göründüğünü doğrulayın
7. Admin paneli açın
8. İstatistiklerin güncellendiğini görün

**Örnek Test Mesajları:**
```
1. "Merhaba, nasılsın?"
2. "Bugün hava nasıl?"
3. "En sevdiğin renk ne?"
4. "Teknoloji hakkında ne düşünüyorsun?"
... 36 mesaja kadar devam et ...
36. "Teşekkürler, harika bir sohbetti"
37. "show code"
```

## ⚠️ Önemli Notlar

- Bu bir demonstrasyon projesidir
- Üretim ortamında güvenlik önlemleri alın
- Admin paneline kimlik doğrulama ekleyin
- SECRET_KEY'i değiştirin
- HTTPS kullanın
- Gerçek seed phrase'leri saklamayın

---

**🎉 İyi Kullanımlar!**

Sorularınız için dokümantasyonu inceleyin veya issue açın.
