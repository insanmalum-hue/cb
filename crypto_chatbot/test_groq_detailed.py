"""
Detailed Groq API Test
"""

import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

print("=" * 60)
print("GROQ API DETAILED TEST")
print("=" * 60)

# Check API key
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

print(f"✓ API Key found: {api_key[:20]}...{api_key[-4:]}")
print(f"✓ API Key length: {len(api_key)}")
print()

# Try to import and initialize
try:
    from groq import Groq
    print("✓ Groq package imported")

    # Initialize client
    client = Groq(api_key=api_key)
    print("✓ Groq client initialized")
    print()

    # Test API call with detailed error
    print("Testing API call...")
    print("-" * 60)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated model (llama3-8b-8192 deprecated May 2025)
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Say hello!"
                }
            ],
            max_tokens=50,
            temperature=0.7
        )

        print("✅ SUCCESS!")
        print(f"Response: {response.choices[0].message.content}")
        print("=" * 60)

    except Exception as e:
        print("❌ API CALL FAILED!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()

        # Additional debugging
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            print(f"Response body: {e.response.text if hasattr(e.response, 'text') else 'N/A'}")

        print("=" * 60)

except ImportError as e:
    print(f"❌ Failed to import groq: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
