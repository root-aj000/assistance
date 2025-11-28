"""
Test script for validating the Vibe Coding AI Agent backend.
Run this after setting up your environment to verify everything works.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    tests = [
        ("FastAPI", lambda: __import__('fastapi')),
        ("Pydantic", lambda: __import__('pydantic')),
        ("Google GenAI", lambda: __import__('google.generativeai')),
        ("FAISS", lambda: __import__('faiss')),
        ("Neo4j", lambda: __import__('neo4j')),
        ("Tree-sitter", lambda: __import__('tree_sitter')),
        ("Tiktoken", lambda: __import__('tiktoken')),
        ("NumPy", lambda: __import__('numpy')),
    ]
    
    passed = 0
    failed = 0
    
    for name, import_func in tests:
        try:
            import_func()
            print(f"  ✓ {name}")
            passed += 1
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print(f"\nImport tests: {passed} passed, {failed} failed\n")
    return failed == 0

def test_configuration():
    """Test that configuration loads correctly."""
    print("Testing configuration...")
    
    try:
        from config import settings
        
        # Check required settings
        checks = [
            ("Gemini API Key", bool(settings.gemini_api_key)),
            ("Vector DB Path", bool(settings.vector_db_path)),
            ("Graph DB URL", bool(settings.graph_db_url)),
            ("Max Tokens", settings.max_tokens_per_request > 0),
        ]
        
        for name, result in checks:
            status = "✓" if result else "✗"
            print(f"  {status} {name}")
        
        print("\n")
        return all(result for _, result in checks)
    except Exception as e:
        print(f"  ✗ Configuration error: {e}\n")
        return False

def test_database_clients():
    """Test database client initialization."""
    print("Testing database clients...")
    
    try:
        from db.vector_store import VectorStore
        from config import settings
        
        # Test vector store
        vector_store = VectorStore(settings.vector_db_path, dimension=768)
        stats = vector_store.get_stats()
        print(f"  ✓ Vector Store initialized (embeddings: {stats['total_embeddings']})")
        
    except Exception as e:
        print(f"  ✗ Vector Store error: {e}")
        return False
    
    try:
        from db.graph_store import GraphStore
        
        # Test graph store (this will fail if Neo4j isn't running)
        graph_store = GraphStore(
            uri=settings.graph_db_url,
            user=settings.graph_db_user,
            password=settings.graph_db_password
        )
        stats = graph_store.get_stats()
        print(f"  ✓ Graph Store connected (nodes: {stats['code_nodes']})")
        graph_store.close()
        
    except Exception as e:
        print(f"  ✗ Graph Store error: {e}")
        print(f"    (Make sure Neo4j is running at {settings.graph_db_url})")
        return False
    
    print("\n")
    return True

def test_code_analysis():
    """Test code analysis components."""
    print("Testing code analysis...")
    
    try:
        from analysis.tree_sitter_parser import parser
        from analysis.chunker import chunker
        
        # Test Python parsing
        test_code = """
def hello_world():
    print("Hello, World!")
    return 42
"""
        tree = parser.parse_file("test.py", test_code)
        if tree:
            print("  ✓ Tree-sitter Python parsing")
        else:
            print("  ✗ Tree-sitter parsing failed")
            return False
        
        # Test chunking
        chunks = chunker.chunk_file("test.py", test_code)
        print(f"  ✓ Code chunking ({len(chunks)} chunks)")
        
    except Exception as e:
        print(f"  ✗ Code analysis error: {e}")
        return False
    
    print("\n")
    return True

def test_token_counter():
    """Test token counting."""
    print("Testing token counter...")
    
    try:
        from llm.token_counter import token_counter
        
        test_text = "Hello, world! This is a test."
        tokens = token_counter.count_tokens(test_text)
        print(f"  ✓ Token counting ('{test_text}' = {tokens} tokens)")
        
    except Exception as e:
        print(f"  ✗ Token counter error: {e}")
        return False
    
    print("\n")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Vibe Coding AI Agent - Backend Validation")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("Database Clients", test_database_clients()))
    results.append(("Code Analysis", test_code_analysis()))
    results.append(("Token Counter", test_token_counter()))
    
    print("=" * 60)
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
        print(f"✗ Some tests failed ({total_passed}/{total_tests} passed)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
