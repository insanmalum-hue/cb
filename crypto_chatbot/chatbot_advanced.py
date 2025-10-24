"""
Advanced Chatbot Engine with Multiple FREE AI API Support

Supported APIs (Priority Order):
1. Groq API - Ultra Fast (300+ tokens/sec) - FREE
2. Hugging Face - Free Tier (1000 req/hour)
3. Together AI - Free $25 credit
4. Cohere - Free Tier
5. Fallback Mode - No API needed

Author: Claude Code
"""

import os
import requests
import random
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class AdvancedChatbot:
    """
    Multi-API Chatbot Engine with automatic fallback
    """

    def __init__(self):
        # API Keys
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.hf_key = os.getenv('HUGGINGFACE_API_KEY')
        self.together_key = os.getenv('TOGETHER_API_KEY')
        self.cohere_key = os.getenv('COHERE_API_KEY')

        # Select best available API
        self.active_api = self._select_best_api()
        self.conversation_memory = {}

        print(f"✓ Advanced Chatbot Initialized")
        print(f"✓ Active AI Provider: {self.active_api.upper()}")

        if self.active_api == 'fallback':
            print("⚠️  No API keys found - Running in fallback mode")
            print("💡 Add API keys to .env for AI-powered responses")

    def _select_best_api(self):
        """Select the best available API based on priority"""
        if self.groq_key:
            return 'groq'
        elif self.hf_key:
            return 'huggingface'
        elif self.together_key:
            return 'together'
        elif self.cohere_key:
            return 'cohere'
        else:
            return 'fallback'

    def generate_response(self, user_message: str, target_word: Optional[str],
                         session_id: str) -> str:
        """
        Generate response using active API with automatic fallback

        Args:
            user_message: User's message
            target_word: Word to include in response
            session_id: Session identifier

        Returns:
            AI-generated response
        """

        # Prepare messages
        messages = self._prepare_messages(user_message, target_word, session_id)

        # Try all available APIs in priority order
        api_methods = []

        if self.groq_key:
            api_methods.append(('groq', self._generate_with_groq))
        if self.hf_key:
            api_methods.append(('huggingface', self._generate_with_huggingface))
        if self.together_key:
            api_methods.append(('together', self._generate_with_together))
        if self.cohere_key:
            api_methods.append(('cohere', self._generate_with_cohere))

        # Try each API
        for api_name, api_method in api_methods:
            try:
                response = api_method(messages)

                # Update conversation memory
                self._update_memory(session_id, user_message, response)

                # Log which API succeeded
                if api_name != self.active_api:
                    print(f"✓ {api_name.upper()} API succeeded (fallback from {self.active_api.upper()})")

                return response

            except Exception as e:
                print(f"⚠️  {api_name.upper()} API Error: {e}")
                if api_name == api_methods[-1][0]:  # Last API
                    print("↪️  All APIs failed. Falling back to basic responses...")
                else:
                    print(f"↪️  Trying next API...")
                continue

        # If all APIs failed, use fallback
        return self._generate_fallback(user_message, target_word)

    def _prepare_messages(self, user_message: str, target_word: Optional[str],
                         session_id: str) -> list:
        """Prepare message history for API"""

        # Get conversation history
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []

        history = self.conversation_memory[session_id][-10:]  # Last 10 messages

        # System prompt
        system_prompt = "You are a helpful and friendly assistant."
        if target_word:
            system_prompt += f" IMPORTANT: You must naturally include the word '{target_word}' in your response."

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        return messages

    def _generate_with_groq(self, messages: list) -> str:
        """
        Generate with Groq API (FASTEST - 300+ tokens/sec)

        Free Tier: Very high limits
        Model: llama3-8b-8192
        """

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 150,
            "top_p": 0.9
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content'].strip()

    def _generate_with_huggingface(self, messages: list) -> str:
        """
        Generate with Hugging Face Inference API

        Free Tier: 1000 requests/hour
        Model: mistralai/Mistral-7B-Instruct-v0.2
        """

        url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {
            "Authorization": f"Bearer {self.hf_key}",
            "Content-Type": "application/json"
        }

        # Convert messages to single prompt
        prompt = self._format_messages_to_prompt(messages)

        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.8,
                "top_p": 0.9,
                "return_full_text": False
            }
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]['generated_text'].strip()
        return str(result)

    def _generate_with_together(self, messages: list) -> str:
        """
        Generate with Together AI

        Free Credit: $25
        Model: meta-llama/Llama-3-8b-chat-hf
        """

        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.together_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 150
        }

        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content'].strip()

    def _generate_with_cohere(self, messages: list) -> str:
        """
        Generate with Cohere API

        Free Tier: Available
        Model: command-light
        """

        url = "https://api.cohere.ai/v1/generate"
        headers = {
            "Authorization": f"Bearer {self.cohere_key}",
            "Content-Type": "application/json"
        }

        # Convert messages to prompt
        prompt = self._format_messages_to_prompt(messages)

        data = {
            "model": "command-light",
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.8
        }

        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()

        return response.json()['generations'][0]['text'].strip()

    def _generate_fallback(self, user_message: str, target_word: Optional[str]) -> str:
        """Fallback response when no API is available"""

        if not target_word:
            return "Thank you for chatting! You've completed all 36 messages."

        templates = [
            f"That's interesting! Speaking of which, I think the word '{target_word}' is quite relevant here.",
            f"I understand your point. The concept of '{target_word}' comes to mind when I think about this.",
            f"Great question! Let me tell you something about '{target_word}' - it's an important concept.",
            f"I see what you mean. The word '{target_word}' perfectly describes this situation.",
            f"Thanks for sharing that! This reminds me of the word '{target_word}' and its meaning.",
            f"Interesting perspective! Have you ever thought about how '{target_word}' relates to this?"
        ]

        return random.choice(templates)

    def _format_messages_to_prompt(self, messages: list) -> str:
        """Convert message history to single prompt string"""

        prompt_parts = []
        for msg in messages:
            role = msg['role']
            content = msg['content']

            if role == 'system':
                prompt_parts.append(f"Instructions: {content}\n")
            elif role == 'user':
                prompt_parts.append(f"User: {content}\n")
            elif role == 'assistant':
                prompt_parts.append(f"Assistant: {content}\n")

        prompt_parts.append("Assistant: ")
        return "".join(prompt_parts)

    def _update_memory(self, session_id: str, user_message: str,
                      bot_response: str):
        """Update conversation memory"""

        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []

        self.conversation_memory[session_id].append({
            "role": "user",
            "content": user_message
        })

        self.conversation_memory[session_id].append({
            "role": "assistant",
            "content": bot_response
        })

        # Keep only last 20 messages (10 exchanges)
        if len(self.conversation_memory[session_id]) > 20:
            self.conversation_memory[session_id] = \
                self.conversation_memory[session_id][-20:]

    def get_target_word(self, message_count: int) -> Optional[str]:
        """Get target word for current message count"""

        WORDS = [
            "pilot", "giant", "enable", "syrup", "medal", "hero", "iron", "soap",
            "visual", "vendor", "genuine", "punch", "grid", "floor", "glide", "penalty",
            "blossom", "crew", "pival", "sheriff", "solar", "claw", "oak", "find",
            "bind", "pet", "urban", "else", "series", "wave", "pumpkin", "amount",
            "verb", "similar", "crime", "bird"
        ]

        if 0 <= message_count < 36:
            return WORDS[message_count]
        return None

    def is_code_request(self, message: str) -> bool:
        """Check if user is requesting code"""

        import re
        patterns = [
            r'\bshow\s+code\b',
            r'\bgive\s+code\b',
            r'\bgive.*code\b',
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

    def format_code_response(self, python_code: str, message_count: int) -> str:
        """Format code response"""

        response = f"Congratulations! You've sent {message_count} messages. Here's your Python code:\n\n"
        response += f"```python\n{python_code}\n```\n\n"
        response += "Thank you for chatting with me!"
        return response


# Test function
if __name__ == "__main__":
    print("Testing Advanced Chatbot Engine...")
    bot = AdvancedChatbot()

    # Test response
    test_response = bot.generate_response(
        user_message="Hello, how are you?",
        target_word="pilot",
        session_id="test-session-123"
    )

    print(f"\nTest Response: {test_response}")
    print("\n✓ Advanced Chatbot Engine is ready!")
