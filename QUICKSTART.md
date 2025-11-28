# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.11 or higher installed
- [ ] Node.js 18 or higher installed  
- [ ] Docker (optional, for Neo4j)
- [ ] Gemini API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 5-Minute Setup

### Step 1: Configure Environment

```bash
# Create .env file from template
cd backend
cp .env.example .env

# Edit .env and add your configuration:
# - GEMINI_API_KEY=your_key_here
# - GRAPH_DB_PASSWORD=choose_a_password
# - REPOSITORY_PATH=C:/path/to/your/repo (optional, for auto-indexing)
```

### Step 2: Start Neo4j Database

**Using Docker (Recommended):**
```bash
docker run -d \
  --name vibe-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password_from_env \
  neo4j:latest
```

Verify at: http://localhost:7474 (Neo4j Browser)

### Step 3: Install Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Step 4: Install Frontend

```bash
cd frontend
npm install
```

### Step 5: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```
→ http://localhost:5001

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
→ http://localhost:3000

## First Usage

### Index Your Codebase

**Method 1: Auto-Index on Startup (Recommended)**

The easiest way is to configure your repository path in the `.env` file:

```bash
# Edit backend/.env and add:
REPOSITORY_PATH=C:/path/to/your/repo
```

Then restart the backend server - it will automatically index your codebase on startup!

**Method 2: Manual Indexing via API**

If you prefer manual control, you can trigger indexing via the API:

```bash
curl -X POST http://localhost:5001/index/index \
  -H "Content-Type: application/json" \
  -d "{\"repository_path\": \"C:/path/to/your/repo\"}"
```

Or via Python:
```python
import requests

response = requests.post(
    "http://localhost:5001/index/index",
    json={"repository_path": "C:/path/to/your/repo"}
)
print(response.json())
```

### Check Indexing Progress

```bash
curl http://localhost:5001/index/stats
```

### Start Chatting

1. Open http://localhost:3000
2. Browse files in the left panel
3. Ask questions in the chat panel:
   - "What does the main function do?"
   - "Find all functions that call process_data"
   - "Explain the authentication flow"

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Verify all dependencies installed: `pip list`
- Check Neo4j is running: http://localhost:7474

### Frontend won't connect
- Ensure backend is running on port 5001
- Check browser console for errors
- Verify CORS settings in backend/main.py

### Neo4j connection error
- Verify Neo4j is running: `docker ps`
- Check password matches .env file
- Test connection: http://localhost:7474

### Gemini API errors
- Verify API key is valid
- Check you have access to Gemini 2.5 Flash
- Monitor rate limits

## API Endpoints

Once running, explore the interactive API docs:
- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

## File Locations

- **Configuration**: `.env`
- **Vector DB**: `./data/vector_db/`
- **Backend logs**: Console output
- **Frontend**: http://localhost:3000

## Next Steps

1. ✅ Index a small test repository
2. ✅ Ask simple questions
3. ✅ Test the debug feature
4. ✅ Generate an implementation plan
5. ✅ Scale to larger repositories

## Support

For detailed documentation, see the main README.md file.
