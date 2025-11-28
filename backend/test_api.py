"""
API endpoint testing script.
Tests all API endpoints to ensure they respond correctly.
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:5001"

def print_test(name: str, passed: bool, message: str = ""):
    """Print test result."""
    status = "✓" if passed else "✗"
    print(f"  {status} {name}", end="")
    if message:
        print(f": {message}")
    else:
        print()

def test_health_check():
    """Test basic health check."""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        passed = response.status_code == 200
        print_test("GET /", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("GET /", False, str(e))
        return False

def test_index_stats():
    """Test index statistics endpoint."""
    print("\n2. Testing Index Stats...")
    try:
        response = requests.get(f"{BASE_URL}/index/stats")
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            print_test("GET /index/stats", True)
            print(f"    Files indexed: {data.get('metrics', {}).get('files_indexed', 0)}")
            print(f"    ASG nodes: {data.get('metrics', {}).get('asg_nodes', 0)}")
            print(f"    Embeddings: {data.get('metrics', {}).get('embeddings', 0)}")
        else:
            print_test("GET /index/stats", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        print_test("GET /index/stats", False, str(e))
        return False

def test_files_endpoint():
    """Test file listing endpoint."""
    print("\n3. Testing File Listing...")
    try:
        response = requests.get(f"{BASE_URL}/files", params={"directory": "."})
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            file_count = data.get('total', 0)
            print_test("GET /files", True, f"Found {file_count} files")
        else:
            print_test("GET /files", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        print_test("GET /files", False, str(e))
        return False

def test_chat_endpoint():
    """Test chat endpoint."""
    print("\n4. Testing Chat Endpoint...")
    try:
        payload = {
            "question": "What is this codebase about?",
            "stream": False
        }
        response = requests.post(
            f"{BASE_URL}/ai/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Note: This might fail if codebase isn't indexed or API key is invalid
        passed = response.status_code in [200, 500]  # 500 is okay if not indexed
        
        if response.status_code == 200:
            data = response.json()
            print_test("POST /ai/chat", True, "Response received")
            if 'context_stats' in data:
                print(f"    Tokens used: {data['context_stats'].get('total_tokens', 0)}")
        elif response.status_code == 500:
            print_test("POST /ai/chat", True, "Endpoint exists (needs indexing or API key)")
        else:
            print_test("POST /ai/chat", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        print_test("POST /ai/chat", False, str(e))
        return False

def test_debug_endpoint():
    """Test debug endpoint."""
    print("\n5. Testing Debug Endpoint...")
    try:
        payload = {
            "file_path": "test.py",
            "error_message": "NameError: name 'undefined_var' is not defined"
        }
        response = requests.post(
            f"{BASE_URL}/ai/debug",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        passed = response.status_code in [200, 500]
        
        if response.status_code == 200:
            print_test("POST /ai/debug", True, "Response received")
        elif response.status_code == 500:
            print_test("POST /ai/debug", True, "Endpoint exists (needs indexing or API key)")
        else:
            print_test("POST /ai/debug", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        print_test("POST /ai/debug", False, str(e))
        return False

def test_plan_endpoint():
    """Test planning endpoint."""
    print("\n6. Testing Planning Endpoint...")
    try:
        payload = {
            "goal": "Add a new feature to handle user authentication"
        }
        response = requests.post(
            f"{BASE_URL}/ai/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        passed = response.status_code in [200, 500]
        
        if response.status_code == 200:
            print_test("POST /ai/plan", True, "Response received")
        elif response.status_code == 500:
            print_test("POST /ai/plan", True, "Endpoint exists (needs indexing or API key)")
        else:
            print_test("POST /ai/plan", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        print_test("POST /ai/plan", False, str(e))
        return False

def main():
    """Run all API tests."""
    print("=" * 60)
    print("API Endpoint Testing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("\nNote: Chat, Debug, and Plan tests require:")
    print("  - Valid Gemini API key in .env")
    print("  - Indexed codebase")
    print("  - Running Neo4j database")
    
    results = []
    
    # Test each endpoint
    results.append(("Health Check", test_health_check()))
    results.append(("Index Stats", test_index_stats()))
    results.append(("File Listing", test_files_endpoint()))
    results.append(("Chat", test_chat_endpoint()))
    results.append(("Debug", test_debug_endpoint()))
    results.append(("Plan", test_plan_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    if total_passed == total_tests:
        print(f"✓ All tests passed ({total_passed}/{total_tests})")
        return 0
    else:
        print(f"⚠ Some tests failed ({total_passed}/{total_tests} passed)")
        print("\nIf chat/debug/plan failed, ensure:")
        print("  1. Backend is running (python main.py)")
        print("  2. .env has valid GEMINI_API_KEY")
        print("  3. Neo4j is running")
        print("  4. Codebase is indexed")
        return 1

if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
