"""
Local embedding generation using HuggingFace sentence-transformers.
Completely free, no API calls, runs on your machine.
"""
from sentence_transformers import SentenceTransformer
from typing import List
import logging
import numpy as np

logger = logging.getLogger(__name__)


class LocalEmbeddingGenerator:
    """Generates embeddings using local sentence-transformers model."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize local embedding generator.
        
        Args:
            model_name: HuggingFace model name
                - all-MiniLM-L6-v2: Fast, lightweight, 384 dimensions (Default)
                - all-mpnet-base-v2: Better quality, 768 dimensions
                - multi-qa-MiniLM-L6-cos-v1: Optimized for Q&A
        """
        self.model_name = model_name
        logger.info(f"📦 Loading local embedding model: {model_name}...")
        
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"✅ Local embedding model loaded! Dimension: {self.embedding_dim}")
        except Exception as e:
            logger.error(f"❌ Failed to load local embedding model: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating local embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * self.embedding_dim
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batched for efficiency).
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating local embeddings batch: {e}")
            return [[0.0] * self.embedding_dim for _ in texts]
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            query: Search query
            
        Returns:
            Query embedding vector
        """
        # For sentence-transformers, query and document embeddings are the same
        return await self.generate_embedding(query)


# Global local embedding generator instance
# This will be initialized on first use to avoid loading model at startup
_local_embedding_generator = None


def get_local_embedding_generator() -> LocalEmbeddingGenerator:
    """Get or create the global local embedding generator instance."""
    global _local_embedding_generator
    if _local_embedding_generator is None:
        _local_embedding_generator = LocalEmbeddingGenerator()
    return _local_embedding_generator
