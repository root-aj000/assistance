"""
Graph-based search using ASG and CFG.
"""
from typing import List, Dict, Any
from db.graph_store import GraphStore
from config import settings


class GraphSearch:
    """Performs graph-based code search."""
    
    def __init__(self):
        """Initialize graph search with graph store."""
        self.graph_store = GraphStore(
            uri=settings.graph_db_url,
            user=settings.graph_db_user,
            password=settings.graph_db_password
        )
    
    def expand_neighbors(self, node_ids: List[str], max_depth: int = 2) -> List[Dict[str, Any]]:
        """
        Expand neighbors in the ASG.
        
        Args:
            node_ids: Starting node IDs
            max_depth: Maximum traversal depth
            
        Returns:
            List of expanded node dictionaries
        """
        all_neighbors = []
        seen_ids = set()
        
        for node_id in node_ids:
            neighbors = self.graph_store.get_neighbors(node_id, max_depth)
            for neighbor in neighbors:
                if neighbor['id'] not in seen_ids:
                    all_neighbors.append(neighbor)
                    seen_ids.add(neighbor['id'])
        
        return all_neighbors
    
    def get_cfg_paths(self, function_ids: List[str]) -> Dict[str, List[List[str]]]:
        """
        Get CFG paths for multiple functions.
        
        Args:
            function_ids: List of function node IDs
            
        Returns:
            Dictionary mapping function ID to list of paths
        """
        paths = {}
        for function_id in function_ids:
            paths[function_id] = self.graph_store.get_cfg_paths(function_id)
        return paths
    
    def search_by_name(self, name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for code nodes by name.
        
        Args:
            name: Name to search for
            limit: Maximum results
            
        Returns:
            List of matching nodes
        """
        return self.graph_store.search_by_name(name, limit)
    
    def get_stats(self) -> dict:
        """Get graph store statistics."""
        return self.graph_store.get_stats()


# Global graph search instance
graph_search = GraphSearch()
