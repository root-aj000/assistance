"""
Configuration module for Vibe Coding AI Agent.
Uses pydantic-settings for type-safe environment variable handling.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API Configuration
    gemini_api_key: str = Field(..., description="Gemini API key for LLM and embeddings")
    
    # Embedding Configuration
    use_local_embeddings: bool = Field(default=True, description="Use local embeddings instead of Gemini API (free, no quota)")
    local_embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Local embedding model name")
    
    # Gemini Model Selection
    # Available models: gemini-2.5-flash, gemini-2.5-pro, gemini-2.5-flash-lite
    gemini_flash_model: str = Field(default="gemini-2.5-flash", description="Fast, lightweight model")
    gemini_pro_model: str = Field(default="gemini-2.5-pro", description="Most capable model")
    gemini_lite_model: str = Field(default="gemini-2.5-flash-lite", description="Ultra-fast lite model")
    gemini_embedding_model: str = Field(default="models/text-embedding-004", description="Embedding model")
    
    # Default model to use for chat
    default_chat_model: str = Field(default="gemini-2.5-flash", description="Default model for chat")
    
    # Model-specific Rate Limiting (requests per minute)
    # Set to 3 RPM to avoid quota issues
    flash_rate_limit_rpm: int = Field(default=3, description="Rate limit for Flash model (RPM)")
    pro_rate_limit_rpm: int = Field(default=3, description="Rate limit for Pro model (RPM)")
    lite_rate_limit_rpm: int = Field(default=3, description="Rate limit for Lite model (RPM)")
    embedding_rate_limit_rpm: int = Field(default=3, description="Rate limit for embeddings (RPM)")
    
    # Vector Database (FAISS)
    vector_db_path: str = Field(default="./data/vector_db", description="Path to FAISS vector database")
    
    # Graph Database (Neo4j)
    graph_db_url: str = Field(default="bolt://localhost:7687", description="Neo4j connection URL")
    graph_db_user: str = Field(default="neo4j", description="Neo4j username")
    graph_db_password: str = Field(..., description="Neo4j password")
    
    # Token Management
    max_tokens_per_request: int = Field(default=70000, description="Maximum tokens per LLM request")
    system_prompt_reserve: int = Field(default=3000, description="Reserved tokens for system prompt")
    
    # Legacy Rate Limiting (kept for backwards compatibility)
    rate_limit_rpm: int = Field(default=3, description="Global rate limit: requests per minute")
    rate_limit_tpm: int = Field(default=100000, description="Rate limit: tokens per minute")
    
    # Server Configuration
    backend_host: str = Field(default="0.0.0.0", description="Backend server host")
    backend_port: int = Field(default=5001, description="Backend server port")
    
    # Frontend Configuration
    frontend_url: str = Field(default="http://localhost:3000", description="Frontend URL for CORS")
    
    # Indexing Configuration
    chunk_size_tokens: int = Field(default=400, description="Target chunk size in tokens")
    chunk_overlap: int = Field(default=50, description="Overlap between chunks in tokens")
    repository_path: Optional[str] = Field(default=None, description="Repository path to auto-index on startup")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
