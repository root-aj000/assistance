"""
Unified embedding interface that automatically uses local or Gemini embeddings.
"""
from typing import List
from config import settings
import logging

logger = logging.getLogger(__name__)


class UnifiedEmbeddingGenerator:
    """
    Smart embedding generator that automatically chooses between:
    - Local embeddings (free, unlimited, no API calls)
    - Gemini embeddings (requires API quota)
    """
    
    def __init__(self):
        """Initialize the appropriate embedding generator based on settings."""
        self.use_local = settings.use_local_embeddings
        
        if self.use_local:
            logger.info("🏠 Using LOCAL embeddings (free, unlimited)")
            from llm.local_embeddings import get_local_embedding_generator
            self.generator = get_local_embedding_generator()
        else:
            logger.info("☁️  Using GEMINI embeddings (requires API quota)")
            from llm.embeddings import embedding_generator
            self.generator = embedding_generator
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        return await self.generator.generate_embedding(text)
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        return await self.generator.generate_embeddings_batch(texts)
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            query: Search query
            
        Returns:
            Query embedding vector
        """
        return await self.generator.generate_query_embedding(query)


# Global unified embedding generator
unified_embedding_generator = UnifiedEmbeddingGenerator()
