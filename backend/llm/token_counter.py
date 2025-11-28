"""
Token counter for managing context limits.
Uses tiktoken for accurate token counting.
"""
import tiktoken
from typing import List


class TokenCounter:
    """Handles token counting and enforcement."""
    
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize token counter.
        
        Args:
            model: Model name for encoding (using gpt-4 as proxy for Gemini)
        """
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base encoding
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def count_tokens_batch(self, texts: List[str]) -> List[int]:
        """Count tokens for multiple texts."""
        return [self.count_tokens(text) for text in texts]
    
    def truncate_to_limit(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to fit within token limit.
        
        Args:
            text: Input text
            max_tokens: Maximum number of tokens
            
        Returns:
            Truncated text
        """
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        
        truncated_tokens = tokens[:max_tokens]
        return self.encoding.decode(truncated_tokens)
    
    def fits_in_limit(self, texts: List[str], max_tokens: int) -> bool:
        """Check if a list of texts fits within token limit."""
        total_tokens = sum(self.count_tokens(text) for text in texts)
        return total_tokens <= max_tokens


# Global token counter instance
token_counter = TokenCounter()
