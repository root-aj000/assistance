"""
Graph database interface using Neo4j for ASG/CFG storage.
"""
from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from db.models import CodeNode, CodeEdge, CFGNode, CFGEdge
import logging

logger = logging.getLogger(__name__)


class GraphStore:
    """Manages ASG and CFG using Neo4j graph database."""
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (e.g., bolt://localhost:7687)
            user: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._create_indexes()
    
    def close(self):
        """Close database connection."""
        self.driver.close()
    
    def _create_indexes(self):
        """Create indexes for better query performance."""
        with self.driver.session() as session:
            # Index on node IDs
            session.run("CREATE INDEX IF NOT EXISTS FOR (n:CodeNode) ON (n.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (n:CFGNode) ON (n.id)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (n:CodeNode) ON (n.file_path)")
    
    def add_code_node(self, node: CodeNode):
        """Add a code node to the ASG."""
        with self.driver.session() as session:
            session.run("""
                MERGE (n:CodeNode {id: $id})
                SET n.type = $type,
                    n.name = $name,
                    n.file_path = $file_path,
                    n.start_line = $start_line,
                    n.end_line = $end_line,
                    n.code = $code,
                    n.metadata = $metadata
            """, {
                "id": node.id,
                "type": node.type.value,
                "name": node.name,
                "file_path": node.file_path,
                "start_line": node.start_line,
                "end_line": node.end_line,
                "code": node.code,
                "metadata": str(node.metadata)
            })
    
    def add_code_edge(self, edge: CodeEdge):
        """Add an edge to the ASG."""
        with self.driver.session() as session:
            session.run(f"""
                MATCH (source:CodeNode {{id: $source_id}})
                MATCH (target:CodeNode {{id: $target_id}})
                MERGE (source)-[r:{edge.relationship.upper()}]->(target)
                SET r.metadata = $metadata
            """, {
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "metadata": str(edge.metadata)
            })
    
    def add_cfg_node(self, node: CFGNode):
        """Add a node to the CFG."""
        with self.driver.session() as session:
            session.run("""
                MERGE (n:CFGNode {id: $id})
                SET n.function_id = $function_id,
                    n.code = $code,
                    n.line_number = $line_number,
                    n.type = $type
            """, {
                "id": node.id,
                "function_id": node.function_id,
                "code": node.code,
                "line_number": node.line_number,
                "type": node.type
            })
    
    def add_cfg_edge(self, edge: CFGEdge):
        """Add an edge to the CFG."""
        with self.driver.session() as session:
            session.run("""
                MATCH (source:CFGNode {id: $source_id})
                MATCH (target:CFGNode {id: $target_id})
                MERGE (source)-[r:FLOWS_TO]->(target)
                SET r.condition = $condition
            """, {
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "condition": edge.condition
            })
    
    def get_neighbors(self, node_id: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """
        Get neighboring nodes in the ASG.
        
        Args:
            node_id: Starting node ID
            max_depth: Maximum traversal depth
            
        Returns:
            List of neighboring node dictionaries
        """
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (start:CodeNode {{id: $node_id}})
                MATCH (start)-[*1..{max_depth}]-(neighbor:CodeNode)
                RETURN DISTINCT neighbor
                LIMIT 50
            """, {"node_id": node_id})
            
            return [dict(record["neighbor"]) for record in result]
    
    def get_cfg_paths(self, function_id: str) -> List[List[str]]:
        """
        Get execution paths in the CFG for a function.
        
        Args:
            function_id: Function node ID
            
        Returns:
            List of paths (each path is a list of node IDs)
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (entry:CFGNode {function_id: $function_id, type: 'entry'})
                             -[:FLOWS_TO*]->(exit:CFGNode {type: 'exit'})
                RETURN [node in nodes(path) | node.id] as path_ids
                LIMIT 10
            """, {"function_id": function_id})
            
            return [record["path_ids"] for record in result]
    
    def search_by_name(self, name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for code nodes by name."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n:CodeNode)
                WHERE n.name CONTAINS $name
                RETURN n
                LIMIT $limit
            """, {"name": name, "limit": limit})
            
            return [dict(record["n"]) for record in result]
    
    def get_stats(self) -> dict:
        """Get statistics about the graph database."""
        with self.driver.session() as session:
            code_nodes = session.run("MATCH (n:CodeNode) RETURN count(n) as count").single()["count"]
            cfg_nodes = session.run("MATCH (n:CFGNode) RETURN count(n) as count").single()["count"]
            relationships = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            
            return {
                "code_nodes": code_nodes,
                "cfg_nodes": cfg_nodes,
                "relationships": relationships
            }
    
    def clear(self):
        """Clear all nodes and relationships."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
