import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler
from app.models.mistral import MistralHandler

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

@pytest.mark.asyncio
async def test_mistral_handler_generate():
    """Test MistralHandler generation with mocked API response"""
    handler = MistralHandler()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked Mistral response"
    
    # We use post for Mistral, so we need to mock post
    handler.client.post = AsyncMock(return_value=mock_response)
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={
        "choices": [{"message": {"content": "Mocked Mistral response"}}]
    })
    
    result = await handler.generate("Hello")
    assert result == "Mocked Mistral response"
    handler.client.post.assert_called_once()
