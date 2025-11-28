"""
Vector similarity search using the vector store.
"""
from typing import List, Tuple
from db.models import CodeChunk
from db.vector_store import VectorStore
from llm.embeddings import embedding_generator
from config import settings


class VectorSearch:
    """Performs vector similarity search."""
    
    def __init__(self):
        """Initialize vector search with vector store."""
        self.vector_store = VectorStore(settings.vector_db_path)
    
    async def search(self, query: str, k: int = 10) -> List[Tuple[CodeChunk, float]]:
        """
        Search for relevant code chunks using vector similarity.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (CodeChunk, similarity_score) tuples
        """
        # Generate query embedding
        query_embedding = await embedding_generator.generate_query_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, k=k)
        
        # Convert distances to similarity scores (lower distance = higher similarity)
        # Using inverse distance as similarity
        scored_results = []
        for chunk, distance in results:
            similarity = 1.0 / (1.0 + distance)
            scored_results.append((chunk, similarity))
        
        return scored_results
    
    def get_stats(self) -> dict:
        """Get vector store statistics."""
        return self.vector_store.get_stats()


# Global vector search instance
vector_search = VectorSearch()
