"""
Abstract base class for LLM model handlers

Defines the interface that all model handlers must implement.
"""

from abc import ABC, abstractmethod


class BaseModelHandler(ABC):
    """
    Abstract base class for LLM model handlers
    
    All model implementations (Mistral, Phi, etc.) must inherit from this
    class and implement the generate method.
    """
    
    @abstractmethod
    async def generate(self, query: str) -> str:
        """
        Generate a response from the LLM
        
        Args:
            query: User prompt/question to send to the model
            
        Returns:
            Raw text output from the LLM
            
        Raises:
            Exception: If model inference fails
        """
        pass
