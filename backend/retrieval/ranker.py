"""
Hybrid ranker combining vector and graph signals.
"""
from typing import List, Tuple, Dict, Any
from db.models import CodeChunk


class HybridRanker:
    """Ranks results using both semantic and graph signals."""
    
    def __init__(self, vector_weight: float = 0.6, graph_weight: float = 0.4):
        """
        Initialize ranker.
        
        Args:
            vector_weight: Weight for vector similarity scores
            graph_weight: Weight for graph centrality scores
        """
        self.vector_weight = vector_weight
        self.graph_weight = graph_weight
    
    def rank(
        self,
        vector_results: List[Tuple[CodeChunk, float]],
        graph_nodes: List[Dict[str, Any]]
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Rank code chunks using hybrid scoring.
        
        Args:
            vector_results: Vector search results with similarity scores
            graph_nodes: Graph nodes from ASG expansion
            
        Returns:
            Ranked list of (CodeChunk, score) tuples
        """
        # Build graph node set for quick lookup
        graph_file_lines = set()
        for node in graph_nodes:
            file_path = node.get('file_path', '')
            start_line = node.get('start_line', 0)
            end_line = node.get('end_line', 0)
            for line in range(start_line, end_line + 1):
                graph_file_lines.add((file_path, line))
        
        # Score each vector result
        scored_results = []
        for chunk, vector_score in vector_results:
            # Check if chunk overlaps with graph nodes
            graph_score = 0.0
            chunk_lines = range(chunk.start_line, chunk.end_line + 1)
            for line in chunk_lines:
                if (chunk.file_path, line) in graph_file_lines:
                    graph_score = 1.0
                    break
            
            # Combined score
            combined_score = (
                self.vector_weight * vector_score +
                self.graph_weight * graph_score
            )
            
            scored_results.append((chunk, combined_score))
        
        # Sort by combined score (descending)
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return scored_results
    
    def deduplicate(
        self,
        results: List[Tuple[CodeChunk, float]]
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Remove duplicate chunks based on file path and line overlap.
        
        Args:
            results: List of (CodeChunk, score) tuples
            
        Returns:
            Deduplicated results
        """
        seen = set()
        deduped = []
        
        for chunk, score in results:
            # Create signature based on file and line range
            signature = (chunk.file_path, chunk.start_line, chunk.end_line)
            
            if signature not in seen:
                seen.add(signature)
                deduped.append((chunk, score))
        
        return deduped


# Global ranker instance
ranker = HybridRanker()
