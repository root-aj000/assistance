"""
Vector database interface using FAISS for local embedding storage.
"""
import faiss
import numpy as np
import pickle
import os
from pathlib import Path
from typing import List, Tuple, Optional
from db.models import CodeChunk


class VectorStore:
    """Manages code embeddings using FAISS."""
    
    def __init__(self, db_path: str, dimension: int = 768):
        """
        Initialize FAISS vector store.
        
        Args:
            db_path: Path to store FAISS index and metadata
            dimension: Embedding dimension (768 for Gemini embeddings)
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.dimension = dimension
        self.index_path = self.db_path / "faiss.index"
        self.metadata_path = self.db_path / "metadata.pkl"
        
        # Initialize or load index
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, 'rb') as f:
                self.chunk_metadata = pickle.load(f)
        else:
            # Create a new index (IndexFlatL2 for exact search)
            self.index = faiss.IndexFlatL2(dimension)
            self.chunk_metadata: List[CodeChunk] = []
    
    def add_embeddings(self, chunks: List[CodeChunk]):
        """
        Add code chunks with embeddings to the vector store.
        
        Args:
            chunks: List of CodeChunk objects with embeddings
        """
        if not chunks:
            return
        
        # Extract embeddings
        embeddings = np.array([chunk.embedding for chunk in chunks], dtype=np.float32)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store metadata
        self.chunk_metadata.extend(chunks)
        
        # Save to disk
        self._save()
    
    def search(self, query_embedding: List[float], k: int = 10) -> List[Tuple[CodeChunk, float]]:
        """
        Search for similar code chunks.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (CodeChunk, distance) tuples
        """
        if self.index.ntotal == 0:
            return []
        
        # Convert query to numpy array
        query = np.array([query_embedding], dtype=np.float32)
        
        # Search
        distances, indices = self.index.search(query, min(k, self.index.ntotal))
        
        # Return chunks with distances
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunk_metadata):
                results.append((self.chunk_metadata[idx], float(distance)))
        
        return results
    
    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        return {
            "total_embeddings": self.index.ntotal,
            "dimension": self.dimension,
            "total_chunks": len(self.chunk_metadata)
        }
    
    def clear(self):
        """Clear all embeddings and metadata."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunk_metadata = []
        self._save()
    
    def _save(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, str(self.index_path))
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.chunk_metadata, f)
