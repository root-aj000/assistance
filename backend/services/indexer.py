"""
Main indexing pipeline orchestrating ASG, CFG, and embedding generation.
"""
from typing import List
from pathlib import Path
import hashlib
import logging

from services.file_scanner import file_scanner
from services.metrics import metrics_tracker
from analysis.tree_sitter_parser import parser
from analysis.asg_builder import asg_builder
from analysis.cfg_builder import cfg_builder
from analysis.chunker import chunker
from llm.embeddings import embedding_generator
from db.vector_store import VectorStore
from db.graph_store import GraphStore
from db.models import FileMetadata
from config import settings

logger = logging.getLogger(__name__)


class Indexer:
    """Main indexing pipeline."""
    
    def __init__(self):
        """Initialize indexer with database connections."""
        self.vector_store = VectorStore(settings.vector_db_path)
        self.graph_store = GraphStore(
            uri=settings.graph_db_url,
            user=settings.graph_db_user,
            password=settings.graph_db_password
        )
        self.indexed_files = {}  # file_path -> file_hash
    
    async def index_repository(self, repo_path: str) -> dict:
        """
        Index an entire repository.
        
        Args:
            repo_path: Path to repository root
            
        Returns:
            Indexing statistics
        """
        logger.info(f"Starting indexing of repository: {repo_path}")
        metrics_tracker.start_indexing()
        
        # Scan for files
        files = file_scanner.scan_directory(repo_path)
        metrics_tracker.set('files_total', len(files))
        
        # Index each file
        for file_path in files:
            try:
                await self.index_file(file_path)
                metrics_tracker.increment('files_indexed')
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {e}")
                metrics_tracker.increment('files_failed')
        
        metrics_tracker.finish_indexing()
        logger.info("Indexing complete!")
        
        return metrics_tracker.get_stats()
    
    async def index_file(self, file_path: str):
        """
        Index a single file.
        
        Args:
            file_path: Path to file
        """
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate file hash
        file_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check if file has changed
        if file_path in self.indexed_files and self.indexed_files[file_path] == file_hash:
            logger.info(f"Skipping unchanged file: {file_path}")
            return
        
        logger.info(f"Indexing file: {file_path}")
        
        # 1. Build ASG
        asg_nodes, asg_edges = asg_builder.build_asg(file_path, content)
        
        # Store ASG nodes and edges
        for node in asg_nodes:
            self.graph_store.add_code_node(node)
            metrics_tracker.increment('asg_nodes')
        
        for edge in asg_edges:
            self.graph_store.add_code_edge(edge)
        
        # 2. Build CFG for each function
        function_nodes = [n for n in asg_nodes if n.type.value == 'function']
        for func_node in function_nodes:
            cfg_nodes, cfg_edges = cfg_builder.build_cfg(
                func_node.id,
                func_node.code,
                func_node.start_line
            )
            
            for cfg_node in cfg_nodes:
                self.graph_store.add_cfg_node(cfg_node)
                metrics_tracker.increment('cfg_nodes')
            
            for cfg_edge in cfg_edges:
                self.graph_store.add_cfg_edge(cfg_edge)
        
        # 3. Chunk file
        chunks = chunker.chunk_file(file_path, content)
        metrics_tracker.increment('chunks', len(chunks))
        
        # 4. Generate embeddings
        for chunk in chunks:
            embedding = await embedding_generator.generate_embedding(chunk.code)
            chunk.embedding = embedding
            metrics_tracker.increment('embeddings')
        
        # 5. Store embeddings
        self.vector_store.add_embeddings(chunks)
        
        # Track indexed file
        self.indexed_files[file_path] = file_hash
        
        logger.info(f"Indexed {file_path}: {len(asg_nodes)} ASG nodes, {len(chunks)} chunks")
    
    def get_stats(self) -> dict:
        """Get indexing statistics."""
        return {
            'metrics': metrics_tracker.get_stats(),
            'vector_store': self.vector_store.get_stats(),
            'graph_store': self.graph_store.get_stats()
        }


# Global indexer instance
indexer = Indexer()
