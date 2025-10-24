"""
System Tests for Crypto Chatbot

This test suite verifies the core functionality of the chatbot system.
Run with: python test_system.py
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotEngine, WORDS


def test_words():
    """Test that the WORDS list contains exactly 36 unique words"""
    print("\n" + "="*60)
    print("TEST 1: Word List Validation")
    print("="*60)

    # Check count
    if len(WORDS) != 36:
        print(f"❌ FAIL: Expected 36 words, found {len(WORDS)}")
        return False
    print(f"✓ Word count: {len(WORDS)}")

    # Check uniqueness
    unique_words = set(WORDS)
    if len(unique_words) != 36:
        duplicates = len(WORDS) - len(unique_words)
        print(f"❌ FAIL: Found {duplicates} duplicate words")
        return False
    print(f"✓ All words are unique")

    # Check that all are strings
    if not all(isinstance(word, str) for word in WORDS):
        print("❌ FAIL: Not all words are strings")
        return False
    print(f"✓ All words are strings")

    # Check that all are lowercase
    if not all(word.islower() for word in WORDS):
        print("❌ FAIL: Not all words are lowercase")
        return False
    print(f"✓ All words are lowercase")

    # Display the word list
    print(f"\nWord List:")
    for i in range(0, 36, 6):
        words_line = ", ".join(WORDS[i:i+6])
        print(f"  {i+1:2d}-{i+6:2d}: {words_line}")

    print("\n✅ PASS: Word list validation successful")
    return True


def test_chatbot_engine():
    """Test ChatbotEngine initialization and basic functionality"""
    print("\n" + "="*60)
    print("TEST 2: ChatbotEngine Initialization")
    print("="*60)

    try:
        # Initialize engine
        engine = ChatbotEngine()
        print("✓ ChatbotEngine initialized")

        # Check attributes
        if not hasattr(engine, 'client'):
            print("❌ FAIL: Missing 'client' attribute")
            return False
        print("✓ Has 'client' attribute")

        if not hasattr(engine, 'conversation_memory'):
            print("❌ FAIL: Missing 'conversation_memory' attribute")
            return False
        print("✓ Has 'conversation_memory' attribute")

        # Check conversation_memory is a dict
        if not isinstance(engine.conversation_memory, dict):
            print("❌ FAIL: conversation_memory is not a dictionary")
            return False
        print("✓ conversation_memory is a dictionary")

        # Check initial state
        if len(engine.conversation_memory) != 0:
            print("❌ FAIL: conversation_memory should be empty initially")
            return False
        print("✓ conversation_memory is empty initially")

        print("\n✅ PASS: ChatbotEngine initialization successful")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception during initialization: {e}")
        return False


def test_code_request_detection():
    """Test code request pattern matching"""
    print("\n" + "="*60)
    print("TEST 3: Code Request Detection")
    print("="*60)

    try:
        engine = ChatbotEngine()

        # Test cases: (message, expected_result)
        test_cases = [
            ("show code", True),
            ("Show Code", True),
            ("SHOW CODE", True),
            ("please show code", True),
            ("can you show code?", True),
            ("give code", True),
            ("give me the code", True),
            ("kod yaz", True),
            ("kod ver", True),
            ("kodu göster", True),
            ("get code", True),
            ("hello", False),
            ("how are you", False),
            ("tell me about yourself", False),
            ("code word in sentence", False),  # Just contains word "code"
        ]

        passed = 0
        failed = 0

        for message, expected in test_cases:
            result = engine.is_code_request(message)
            if result == expected:
                print(f"✓ '{message}' -> {result} (expected {expected})")
                passed += 1
            else:
                print(f"❌ '{message}' -> {result} (expected {expected})")
                failed += 1

        print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")

        if failed == 0:
            print("\n✅ PASS: Code request detection working correctly")
            return True
        else:
            print("\n❌ FAIL: Some code request detection tests failed")
            return False

    except Exception as e:
        print(f"❌ FAIL: Exception during testing: {e}")
        return False


def test_get_target_word():
    """Test target word retrieval"""
    print("\n" + "="*60)
    print("TEST 4: Target Word Retrieval")
    print("="*60)

    try:
        engine = ChatbotEngine()

        # Test valid indices
        for i in range(36):
            word = engine.get_target_word(i)
            expected = WORDS[i]
            if word != expected:
                print(f"❌ FAIL: Message {i} returned '{word}', expected '{expected}'")
                return False
        print(f"✓ All 36 words retrieved correctly (0-35)")

        # Test out of range (should return None)
        for i in [36, 37, 100]:
            word = engine.get_target_word(i)
            if word is not None:
                print(f"❌ FAIL: Message {i} returned '{word}', expected None")
                return False
        print(f"✓ Out of range indices return None")

        # Test negative index
        word = engine.get_target_word(-1)
        if word is None:
            print(f"✓ Negative index returns None")
        else:
            print(f"❌ FAIL: Negative index returned '{word}', expected None")
            return False

        print("\n✅ PASS: Target word retrieval working correctly")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception during testing: {e}")
        return False


def test_fallback_responses():
    """Test fallback response generation"""
    print("\n" + "="*60)
    print("TEST 5: Fallback Response Generation")
    print("="*60)

    try:
        engine = ChatbotEngine()

        # Test with different words
        test_words = ["pilot", "giant", "enable", "syrup", "medal"]

        for word in test_words:
            response = engine._generate_fallback("Hello", word)

            # Check response is not empty
            if not response:
                print(f"❌ FAIL: Empty response for word '{word}'")
                return False

            # Check word is in response
            if word.lower() not in response.lower():
                print(f"❌ FAIL: Word '{word}' not found in response: {response}")
                return False

            print(f"✓ Word '{word}' included in response")

        # Test with None (completed sequence)
        response = engine._generate_fallback("Hello", None)
        if "completed" not in response.lower() or "36" not in response:
            print(f"❌ FAIL: Completion message incorrect: {response}")
            return False
        print(f"✓ Completion message correct")

        print("\n✅ PASS: Fallback response generation working correctly")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception during testing: {e}")
        return False


def test_format_code_response():
    """Test code response formatting"""
    print("\n" + "="*60)
    print("TEST 6: Code Response Formatting")
    print("="*60)

    try:
        engine = ChatbotEngine()

        test_code = "print('Hello World')\nprint('Test code')"
        message_count = 36

        response = engine.format_code_response(test_code, message_count)

        # Check response contains key elements
        checks = [
            ("Congratulations" in response, "Contains 'Congratulations'"),
            (str(message_count) in response, "Contains message count"),
            ("```python" in response, "Contains Python code block start"),
            ("```" in response, "Contains code block end"),
            (test_code in response, "Contains the actual code"),
        ]

        all_passed = True
        for check, description in checks:
            if check:
                print(f"✓ {description}")
            else:
                print(f"❌ {description}")
                all_passed = False

        if all_passed:
            print("\n✅ PASS: Code response formatting working correctly")
            return True
        else:
            print("\n❌ FAIL: Some formatting checks failed")
            return False

    except Exception as e:
        print(f"❌ FAIL: Exception during testing: {e}")
        return False


def run_all_tests():
    """Run all system tests"""
    print("\n" + "="*60)
    print("CRYPTO CHATBOT SYSTEM TESTS")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    tests = [
        ("Word List Validation", test_words),
        ("ChatbotEngine Initialization", test_chatbot_engine),
        ("Code Request Detection", test_code_request_detection),
        ("Target Word Retrieval", test_get_target_word),
        ("Fallback Response Generation", test_fallback_responses),
        ("Code Response Formatting", test_format_code_response),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ FATAL ERROR in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("-"*60)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
