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
    
    # Vector Database (FAISS)
    vector_db_path: str = Field(default="./data/vector_db", description="Path to FAISS vector database")
    
    # Graph Database (Neo4j)
    graph_db_url: str = Field(default="bolt://localhost:7687", description="Neo4j connection URL")
    graph_db_user: str = Field(default="neo4j", description="Neo4j username")
    graph_db_password: str = Field(..., description="Neo4j password")
    
    # Token Management
    max_tokens_per_request: int = Field(default=70000, description="Maximum tokens per LLM request")
    system_prompt_reserve: int = Field(default=3000, description="Reserved tokens for system prompt")
    
    # Rate Limiting
    rate_limit_rpm: int = Field(default=60, description="Rate limit: requests per minute")
    rate_limit_tpm: int = Field(default=100000, description="Rate limit: tokens per minute")
    
    # Server Configuration
    backend_host: str = Field(default="0.0.0.0", description="Backend server host")
    backend_port: int = Field(default=5001, description="Backend server port")
    
    # Frontend Configuration
    frontend_url: str = Field(default="http://localhost:3000", description="Frontend URL for CORS")
    
    # Indexing Configuration
    chunk_size_tokens: int = Field(default=400, description="Target chunk size in tokens")
    chunk_overlap: int = Field(default=50, description="Overlap between chunks in tokens")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
