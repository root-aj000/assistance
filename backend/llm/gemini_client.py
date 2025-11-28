"""
Gemini API client with streaming support.
"""
import google.generativeai as genai
from typing import AsyncGenerator, Optional
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


class GeminiClient:
    """Client for Gemini LLM interactions."""
    
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini client.
        
        Args:
            model: Gemini model name
        """
        self.model = genai.GenerativeModel(model)
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a non-streaming response.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_response_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response.
        
        Args:
            prompt: Input prompt
            
        Yields:
            Text chunks as they are generated
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            yield f"Error: {str(e)}"
    
    async def generate_with_context(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response with system prompt and user message.
        
        Args:
            system_prompt: System instructions
            user_message: User's message
            max_tokens: Optional max output tokens
            
        Returns:
            Generated response
        """
        # Combine prompts
        full_prompt = f"{system_prompt}\n\n{user_message}"
        
        # Override max tokens if specified
        config = self.generation_config.copy()
        if max_tokens:
            config["max_output_tokens"] = max_tokens
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating response with context: {e}")
            raise


# Global Gemini client instance
gemini_client = GeminiClient()
