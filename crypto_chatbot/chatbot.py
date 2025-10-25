"""
Advanced Chatbot with Groq AI Integration
"""

import os
from groq import Groq

class AdvancedChatbot:
    def __init__(self):
        # 36 kelime
        self.words = [
            "pilot", "giant", "enable", "syrup", "medal", "hero", "iron", "soap",
            "visual", "vendor", "genuine", "punch", "grid", "floor", "glide", "penalty",
            "blossom", "crew", "pival", "sheriff", "solar", "claw", "oak", "find",
            "bind", "pet", "urban", "else", "series", "wave", "pumpkin", "amount",
            "verb", "similar", "crime", "bird"
        ]

        # Groq client
        self.groq_available = False
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.client = Groq(api_key=api_key)
                self.groq_available = True
                print("✓ Groq AI initialized")
            else:
                print("⚠ GROQ_API_KEY not found - using fallback mode")
        except Exception as e:
            print(f"⚠ Groq initialization failed: {e}")

    def get_target_word(self, message_count):
        """Get word for current message"""
        if message_count >= 36:
            return None
        return self.words[message_count]

    def generate_response(self, user_message, message_count, conversation_history=None):
        """Generate AI response with target word"""

        target_word = self.get_target_word(message_count)

        if not target_word:
            return "Sequence complete! Type 'show code' to get your code."

        # Use Groq AI if available
        if self.groq_available:
            try:
                return self._generate_with_groq(user_message, target_word, conversation_history)
            except Exception as e:
                print(f"Groq error: {e}")
                # Fallback
                return self._generate_fallback(target_word)
        else:
            return self._generate_fallback(target_word)

    def _generate_with_groq(self, user_message, target_word, conversation_history):
        """Generate response using Groq AI"""

        # Build messages
        messages = [
            {
                "role": "system",
                "content": f"""You are a friendly, conversational AI assistant.

CRITICAL RULES:
1. You MUST naturally include the word "{target_word}" in your response
2. Keep responses conversational and engaging (2-3 sentences)
3. Answer the user's question while naturally using the word
4. Make it feel like a real conversation
5. Don't mention you're using a specific word
6. Be helpful and relevant to what the user asked

Examples:
User: "How are you?" → "I'm doing great! Just like a pilot navigating through the day smoothly. How about you?"
User: "Tell me about technology" → "Technology is giant in its impact on our lives! It's transforming how we work and communicate."

Now respond to the user naturally while including the word "{target_word}"."""
            }
        ]

        # Add conversation history (last 3 exchanges)
        if conversation_history:
            import json
            try:
                history = json.loads(conversation_history) if isinstance(conversation_history, str) else conversation_history
                for msg in history[-6:]:  # Last 3 exchanges (6 messages)
                    messages.append({
                        "role": "user" if msg.get('type') == 'user' else "assistant",
                        "content": msg.get('content', '')
                    })
            except:
                pass

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Groq API
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.8,
            max_tokens=150,
            top_p=0.9
        )

        bot_response = response.choices[0].message.content

        # Verify word is included (case-insensitive)
        if target_word.lower() not in bot_response.lower():
            # Add word naturally if missing
            bot_response += f" Speaking of which, {target_word} is quite relevant here!"

        return bot_response

    def _generate_fallback(self, target_word):
        """Fallback response if AI not available"""
        import random

        responses = [
            f"Great question! Let me tell you something about '{target_word}' - it's an important concept.",
            f"Interesting! The word '{target_word}' reminds me of something fascinating.",
            f"I love discussing this! '{target_word}' plays a key role in many areas.",
            f"That's a good point! Speaking of which, '{target_word}' is quite relevant here.",
            f"Thanks for asking! The concept of '{target_word}' is worth exploring."
        ]

        return random.choice(responses)

# Global chatbot instance
chatbot = AdvancedChatbot()
