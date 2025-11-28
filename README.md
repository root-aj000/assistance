# Vibe Coding AI Agent

An AI-powered desktop assistant that deeply understands large Python/TypeScript codebases through Abstract Semantic Graph (ASG) and Control Flow Graph (CFG) analysis, combined with vector embeddings for intelligent code interaction, debugging, and planning.

## Features

- 🧠 **Deep Code Understanding**: Analyzes codebases using ASG (semantic relationships) and CFG (execution flows)
- 🔍 **Hybrid Search**: Combines vector similarity and graph traversal for precise code retrieval
- 💬 **Interactive Chat**: Ask questions about your codebase and get context-aware answers
- 🐛 **Intelligent Debugging**: Analyzes errors and suggests fixes based on code context
- 📋 **Task Planning**: Generates implementation plans for new features or changes
- 🗄️ **Local-First**: All data stored locally using FAISS (vectors) and Neo4j (graphs)
- ⚡ **Token-Aware**: Respects 70k token limit with smart context packing
- 📊 **Metrics & Coverage**: Track indexing progress and code coverage

## Architecture

```
┌─────────────┐
│  Frontend   │  Next.js 14 + TypeScript
│  (Port 3000)│  - File Tree
└──────┬──────┘  - Code Viewer
       │         - Chat Interface
       │
       ▼
┌─────────────┐
│   FastAPI   │  Backend (Port 5001)
│   Server    │  - API Endpoints
└──────┬──────┘  - LLM Integration
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ FAISS DB │   │  Neo4j   │   │  Gemini  │   │  Tree-   │
│ (Vector) │   │ (Graph)  │   │   API    │   │  sitter  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Neo4j** (Community Edition or Docker)
- **Gemini API Key** (Google AI Studio)

## Installation

### 1. Clone and Setup

```bash
cd u:\Assistance
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Database Setup

#### Neo4j Setup

**Option A: Docker** (Recommended)
```bash
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/your_password \
    -v neo4j_data:/data \
    neo4j:latest
```

**Option B: Local Installation**
- Download from https://neo4j.com/download/
- Install and start Neo4j
- Set password via Neo4j Browser (http://localhost:7474)

### 5. Configuration

Create `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Gemini API
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Neo4j (adjust if using different credentials)
GRAPH_DB_PASSWORD=your_neo4j_password_here

# Other settings are pre-configured
```

## Usage

### 1. Start Backend

```bash
cd backend
python main.py
```

Backend will run at: http://localhost:5001

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:3000

### 3. Index Your Codebase

Before using the AI assistant, you need to index your codebase:

**Via API:**
```bash
curl -X POST http://localhost:5001/index/index \
  -H "Content-Type: application/json" \
  -d '{"repository_path": "/path/to/your/repo"}'
```

**Via Frontend:**
- Navigate to the indexing section
- Enter your repository path
- Click "Index Repository"

### 4. Start Chatting!

- Ask questions about your code
- Debug errors
- Generate implementation plans
- Explore code relationships

## API Endpoints

### Chat
- `POST /ai/chat` - Chat with codebase
- `POST /ai/codebase/chat` - Chat with specific files

### Debug
- `POST /ai/debug` - Analyze and fix code errors

### Planning
- `POST /ai/plan` - Generate implementation plans

### Files
- `GET /files?directory=/path` - List repository files
- `GET /file?file_path=/path/to/file` - Get file content

### Index
- `GET /index/stats` - Get indexing statistics
- `POST /index/index` - Trigger repository indexing

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | Required | Gemini API key |
| `VECTOR_DB_PATH` | `./data/vector_db` | FAISS database path |
| `GRAPH_DB_URL` | `bolt://localhost:7687` | Neo4j connection URL |
| `GRAPH_DB_USER` | `neo4j` | Neo4j username |
| `GRAPH_DB_PASSWORD` | Required | Neo4j password |
| `MAX_TOKENS_PER_REQUEST` | `70000` | Maximum tokens per LLM request |
| `CHUNK_SIZE_TOKENS` | `400` | Code chunk size in tokens |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |

## How It Works

### 1. **Indexing Pipeline**
   - Scans repository for Python/TypeScript files
   - Parses code using Tree-sitter
   - Builds ASG (functions, classes, calls, imports)
   - Builds CFG (execution paths within functions)
   - Chunks code into 300-500 token pieces
   - Generates embeddings via Gemini
   - Stores in FAISS (vectors) and Neo4j (graphs)

### 2. **Retrieval System**
   - Vector search finds semantically similar code
   - Graph expansion finds related code via ASG
   - Hybrid ranker combines both signals
   - Context packer respects 70k token limit

### 3. **LLM Integration**
   - Gemini 2.5 Flash for generation
   - Streaming support for real-time responses
   - Token counting and enforcement
   - Retry logic with exponential backoff

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── db/                  # Database interfaces
│   │   ├── vector_store.py  # FAISS wrapper
│   │   ├── graph_store.py   # Neo4j wrapper
│   │   └── models.py        # Data models
│   ├── analysis/            # Code analysis
│   │   ├── tree_sitter_parser.py
│   │   ├── asg_builder.py   # ASG construction
│   │   ├── cfg_builder.py   # CFG construction
│   │   └── chunker.py       # Code chunking
│   ├── llm/                 # LLM integration
│   │   ├── gemini_client.py
│   │   ├── embeddings.py
│   │   ├── prompts.py
│   │   └── token_counter.py
│   ├── retrieval/           # Retrieval system
│   │   ├── vector_search.py
│   │   ├── graph_search.py
│   │   ├── ranker.py
│   │   └── context_packer.py
│   ├── services/            # Business logic
│   │   ├── indexer.py       # Main indexing pipeline
│   │   ├── file_scanner.py
│   │   └── metrics.py
│   └── api/                 # API routes
│       ├── chat.py
│       ├── debug.py
│       ├── plan.py
│       ├── files.py
│       └── index.py
├── frontend/
│   ├── app/                 # Next.js app router
│   ├── components/          # React components
│   └── lib/                 # API client & types
├── .env.example             # Environment template
└── README.md                # This file
```

## Troubleshooting

### Neo4j Connection Issues
- Ensure Neo4j is running: `http://localhost:7474`
- Check credentials in `.env`
- Verify ports 7687 (Bolt) and 7474 (HTTP) are not blocked

### Gemini API Errors
- Verify API key is valid
- Check rate limits
- Ensure you have access to Gemini 2.5 Flash

### Indexing Failures
- Check file permissions
- Ensure repository path is correct
- Look for syntax errors in source files
- Check backend logs for details

### Frontend Won't Connect
- Verify backend is running on port 5001
- Check CORS settings in `main.py`
- Ensure `FRONTEND_URL` in `.env` matches your frontend URL

## Performance Tips

- **Large Repositories**: Index takes ~1-5 minutes per 100 files
- **Query Speed**: First query may be slow (model loading), subsequent queries are fast
- **Token Limits**: Smaller chunks = more precise but less context
- **Database**: Keep Neo4j and FAISS on SSD for better performance

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.

## Acknowledgments

- Built with FastAPI, Next.js, Tree-sitter, FAISS, Neo4j, and Gemini 2.5 Flash
- Inspired by advanced code intelligence systems
