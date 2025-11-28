"""
Embedding generation using Gemini API.
"""
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from typing import List
from config import settings
from llm.rate_limiter import rate_limiter
import logging
import time

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)

# Initialize rate limiter for embeddings
rate_limiter.add_model("embeddings", settings.embedding_rate_limit_rpm)


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
        max_retries = 3
        base_delay = 2
        
        # Apply rate limiting
        rate_limiter.wait_if_needed("embeddings")
        
        for attempt in range(max_retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
            except google_exceptions.ResourceExhausted as e:
                error_msg = str(e)
                if "quota" in error_msg.lower():
                    logger.error(f"❌ API Quota Exceeded: {error_msg}")
                    logger.error("Please wait for quota to reset or upgrade your API plan")
                    logger.error("Visit: https://ai.google.dev/gemini-api/docs/rate-limits")
                    # Don't retry on quota errors, fail immediately
                    return [0.0] * 768
                else:
                    # Retry other resource exhausted errors
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Resource exhausted, retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"Error generating embedding after {max_retries} attempts: {e}")
                        return [0.0] * 768
            except Exception as e:
                logger.error(f"Error generating embedding: {e}")
                return [0.0] * 768
        
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
        # Apply rate limiting
        rate_limiter.wait_if_needed("embeddings")
        
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=query,
                    task_type="retrieval_query"
                )
                return result['embedding']
            except google_exceptions.ResourceExhausted as e:
                error_msg = str(e)
                if "quota" in error_msg.lower():
                    logger.error(f"❌ API Quota Exceeded for query embedding: {error_msg}")
                    logger.error("Please wait for quota to reset or upgrade your API plan")
                    logger.error("Visit: https://ai.google.dev/gemini-api/docs/rate-limits")
                    return [0.0] * 768
                else:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Resource exhausted, retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"Error generating query embedding after {max_retries} attempts: {e}")
                        return [0.0] * 768
            except Exception as e:
                logger.error(f"Error generating query embedding: {e}")
                return [0.0] * 768
        
        return [0.0] * 768


# Global embedding generator instance
embedding_generator = EmbeddingGenerator()

