"""
Embedding generation using Gemini API.
"""
import google.generativeai as genai
from typing import List
from config import settings
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


class EmbeddingGenerator:
    """Generates embeddings using Gemini API."""
    
    def __init__(self, model: str = "models/embedding-001"):
        """
        Initialize embedding generator.
        
        Args:
            model: Gemini embedding model name
        """
        self.model = model
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return [0.0] * 768
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            query: Search query
            
        Returns:
            Query embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return [0.0] * 768


# Global embedding generator instance
embedding_generator = EmbeddingGenerator()
