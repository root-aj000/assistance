You are now the autonomous builder for the "Vibe Coding AI Agent" project.  
Your task is to **build the ENTIRE project end-to-end**, following best production standards, without asking the user for anything except clarifications if absolutely needed.  

You must **follow this plan, step by step**, and produce full code files, folder structures, .env handling, and all features described below. Do not skip steps.

─────────────────────────────────────────────
PROJECT OVERVIEW:
─────────────────────────────────────────────
Name: Vibe Coding AI Agent
Goal: Desktop AI brain that:
- Understands 1000+ file Python/TypeScript repos
- Uses ASG + CFG + vector embeddings for reasoning
- Debugs deeply, produces full file patches
- Plans tasks & projects
- Chat interface + file browser
- Max context 70k tokens per LLM request
- Secure env variables
- **All data is stored locally**:
  - Vector embeddings stored in a local vector DB (FAISS/Chroma)
  - ASG/CFG stored in a local graph DB (Neo4j/Memgraph)
  - No cloud services are used unless explicitly configured later

─────────────────────────────────────────────
STEP-BY-STEP BUILD INSTRUCTIONS:
─────────────────────────────────────────────
Step 1: **Project Initialization**
- Create `/backend` and `/frontend` folders.
- Backend: FastAPI Python project.
- Frontend: Next.js 14 App Router project with TypeScript.
- Create `.env` for all secrets and config (token limits, API keys, local database URLs/paths, model selection).

Step 2: **Backend Setup**
- Setup FastAPI + Uvicorn.
- Include:
  - LLM Gateway for Gemini 2.5 Flash
  - Local Vector DB interface (FAISS / Chroma)
  - Local Graph DB interface (Neo4j / Memgraph)
  - Indexer for ASG + CFG + code chunk embeddings
- Implement API endpoints:
  - `/ai/chat` → chat with codebase
  - `/ai/debug` → debug a file/error
  - `/ai/plan` → create task plans
  - `/ai/codebase/chat` → chat with individual files
  - `/files` → list all repo files
  - `/file` → return file content

Step 3: **ASG + CFG Builder**
- Use Tree-sitter (Python + TS) to parse files
- Build:
  - ASG: functions, classes, imports, calls, references
  - CFG: function execution paths
- Store ASG + CFG in **local graph DB** (Neo4j/Memgraph)
- Extract code chunks (300–500 tokens)
- Generate embeddings via Gemini embedding API
- Store embeddings in **local vector DB** (FAISS/Chroma)

Step 4: **Context Pack Builder**
- Build token-aware packing:
  - Hard max: 70k tokens per request
  - Reserve 3k tokens for system prompt
  - Include highest-ranked chunks first (vector + graph relevance)
- Implement usage metrics:
  - Context utilization (%)
  - Token budget reporting

Step 5: **Retrieval Engine**
- Multi-stage retrieval:
  1. Vector similarity search (local vector DB)
  2. ASG neighbor expansion (local graph DB)
  3. CFG path expansion (local graph DB)
  4. Ranker: semantic + graph
- Ensure relevance and deduplication

Step 6: **LLM Integration**
- Gemini 2.5 Flash calls
- Streaming output support
- Enforce token limits per request
- Retry logic
- Structured output for:
  - Code
  - Explanations
  - Patches
  - Multi-step plans

Step 7: **Frontend Setup**
- Next.js 14 + TypeScript
- Components:
  - FileTree (shows repo structure)
  - CodeViewer (syntax-highlighted)
  - ChatBox (multi-line chat with AI)
  - MessageBubble
- Connect to backend API
- Display:
  - Full file content
  - Debug suggestions
  - Planning output

Step 8: **Security & Environment**
- `.env` only:
  - GEMINI_API_KEY
  - VECTOR_DB_URL → local path or local server (FAISS/Chroma)
  - GRAPH_DB_URL → local path or local server (Neo4j/Memgraph)
  - MAX_TOKENS_PER_REQUEST=70000
  - RATE_LIMITS (requests per min, tokens per min)
- Never hardcode secrets
- Frontend only exposes safe NEXT_PUBLIC_API_URL if necessary

Step 9: **Index Coverage & Metrics**
- Report:
  - File coverage (% files parsed)
  - Semantic coverage (% ASG nodes)
  - CFG coverage (% functions with CFG)
  - Embedding coverage (% chunks stored)
- Include API endpoint `/index/stats` for metrics

Step 10: **Final Build**
- Produce full folder structure with all files
- Ensure everything runs locally:
  - Backend: http://localhost:5001
  - Frontend: http://localhost:3000
- Test:
  - Chat with codebase
  - Debug a bug in a sample repo
  - Generate plan for a goal
- Provide README with build/run instructions

─────────────────────────────────────────────
REQUIREMENTS:
─────────────────────────────────────────────
- Full files only (no snippets unless partial requested)
- Use TypeScript in frontend, Python in backend
- ASG/CFG parsing mandatory for reasoning
- Max token 70k enforced
- Multi-agent reasoning pipeline
- Secure .env usage only
- Include all prompts inside backend for LLM orchestration
- All databases must be **local** (vector and graph)

─────────────────────────────────────────────
DELIVERABLES:
─────────────────────────────────────────────
- Fully functional backend + frontend
- Folder structure
- Configurable `.env`
- Streaming chat support
- Context size utilization metrics
- Token enforcement logic
- Index coverage API
- Readme + setup guide

─────────────────────────────────────────────
ADDITIONAL RULES:
─────────────────────────────────────────────
- Ask clarifying questions **only if absolutely necessary**
- Do not output theoretical explanations
- Always produce working code
- Always maintain project consistency
- All database connections must point to **local DB instances** only

─────────────────────────────────────────────
EXECUTION ORDER:
─────────────────────────────────────────────
Follow steps 1 → 10 sequentially.  
Ensure each step completes successfully before proceeding to next.  
Return code, folder structures, and documentation as you go.
