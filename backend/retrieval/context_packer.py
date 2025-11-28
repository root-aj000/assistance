"""
Context packer that respects token limits.
"""
from typing import List, Tuple
from db.models import CodeChunk
from llm.token_counter import token_counter
from config import settings


class ContextPacker:
    """Packs relevant code chunks into context within token limits."""
    
    def __init__(self):
        """Initialize context packer."""
        self.max_tokens = settings.max_tokens_per_request
        self.system_reserve = settings.system_prompt_reserve
    
    def pack_context(
        self,
        ranked_chunks: List[Tuple[CodeChunk, float]],
        system_prompt: str
    ) -> Tuple[str, dict]:
        """
        Pack chunks into context within token limit.
        
        Args:
            ranked_chunks: Ranked list of (CodeChunk, score) tuples
            system_prompt: System prompt to include
            
        Returns:
            Tuple of (packed_context, stats)
        """
        # Calculate available tokens for context
        system_tokens = token_counter.count_tokens(system_prompt)
        available_tokens = self.max_tokens - system_tokens - self.system_reserve
        
        # Pack chunks greedily
        packed_chunks = []
        current_tokens = 0
        
        for chunk, score in ranked_chunks:
            chunk_tokens = chunk.tokens
            
            if current_tokens + chunk_tokens <= available_tokens:
                packed_chunks.append(chunk)
                current_tokens += chunk_tokens
            else:
                # Try to fit a truncated version
                remaining_tokens = available_tokens - current_tokens
                if remaining_tokens > 100:  # Minimum useful chunk size
                    truncated_code = token_counter.truncate_to_limit(
                        chunk.code,
                        remaining_tokens
                    )
                    truncated_chunk = CodeChunk(
                        id=chunk.id,
                        file_path=chunk.file_path,
                        start_line=chunk.start_line,
                        end_line=chunk.end_line,
                        code=truncated_code,
                        tokens=remaining_tokens,
                        metadata={**chunk.metadata, 'truncated': True}
                    )
                    packed_chunks.append(truncated_chunk)
                    current_tokens += remaining_tokens
                break
        
        # Build context string
        context_parts = []
        for chunk in packed_chunks:
            context_parts.append(
                f"File: {chunk.file_path} (lines {chunk.start_line}-{chunk.end_line})\n"
                f"```\n{chunk.code}\n```\n"
            )
        
        context = "\n".join(context_parts)
        
        # Calculate stats
        stats = {
            "total_chunks": len(ranked_chunks),
            "packed_chunks": len(packed_chunks),
            "context_tokens": current_tokens,
            "system_tokens": system_tokens,
            "total_tokens": system_tokens + current_tokens,
            "utilization": (system_tokens + current_tokens) / self.max_tokens,
            "available_tokens": available_tokens,
            "used_tokens": current_tokens
        }
        
        return context, stats


# Global context packer instance
context_packer = ContextPacker()
