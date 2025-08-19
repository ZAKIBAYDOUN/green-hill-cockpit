"""OpenAI client with API key fallback"""
import os
from openai import OpenAI
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class OpenAIClientWithFallback:
    """OpenAI client that tries multiple API keys from environment"""
    
    def __init__(self):
        self.api_keys = []
        
        # Load keys from environment only
        primary_key = os.getenv("OPENAI_API_KEY")
        fallback_key = os.getenv("OPENAI_API_KEY_FALLBACK")
        
        if primary_key:
            self.api_keys.append(primary_key)
        if fallback_key:
            self.api_keys.append(fallback_key)
        
        if not self.api_keys:
            raise ValueError("No OpenAI API keys configured in environment")
        
        self.current_key_index = 0
        self._client = OpenAI(api_key=self.api_keys[0])
    
    def _try_next_key(self):
        """Switch to next API key"""
        self.current_key_index += 1
        if self.current_key_index < len(self.api_keys):
            self._client = OpenAI(api_key=self.api_keys[self.current_key_index])
            return True
        return False
    
    @property
    def chat(self):
        return self
    
    @property
    def completions(self):
        return self
    
    def create(self, **kwargs):
        """Create completion with automatic fallback"""
        last_error = None
        
        for _ in range(len(self.api_keys)):
            try:
                return self._client.chat.completions.create(**kwargs)
            except Exception as e:
                last_error = e
                if "invalid_api_key" in str(e) or "Incorrect API key" in str(e):
                    if not self._try_next_key():
                        break
                else:
                    raise e
        
        raise last_error or Exception("All API keys failed")

def get_openai_client():
    """Get OpenAI client with fallback support"""
    return OpenAIClientWithFallback()
