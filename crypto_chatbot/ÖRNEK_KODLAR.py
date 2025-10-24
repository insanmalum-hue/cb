"""
ÖRNEK KRİPTOGRAFİ KODLARI
Crypto Chatbot Projesi için 8 Farklı Kriptografi Örneği

Bu dosya, kullanıcılara admin panelden gösterilmek üzere hazırlanmış
örnek kriptografi kodlarını içerir. Her örnek çalışır durumdadır.
"""

print("=" * 70)
print("KRİPTOGRAFİ ÖRNEKLERİ - CRYPTO CHATBOT")
print("=" * 70)

# ============================================================================
# ÖRNEK 1: Fernet Encryption (Symmetric)
# ============================================================================
print("\n1. FERNET ENCRYPTION (Symmetric - cryptography library)")
print("-" * 70)

from cryptography.fernet import Fernet

# Anahtar oluştur
fernet_key = Fernet.generate_key()
print(f"Oluşturulan Anahtar: {fernet_key.decode()}")

# Cipher oluştur
cipher_suite = Fernet(fernet_key)

# Şifreleme
plain_text = b"Bu gizli bir mesajdir - Crypto Chatbot"
encrypted_text = cipher_suite.encrypt(plain_text)
print(f"Şifreli Metin: {encrypted_text.decode()}")

# Şifre çözme
decrypted_text = cipher_suite.decrypt(encrypted_text)
print(f"Çözülmüş Metin: {decrypted_text.decode()}")
print("✓ Fernet encryption başarılı!")


# ============================================================================
# ÖRNEK 2: AES-256 Encryption
# ============================================================================
print("\n2. AES-256 ENCRYPTION (Advanced Encryption Standard)")
print("-" * 70)

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# 256-bit anahtar (32 byte)
aes_key = get_random_bytes(32)
print(f"AES-256 Anahtar (hex): {aes_key.hex()[:40]}...")

# Şifreleme
cipher = AES.new(aes_key, AES.MODE_CBC)
plain_data = b"AES-256 ile korunan veri"
encrypted_data = cipher.encrypt(pad(plain_data, AES.block_size))

print(f"IV (Initialization Vector): {base64.b64encode(cipher.iv).decode()}")
print(f"Şifreli Veri: {base64.b64encode(encrypted_data).decode()[:40]}...")

# Şifre çözme
decipher = AES.new(aes_key, AES.MODE_CBC, cipher.iv)
decrypted_data = unpad(decipher.decrypt(encrypted_data), AES.block_size)
print(f"Çözülmüş Veri: {decrypted_data.decode()}")
print("✓ AES-256 encryption başarılı!")


# ============================================================================
# ÖRNEK 3: RSA Asymmetric Encryption
# ============================================================================
print("\n3. RSA ASYMMETRIC ENCRYPTION (Public/Private Key)")
print("-" * 70)

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# RSA anahtar çifti oluştur (2048 bit)
rsa_key = RSA.generate(2048)
private_key = rsa_key
public_key = rsa_key.publickey()

print(f"Public Key (ilk 60 karakter):")
print(f"{public_key.export_key().decode()[:60]}...")
print(f"Private Key (ilk 60 karakter):")
print(f"{private_key.export_key().decode()[:60]}...")

# Public key ile şifreleme
rsa_cipher = PKCS1_OAEP.new(public_key)
rsa_message = b"RSA ile sifrelenmis mesaj"
rsa_encrypted = rsa_cipher.encrypt(rsa_message)
print(f"\nŞifreli Mesaj (base64): {base64.b64encode(rsa_encrypted).decode()[:40]}...")

# Private key ile şifre çözme
rsa_decipher = PKCS1_OAEP.new(private_key)
rsa_decrypted = rsa_decipher.decrypt(rsa_encrypted)
print(f"Çözülmüş Mesaj: {rsa_decrypted.decode()}")
print("✓ RSA asymmetric encryption başarılı!")


# ============================================================================
# ÖRNEK 4: SHA-256 Hash ve HMAC
# ============================================================================
print("\n4. SHA-256 HASH ve HMAC (Message Authentication)")
print("-" * 70)

import hashlib
import hmac

# SHA-256 Hash
data = b"Crypto Chatbot - Hash ornegi"
sha256_hash = hashlib.sha256(data).hexdigest()
print(f"Veri: {data.decode()}")
print(f"SHA-256 Hash: {sha256_hash}")

# HMAC (Hash-based Message Authentication Code)
hmac_key = b"gizli-anahtar-2024"
hmac_hash = hmac.new(hmac_key, data, hashlib.sha256).hexdigest()
print(f"\nHMAC Anahtarı: {hmac_key.decode()}")
print(f"HMAC-SHA256: {hmac_hash}")

# Doğrulama
is_valid = hmac.compare_digest(
    hmac_hash,
    hmac.new(hmac_key, data, hashlib.sha256).hexdigest()
)
print(f"HMAC Doğrulama: {'✓ Geçerli' if is_valid else '✗ Geçersiz'}")
print("✓ SHA-256 ve HMAC başarılı!")


# ============================================================================
# ÖRNEK 5: BIP39 Mnemonic (Cryptocurrency Seed Phrase)
# ============================================================================
print("\n5. BIP39 MNEMONIC (Cryptocurrency Seed Phrase)")
print("-" * 70)

