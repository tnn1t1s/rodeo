import pytest
from unittest.mock import patch, MagicMock
from src.rodeo.chat import Chat

@pytest.fixture
def mock_requests():
    with patch('src.rodeo.chat.requests') as mock:
        yield mock

def test_chat_initialization():
    chat = Chat("test_session.json")
    assert chat.session_file == "test_session.json"
    assert chat.messages == []

def test_get_response(mock_requests):
    chat = Chat("test_session.json")
    mock_response = MagicMock()
    mock_response.json.return_value = {"content": [{"text": "Test response"}]}
    mock_requests.post.return_value = mock_response

    response = chat.get_response("Test prompt")

    assert response == "Test response"
    assert len(chat.messages) == 2
    assert chat.messages[0] == {"role": "user", "content": "Test prompt"}
    assert chat.messages[1] == {"role": "assistant", "content": "Test response"}

def test_clear_session():
    chat = Chat("test_session.json")
    chat.messages = [{"role": "user", "content": "Test"}]
    
    chat.clear_session()
    
    assert chat.messages == []

