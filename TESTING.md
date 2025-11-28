# Testing Guide

This guide helps you test and verify the Vibe Coding AI Agent.

## Prerequisites

Before testing, ensure you have:
- ✅ Completed installation (see README.md)
- ✅ Created `.env` file with valid credentials
- ✅ Started Neo4j database
- ✅ Activated Python virtual environment

## Step 1: Backend Validation

Test that all dependencies are installed and configured correctly:

```bash
cd backend
python test_setup.py
```

**Expected Output:**
```
✓ PASS: Imports
✓ PASS: Configuration
✓ PASS: Database Clients
✓ PASS: Code Analysis
✓ PASS: Token Counter
```

**If any tests fail:**
- **Imports**: Run `pip install -r requirements.txt`
- **Configuration**: Check your `.env` file
- **Database Clients**: Make sure Neo4j is running
- **Code Analysis**: Verify tree-sitter installation
- **Token Counter**: Verify tiktoken installation

## Step 2: Start the Backend

```bash
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5001
```

**Access Points:**
- API: http://localhost:5001
- Interactive Docs: http://localhost:5001/docs
- Alternative Docs: http://localhost:5001/redoc

## Step 3: API Endpoint Testing

In a **new terminal** (keep backend running):

```bash
cd backend
python test_api.py
```

**Expected Output:**
```
✓ PASS: Health Check
✓ PASS: Index Stats
✓ PASS: File Listing
✓ PASS: Chat (needs indexing)
✓ PASS: Debug (needs indexing)
✓ PASS: Plan (needs indexing)
```

## Step 4: Index a Test Repository

Create a small test directory:

```bash
mkdir test_repo
cd test_repo
```

Create `hello.py`:
```python
def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

def main():
    print(greet("World"))

if __name__ == "__main__":
    main()
```

Index it:
```bash
curl -X POST http://localhost:5001/index/index \
  -H "Content-Type: application/json" \
  -d "{\"repository_path\": \"$(pwd)/test_repo\"}"
```

**Or using Python:**
```python
import requests
response = requests.post(
    "http://localhost:5001/index/index",
    json={"repository_path": "C:/path/to/test_repo"}
)
print(response.json())
```

## Step 5: Verify Indexing

Check index statistics:

```bash
curl http://localhost:5001/index/stats
```

**Expected Output:**
```json
{
  "metrics": {
    "files_indexed": 1,
    "asg_nodes": 2,
    "embeddings": 1,
    ...
  },
  "vector_store": {
    "total_embeddings": 1
  },
  "graph_store": {
    "code_nodes": 2,
    "cfg_nodes": 8
  }
}
```

## Step 6: Test Chat Functionality

Ask a question about your code:

```bash
curl -X POST http://localhost:5001/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the greet function do?"}'
```

**Expected:** JSON response with an answer about the greet function.

## Step 7: Test Debug Functionality

```bash
curl -X POST http://localhost:5001/ai/debug \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "hello.py",
    "error_message": "TypeError: greet() missing 1 required positional argument"
  }'
```

**Expected:** Analysis and fix suggestions.

## Step 8: Test Planning

```bash
curl -X POST http://localhost:5001/ai/plan \
  -H "Content-Type: application/json" \
  -d '{"goal": "Add error handling to the greet function"}'
```

**Expected:** Implementation plan with steps.

## Step 9: Frontend Testing

Start the frontend (in a new terminal):

```bash
cd frontend
npm run dev
```

Visit http://localhost:3000 and verify:
- ✅ File tree loads
- ✅ Can select and view files
- ✅ Can send chat messages
- ✅ Chat receives responses

## Step 10: Integration Testing

### Test Complete Workflow

1. **Index a larger repository** (e.g., your actual project)
2. **Ask complex questions**:
   - "Find all functions that use the database"
   - "What are the main entry points?"
   - "Explain the authentication flow"
3. **Test debug** with a real error from your codebase
4. **Generate a plan** for a real feature

## Performance Testing

### Indexing Performance

Index a repository and note:
- Files/second
- Total time
- Memory usage

**Typical Performance:**
- Small repos (10-50 files): 30-60 seconds
- Medium repos (100-500 files): 2-5 minutes
- Large repos (1000+ files): 10-30 minutes

### Query Performance

Test query response times:

```bash
time curl -X POST http://localhost:5001/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does main.py do?"}'
```

**Expected:**
- First query: 2-5 seconds (model loading)
- Subsequent queries: 1-2 seconds

## Troubleshooting

### Test Failures

**Q: test_setup.py fails on imports**
A: Run `pip install -r requirements.txt` again

**Q: Database connection fails**
A: Check Neo4j is running: `docker ps` or visit http://localhost:7474

**Q: API tests time out**
A: Ensure backend is running on port 5001

**Q: Chat returns errors**
A: 
1. Check Gemini API key in `.env`
2. Ensure codebase is indexed
3. Check backend logs for details

### Performance Issues

**Q: Indexing is very slow**
A:
- Check disk I/O (use SSD if possible)
- Reduce chunk size in config
- Check network (if using cloud Neo4j)

**Q: Queries are slow**
A:
- First query loads models (normal)
- Check Neo4j query performance
- Reduce number of chunks retrieved (k parameter)

## Success Criteria

Your system is working correctly if:

- ✅ All setup tests pass
- ✅ All API tests pass
- ✅ Can index a repository successfully
- ✅ Index stats show correct counts
- ✅ Chat provides relevant answers
- ✅ Debug provides fix suggestions
- ✅ Planning generates structured plans
- ✅ Frontend connects and displays data
- ✅ No errors in backend logs

## Next Steps

Once all tests pass:
1. Index your actual codebase
2. Try complex queries
3. Test with team members
4. Monitor performance
5. Adjust configuration as needed

## Getting Help

If tests continue to fail:
1. Check backend logs for detailed errors
2. Verify all prerequisites are met
3. Review the troubleshooting sections in README.md
4. Ensure all services (Neo4j, backend, frontend) are running
