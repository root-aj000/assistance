"""
Rate limiter for API calls.
Implements a simple token bucket rate limiter.
"""
import time
import threading
from collections import defaultdict
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Token bucket rate limiter for API calls."""
    
    def __init__(self, requests_per_minute: int):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum number of requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute  # Seconds between requests
        self.last_request_time = 0.0
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        """
        Wait if necessary to respect rate limit.
        This method blocks until a request can be made.
        """
        with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            
            if time_since_last_request < self.interval:
                sleep_time = self.interval - time_since_last_request
                logger.info(f"⏳ Rate limit: waiting {sleep_time:.2f}s before next request")
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
    
    def can_make_request(self) -> bool:
        """
        Check if a request can be made without blocking.
        
        Returns:
            True if request can be made immediately, False otherwise
        """
        with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            return time_since_last_request >= self.interval
    
    def time_until_next_request(self) -> float:
        """
        Get the time in seconds until the next request can be made.
        
        Returns:
            Seconds until next request (0 if can make request now)
        """
        with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            
            if time_since_last_request >= self.interval:
                return 0.0
            
            return self.interval - time_since_last_request


class MultiModelRateLimiter:
    """Rate limiter that manages multiple models independently."""
    
    def __init__(self):
        """Initialize multi-model rate limiter."""
        self.limiters: Dict[str, RateLimiter] = {}
        self.lock = threading.Lock()
    
    def add_model(self, model_name: str, requests_per_minute: int):
        """
        Add a model to the rate limiter.
        
        Args:
            model_name: Name of the model
            requests_per_minute: Rate limit for this model
        """
        with self.lock:
            self.limiters[model_name] = RateLimiter(requests_per_minute)
            logger.info(f"✅ Rate limiter configured for {model_name}: {requests_per_minute} RPM")
    
    def wait_if_needed(self, model_name: str):
        """
        Wait if necessary to respect rate limit for a specific model.
        
        Args:
            model_name: Name of the model to check
        """
        with self.lock:
            if model_name not in self.limiters:
                logger.warning(f"⚠️  No rate limiter configured for {model_name}, using default")
                # Create a default rate limiter
                self.limiters[model_name] = RateLimiter(3)
        
        self.limiters[model_name].wait_if_needed()
    
    def can_make_request(self, model_name: str) -> bool:
        """
        Check if a request can be made for a specific model.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            True if request can be made, False otherwise
        """
        with self.lock:
            if model_name not in self.limiters:
                return True
        
        return self.limiters[model_name].can_make_request()
    
    def time_until_next_request(self, model_name: str) -> float:
        """
        Get time until next request for a specific model.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            Seconds until next request
        """
        with self.lock:
            if model_name not in self.limiters:
                return 0.0
        
        return self.limiters[model_name].time_until_next_request()


# Global rate limiter instance
rate_limiter = MultiModelRateLimiter()
