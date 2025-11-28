"""
Code chunking for embedding generation.
Breaks code into manageable pieces while respecting token limits.
"""
from typing import List
from llm.token_counter import token_counter
from db.models import CodeChunk
import hashlib


class CodeChunker:
    """Chunks code for embedding generation."""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target chunk size in tokens
            overlap: Overlap between chunks in tokens
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_file(self, file_path: str, content: str) -> List[CodeChunk]:
        """
        Chunk a file's content.
        
        Args:
            file_path: Path to the file
            content: File content
            
        Returns:
            List of CodeChunk objects
        """
        lines = content.split('\n')
        chunks = []
        
        current_chunk = []
        current_tokens = 0
        start_line = 1
        
        for i, line in enumerate(lines, 1):
            line_tokens = token_counter.count_tokens(line)
            
            # If adding this line exceeds chunk size, save current chunk
            if current_tokens + line_tokens > self.chunk_size and current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunk_id = self._generate_chunk_id(file_path, start_line, i - 1)
                
                chunks.append(CodeChunk(
                    id=chunk_id,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=i - 1,
                    code=chunk_text,
                    tokens=current_tokens,
                    metadata={"method": "line_based"}
                ))
                
                # Start new chunk with overlap
                overlap_lines = self._calculate_overlap_lines(current_chunk)
                current_chunk = overlap_lines + [line]
                current_tokens = token_counter.count_tokens('\n'.join(current_chunk))
                start_line = i - len(overlap_lines)
            else:
                current_chunk.append(line)
                current_tokens += line_tokens
        
        # Add remaining chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunk_id = self._generate_chunk_id(file_path, start_line, len(lines))
            
            chunks.append(CodeChunk(
                id=chunk_id,
                file_path=file_path,
                start_line=start_line,
                end_line=len(lines),
                code=chunk_text,
                tokens=current_tokens,
                metadata={"method": "line_based"}
            ))
        
        return chunks
    
    def _calculate_overlap_lines(self, lines: List[str]) -> List[str]:
        """Calculate overlap lines to include in next chunk."""
        if not lines or self.overlap <= 0:
            return []
        
        # Take last N lines that fit within overlap token limit
        overlap_lines = []
        overlap_tokens = 0
        
        for line in reversed(lines):
            line_tokens = token_counter.count_tokens(line)
            if overlap_tokens + line_tokens <= self.overlap:
                overlap_lines.insert(0, line)
                overlap_tokens += line_tokens
            else:
                break
        
        return overlap_lines
    
    def _generate_chunk_id(self, file_path: str, start_line: int, end_line: int) -> str:
        """Generate unique chunk ID."""
        content = f"{file_path}:{start_line}-{end_line}"
        return hashlib.md5(content.encode()).hexdigest()


# Global chunker instance
chunker = CodeChunker()