from mnemonic import Mnemonic

# Mnemonic oluşturucu
mnemo = Mnemonic("english")

# 12 kelimelik seed phrase oluştur
seed_phrase = mnemo.generate(strength=128)
print(f"12-Kelimelik Seed Phrase:")
print(f"  {seed_phrase}")

# 24 kelimelik seed phrase oluştur
seed_phrase_24 = mnemo.generate(strength=256)
print(f"\n24-Kelimelik Seed Phrase:")
print(f"  {' '.join(seed_phrase_24.split()[:12])}")
print(f"  {' '.join(seed_phrase_24.split()[12:])}")

# Seed phrase'den entropy'ye dönüşüm
seed_bytes = mnemo.to_seed(seed_phrase, passphrase="")
print(f"\nSeed (hex - ilk 40 karakter): {seed_bytes.hex()[:40]}...")

# Doğrulama
is_valid = mnemo.check(seed_phrase)
print(f"Seed Phrase Doğrulama: {'✓ Geçerli' if is_valid else '✗ Geçersiz'}")
print("✓ BIP39 mnemonic başarılı!")


# ============================================================================
# ÖRNEK 6: Bcrypt Password Hashing
# ============================================================================
print("\n6. BCRYPT PASSWORD HASHING (Secure Password Storage)")
print("-" * 70)

import bcrypt

# Şifre hashleme
password = b"SuperGizliSifre123!"
salt = bcrypt.gensalt(rounds=12)
hashed_password = bcrypt.hashpw(password, salt)

print(f"Orijinal Şifre: {password.decode()}")
print(f"Salt: {salt.decode()}")
print(f"Hashed Şifre: {hashed_password.decode()}")

# Şifre doğrulama
correct_password = b"SuperGizliSifre123!"
wrong_password = b"YanlisSifre123"

is_correct = bcrypt.checkpw(correct_password, hashed_password)
is_wrong = bcrypt.checkpw(wrong_password, hashed_password)

print(f"\nDoğru Şifre Kontrolü: {'✓ Eşleşti' if is_correct else '✗ Eşleşmedi'}")
print(f"Yanlış Şifre Kontrolü: {'✓ Eşleşti' if is_wrong else '✗ Eşleşmedi'}")
print("✓ Bcrypt password hashing başarılı!")


# ============================================================================
# ÖRNEK 7: Base64 Encoding/Decoding
# ============================================================================
print("\n7. BASE64 ENCODING (Data Encoding)")
print("-" * 70)

import base64

# String encoding
original_string = "Crypto Chatbot - Base64 Örneği 🔐"
encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

print(f"Orijinal String: {original_string}")
print(f"Base64 Encoded: {encoded_string}")

# Decoding
decoded_bytes = base64.b64decode(encoded_string)
decoded_string = decoded_bytes.decode('utf-8')
print(f"Base64 Decoded: {decoded_string}")

# URL-safe Base64
url_safe_encoded = base64.urlsafe_b64encode(original_string.encode('utf-8'))
print(f"\nURL-Safe Base64: {url_safe_encoded.decode()}")

# Binary data encoding
binary_data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'
binary_encoded = base64.b64encode(binary_data).decode()
print(f"Binary Data Encoded: {binary_encoded}")
print("✓ Base64 encoding başarılı!")


# ============================================================================
# ÖRNEK 8: XOR Encryption (Simple Cipher)
# ============================================================================
print("\n8. XOR ENCRYPTION (Simple Cipher - Eğitim Amaçlı)")
print("-" * 70)

def xor_encrypt_decrypt(data, key):
    """XOR encryption/decryption (aynı fonksiyon)"""
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

# XOR ile şifreleme
xor_message = b"XOR Cipher Ornegi"
xor_key = b"SECRET_KEY"

encrypted = xor_encrypt_decrypt(xor_message, xor_key)
print(f"Orijinal Mesaj: {xor_message.decode()}")
print(f"XOR Anahtarı: {xor_key.decode()}")
print(f"Şifreli (hex): {encrypted.hex()}")
print(f"Şifreli (base64): {base64.b64encode(encrypted).decode()}")

# XOR ile şifre çözme (aynı fonksiyon)
decrypted = xor_encrypt_decrypt(encrypted, xor_key)
print(f"Çözülmüş Mesaj: {decrypted.decode()}")

# XOR özelliği: iki kez uygulama orijinali verir
double_xor = xor_encrypt_decrypt(encrypted, xor_key)
print(f"İki kez XOR: {double_xor.decode()} (orijinal mesaj)")
print("✓ XOR encryption başarılı!")

print("\n" + "=" * 70)
print("TÜM KRİPTOGRAFİ ÖRNEKLERİ BAŞARIYLA TAMAMLANDI!")
print("=" * 70)
print("\n⚠️  DİKKAT: Bu örnekler eğitim amaçlıdır.")
print("Gerçek uygulamalarda güvenlik best practices'i uygulayın.")
print("Private key'leri ve seed phrase'leri asla paylaşmayın!")
print("\n🔐 Crypto Chatbot - Güvenli İletişim İçin")
