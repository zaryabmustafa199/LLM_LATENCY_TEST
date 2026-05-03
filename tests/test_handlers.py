import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler

@pytest.mark.asyncio
async def test_llama_handler_generate():
    """Test LlamaHandler generation with mocked API response"""
    handler = LlamaHandler()
    # Mock the client's chat_completion method
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked Llama response"
    
    handler.client.chat_completion = AsyncMock(return_value=mock_response)
    
    result = await handler.generate("Hello")
    assert result == "Mocked Llama response"
    handler.client.chat_completion.assert_called_once()

@pytest.mark.asyncio
async def test_qwen_handler_generate():
    """Test QwenHandler generation with mocked API response"""
    handler = QwenHandler()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked Qwen response"
    
    handler.client.chat_completion = AsyncMock(return_value=mock_response)
    
    result = await handler.generate("Hello")
    assert result == "Mocked Qwen response"
    handler.client.chat_completion.assert_called_once()

@pytest.mark.asyncio
async def test_gemma_handler_generate():
    """Test GemmaHandler generation with mocked API response"""
    handler = GemmaHandler()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked Gemma response"
    
    handler.client.chat_completion = AsyncMock(return_value=mock_response)
    
    result = await handler.generate("Hello")
    assert result == "Mocked Gemma response"
    handler.client.chat_completion.assert_called_once()
