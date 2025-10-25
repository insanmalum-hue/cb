"""
Advanced Chatbot with Ollama Llama 3
Kelimeleri AI ile doğal cümlelerde kullanır
"""

import requests
import json

class AdvancedChatbot:
    def __init__(self):
        # 36 sabit kelime - sırayla kullanılacak
        self.words = [
            "pilot", "giant", "enable", "syrup", "medal", "hero", "iron", "soap",
            "visual", "vendor", "genuine", "punch", "grid", "floor", "glide", "penalty",
            "blossom", "crew", "pival", "sheriff", "solar", "claw", "oak", "find",
            "bind", "pet", "urban", "else", "series", "wave", "pumpkin", "amount",
            "verb", "similar", "crime", "bird"
        ]

        self.ollama_url = "http://localhost:11434"
        self.model = "llama3.2"

        # Ollama bağlantısını kontrol et
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    self.ollama_available = True
                    print(f"✓ Ollama Llama 3 active! Model: {self.model}")
                else:
                    self.ollama_available = False
                    print("⚠ No models found. Run: ollama pull llama3.2")
            else:
                self.ollama_available = False
                print("⚠ Ollama not responding")
        except Exception as e:
            self.ollama_available = False
            print(f"⚠ Ollama not available: {e}")
            print("  Solution: Open Ollama app or run 'ollama serve'")

    def get_target_word(self, message_count):
        """Mesaj numarasına göre hedef kelimeyi al"""
        if message_count >= 36:
            return None
        return self.words[message_count]

    def generate_response(self, user_message, message_count, conversation_history=None):
        """
        AI ile yanıt üret - kelimeyi doğal şekilde kullan
        """
        target_word = self.get_target_word(message_count)

        if not target_word:
            return "Tebrikler! 36 mesajı tamamladın. 'show code' yazarak kodunu al."

        if self.ollama_available:
            try:
                return self._generate_with_llama(user_message, target_word, conversation_history)
            except Exception as e:
                print(f"Llama error: {e}")
                return self._fallback_response(target_word)
        else:
            return self._fallback_response(target_word)

    def _generate_with_llama(self, user_message, target_word, conversation_history):
        """
        Llama 3 ile yanıt üret
        Kelime SABİT ama etrafındaki cümleler AI tarafından üretilir
        """

        # System prompt - Türkçe ve doğal konuşma
        system_prompt = f"""Sen samimi ve yardımsever bir AI asistanısın. Türkçe konuşuyorsun.

KRİTİK KURAL:
- Yanıtında '{target_word}' kelimesini MUTLAKA kullan
- Ama kelimeyi DOĞAL ve YARATICI bir şekilde cümleye yerleştir
- Her seferinde FARKLI bir cümle kur
- 2-3 cümle ile özet ve samimi ol
- Kullanıcının sorusuna gerçekten cevap ver

KÖTÜ ÖRNEKLER (tekrarlı, yapay):
❌ "İyi soru! '{target_word}' önemli bir kavram."
❌ "'{target_word}' hakkında konuşalım."

İYİ ÖRNEKLER (doğal, yaratıcı):
✅ Kelime: pilot → "Harika gidiyorum! Sanki bir pilot gibi rahat ve kontrollü hissediyorum. Sen nasılsın?"
✅ Kelime: giant → "AI kesinlikle giant bir etki yaratıyor dünyada! Her gün yeni gelişmeler oluyor."
✅ Kelime: enable → "Teknoloji insanlara inanılmaz şeyler yapma imkanı enable ediyor. Örneğin AI gibi!"
✅ Kelime: syrup → "Kahvaltıda syrup seviyorum aslında, tatlı bir başlangıç güne. Sen ne seversin?"
✅ Kelime: hero → "Her insan kendi hayatının hero'su olabilir. Küçük adımlar bile önemli!"

Şimdi kullanıcıya cevap ver ve '{target_word}' kelimesini YARATICI şekilde kullan:"""

        # Conversation history ekle
        conversation_context = ""
        if conversation_history:
            try:
                history = json.loads(conversation_history) if isinstance(conversation_history, str) else conversation_history
                recent = history[-4:] if len(history) > 4 else history

                if recent:
                    conversation_context = "\n\nÖnceki konuşma:\n"
                    for msg in recent:
                        role = "Kullanıcı" if msg.get('type') == 'user' else "Sen"
                        conversation_context += f"{role}: {msg.get('content', '')}\n"
            except:
                pass

        # Tam prompt
        full_prompt = f"""{system_prompt}

{conversation_context}

Kullanıcı: {user_message}

Sen ('{target_word}' kelimesini doğal şekilde kullanarak):"""

        # Ollama API çağrısı
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.9,  # Yaratıcılık için yüksek
                    "top_p": 0.95,
                    "top_k": 50,
                    "num_predict": 200,
                    "stop": ["\n\nKullanıcı:", "\nKullanıcı:"]
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            bot_response = response.json()['response'].strip()

            # Gereksiz ekleri temizle
            if bot_response.startswith("Sen:"):
                bot_response = bot_response[4:].strip()

            # Kelime kontrolü - yoksa ekle (son çare)
            if target_word.lower() not in bot_response.lower():
                bot_response += f" Bu arada, '{target_word}' kelimesi ilginç değil mi?"

            return bot_response
        else:
            raise Exception(f"Ollama API error: {response.status_code}")

    def _fallback_response(self, target_word):
        """Ollama yoksa basit yanıt"""
        import random

        templates = [
            f"Harika soru! '{target_word}' gerçekten ilginç bir konu.",
            f"Bunu merak etmen güzel! '{target_word}' hakkında düşünelim.",
            f"İyi nokta! '{target_word}' ile ilgili çok şey söylenebilir.",
            f"Anlıyorum! '{target_word}' önemli bir kavram aslında.",
            f"Teşekkürler! '{target_word}' gerçekten keşfetmeye değer."
        ]

        return random.choice(templates)

# Global instance
chatbot = AdvancedChatbot()
