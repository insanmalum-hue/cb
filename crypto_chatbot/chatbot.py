import os
import re
import random
from openai import OpenAI
from typing import Optional

# 36 kelimelik seed phrase listesi
WORDS = [
    "pilot", "giant", "enable", "syrup", "medal", "hero", "iron", "soap",
    "visual", "vendor", "genuine", "punch", "grid", "floor", "glide", "penalty",
    "blossom", "crew", "pival", "sheriff", "solar", "claw", "oak", "find",
    "bind", "pet", "urban", "else", "series", "wave", "pumpkin", "amount",
    "verb", "similar", "crime", "bird"
]


class ChatbotEngine:
    """OpenAI tabanlı chatbot motoru - fallback desteği ile"""

    def __init__(self):
        """OpenAI client'ı başlatır veya fallback mode'a geçer"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.conversation_memory = {}  # session_id -> mesaj listesi

        if self.api_key and self.api_key.strip():
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("OpenAI client başlatıldı.")
            except Exception as e:
                print(f"OpenAI client başlatılamadı: {e}")
                print("Fallback mode aktif.")
        else:
            print("OPENAI_API_KEY bulunamadı. Fallback mode aktif.")

    def is_code_request(self, message: str) -> bool:
        """
        Kullanıcının kod isteyip istemediğini kontrol eder.

        Args:
            message: Kullanıcı mesajı

        Returns:
            bool: Kod isteği varsa True
        """
        patterns = [
            r'\bshow\s+code\b',
            r'\bgive\s+code\b',
            r'\bkod\s+yaz\b',
            r'\bkod\s+ver\b',
            r'\bkodu\s+göster\b',
            r'\bget\s+code\b',
            r'\bkodu\s+al\b',
        ]

        message_lower = message.lower()
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return True
        return False

    def get_target_word(self, message_count: int) -> Optional[str]:
        """
        Mesaj sayısına göre hedef kelimeyi döndürür.

        Args:
            message_count: Kullanıcının gönderdiği mesaj sayısı

        Returns:
            str: Hedef kelime veya None (36+ mesaj için)
        """
        if 0 <= message_count < 36:
            return WORDS[message_count]
        return None

    def generate_response(self, user_message: str, target_word: Optional[str],
                         session_id: str) -> str:
        """
        Kullanıcı mesajına cevap üretir.

        Args:
            user_message: Kullanıcı mesajı
            target_word: Cevaba dahil edilmesi gereken hedef kelime
            session_id: Kullanıcı oturumu ID'si

        Returns:
            str: Bot cevabı
        """
        if self.client:
            return self._generate_with_openai(user_message, target_word, session_id)
        else:
            return self._generate_fallback(user_message, target_word)

    def _generate_with_openai(self, user_message: str, target_word: Optional[str],
                             session_id: str) -> str:
        """
        OpenAI API kullanarak cevap üretir.

        Args:
            user_message: Kullanıcı mesajı
            target_word: Hedef kelime
            session_id: Oturum ID'si

        Returns:
            str: OpenAI'dan gelen cevap
        """
        # Conversation history'yi başlat
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []

        # System prompt hazırla
        system_content = "You are a helpful and friendly assistant."
        if target_word:
            system_content += f" You must use the word '{target_word}' naturally in your response."

        # Mesajları hazırla
        messages = [{"role": "system", "content": system_content}]
        messages.extend(self.conversation_memory[session_id])
        messages.append({"role": "user", "content": user_message})

        try:
            # OpenAI API çağrısı
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,
                max_tokens=500
            )

            bot_response = response.choices[0].message.content

            # Conversation history'yi güncelle
            self.conversation_memory[session_id].append(
                {"role": "user", "content": user_message}
            )
            self.conversation_memory[session_id].append(
                {"role": "assistant", "content": bot_response}
            )

            # Son 10 mesajı tut (bellek yönetimi)
            if len(self.conversation_memory[session_id]) > 20:
                self.conversation_memory[session_id] = \
                    self.conversation_memory[session_id][-20:]

            return bot_response

        except Exception as e:
            print(f"OpenAI API hatası: {e}")
            return self._generate_fallback(user_message, target_word)

    def _generate_fallback(self, user_message: str, target_word: Optional[str]) -> str:
        """
        OpenAI olmadan basit cevaplar üretir.

        Args:
            user_message: Kullanıcı mesajı
            target_word: Hedef kelime

        Returns:
            str: Fallback cevap
        """
        if not target_word:
            return "Thank you for chatting! You've completed all the messages."

        templates = [
            f"That's interesting! Speaking of which, I think the word '{target_word}' is quite relevant here.",
            f"I understand your point. The concept of '{target_word}' comes to mind when I think about this.",
            f"Great question! Let me tell you something about '{target_word}' - it's an important concept.",
            f"I see what you mean. The word '{target_word}' perfectly describes this situation.",
            f"Thanks for sharing that! This reminds me of the word '{target_word}' and its meaning.",
            f"Interesting perspective! Have you ever thought about how '{target_word}' relates to this?"
        ]

        return random.choice(templates)

    def format_code_response(self, python_code: str, message_count: int) -> str:
        """
        Python kodunu formatlar ve kullanıcıya gösterir.

        Args:
            python_code: Admin panelden alınan Python kodu
            message_count: Kullanıcının mesaj sayısı

        Returns:
            str: Formatlanmış kod cevabı
        """
        response = f"Congratulations! You've sent {message_count} messages. Here's your Python code:\n\n"
        response += f"```python\n{python_code}\n```\n\n"
        response += "Thank you for chatting with me!"
        return response
