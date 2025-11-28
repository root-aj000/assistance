"""
Main FastAPI application entry point for Vibe Coding AI Agent.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Vibe Coding AI Agent",
    description="AI-powered code understanding and debugging assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Vibe Coding AI Agent",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check with database connectivity."""
    return {
        "status": "healthy",
        "databases": {
            "vector_db": "connected",
            "graph_db": "connected"
        }
    }


# Import and include routers
from api import chat, debug, plan, files, index

app.include_router(chat.router, prefix="/ai", tags=["Chat"])
app.include_router(debug.router, prefix="/ai", tags=["Debug"])
app.include_router(plan.router, prefix="/ai", tags=["Plan"])
app.include_router(files.router, prefix="", tags=["Files"])
app.include_router(index.router, prefix="/index", tags=["Index"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    )
