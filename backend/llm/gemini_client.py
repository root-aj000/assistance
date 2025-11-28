"""
Gemini API client with streaming support and rate limiting.
"""
import google.generativeai as genai
from typing import AsyncGenerator, Optional
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from llm.rate_limiter import rate_limiter
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)

# Initialize rate limiters for each model
rate_limiter.add_model(settings.gemini_flash_model, settings.flash_rate_limit_rpm)
rate_limiter.add_model(settings.gemini_pro_model, settings.pro_rate_limit_rpm)
rate_limiter.add_model(settings.gemini_lite_model, settings.lite_rate_limit_rpm)


class GeminiClient:
    """Client for Gemini LLM interactions with rate limiting."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            model_name: Gemini model name (default: settings.default_chat_model)
        """
        self.model_name = model_name or settings.default_chat_model
        self.model = genai.GenerativeModel(self.model_name)
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        logger.info(f"🚀 Initialized Gemini client with model: {self.model_name}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry_error_callback=lambda retry_state: None
    )
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a non-streaming response with rate limiting.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        # Apply rate limiting
        rate_limiter.wait_if_needed(self.model_name)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                logger.error(f"❌ API Quota Exceeded: {error_msg}")
                logger.error("⚠️  You have exceeded your Gemini API quota.")
                logger.error("📊 Please check your usage at: https://ai.dev/usage")
                logger.error("📖 Learn about rate limits: https://ai.google.dev/gemini-api/docs/rate-limits")
                raise Exception("API Quota Exceeded. Please wait for quota to reset or upgrade your plan.")
            else:
                logger.error(f"Error generating response: {e}")
                raise
    
    async def generate_response_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response with rate limiting.
        
        Args:
            prompt: Input prompt
            
        Yields:
            Text chunks as they are generated
        """
        # Apply rate limiting
        rate_limiter.wait_if_needed(self.model_name)
        
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
        Generate response with system prompt and user message with rate limiting.
        
        Args:
            system_prompt: System instructions
            user_message: User's message
            max_tokens: Optional max output tokens
            
        Returns:
            Generated response
        """
        # Apply rate limiting
        rate_limiter.wait_if_needed(self.model_name)
        
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


# Global Gemini client instances for each model
gemini_client = GeminiClient(settings.default_chat_model)
gemini_flash_client = GeminiClient(settings.gemini_flash_model)
gemini_pro_client = GeminiClient(settings.gemini_pro_model)
gemini_lite_client = GeminiClient(settings.gemini_lite_model)

