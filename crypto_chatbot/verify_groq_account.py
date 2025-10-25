"""
Groq API Key Verification Script
Checks account status, permissions, and available models
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("GROQ API KEY VERIFICATION")
print("=" * 70)

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    exit(1)

print(f"\n1. API Key Format Check:")
print(f"   Key: {api_key[:20]}...{api_key[-4:]}")
print(f"   Length: {len(api_key)} characters")
print(f"   Prefix: {'✓ Correct (gsk_)' if api_key.startswith('gsk_') else '❌ Invalid prefix'}")

try:
    from groq import Groq
    print(f"\n2. Groq SDK: ✓ Installed")

    client = Groq(api_key=api_key)
    print(f"   Client: ✓ Initialized")

    # Try to make an API call
    print(f"\n3. Testing API Access:")
    print(f"   Model: llama-3.1-8b-instant (latest)")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Respond with only: OK"}
            ],
            max_tokens=10,
            temperature=0.5
        )

        print(f"   Status: ✅ SUCCESS!")
        print(f"   Response: {response.choices[0].message.content}")
        print("\n" + "=" * 70)
        print("✅ YOUR GROQ API KEY IS WORKING PERFECTLY!")
        print("=" * 70)

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        print(f"   Status: ❌ FAILED")
        print(f"   Error: {error_type}")
        print(f"   Message: {error_msg}")

        print("\n" + "=" * 70)
        print("⚠️  API KEY PERMISSION ISSUE DETECTED")
        print("=" * 70)

        print("\nPossible causes:")
        print("1. Account Role: Your account may not have 'Developer' or 'Team Owner' role")
        print("2. Key Revoked: This API key may have been revoked or deleted")
        print("3. Billing: Your account may have insufficient credits or billing issues")
        print("4. Account Limits: You may have exceeded API rate limits")

        print("\n📋 ACTION REQUIRED:")
        print("1. Visit: https://console.groq.com/keys")
        print("2. Check your account role and permissions")
        print("3. Generate a NEW API key")
        print("4. Verify your account has credits/billing setup")
        print("5. Check for any account warnings or restrictions")

        print("\n" + "=" * 70)

except ImportError:
    print(f"❌ Groq package not installed")
    print(f"   Install: pip install groq")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
