import pytest
from unittest.mock import MagicMock
from src.rodeo.cli import process_command
from src.rodeo.chat import Chat

@pytest.fixture
def mock_chat():
    return MagicMock(spec=Chat)

def test_process_command_with_cat(mock_chat):
    mock_chat.get_response.return_value = "Processed: Hello, World!"
    
    result = process_command("Echo this: $(cat)", mock_chat, "Hello, World!")
    assert result == "Processed: Hello, World!"
    mock_chat.get_response.assert_called_once_with("Echo this: Hello, World!")

def test_process_command_without_cat(mock_chat):
    mock_chat.get_response.return_value = "Translated: Bonjour le monde!"
    
    result = process_command("Translate to French: Hello, World!", mock_chat)
    assert result == "Translated: Bonjour le monde!"
    mock_chat.get_response.assert_called_once_with("Translate to French: Hello, World!")

# Add more tests as needed...

def test_main_with_prompt(mock_chat, monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['rodeo-cli', 'Hello, World!'])
    monkeypatch.setattr('src.rodeo.cli.Chat', lambda _: mock_chat)
    mock_chat.get_response.return_value = "Bonjour le monde!"

    from src.rodeo.cli import main
    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Bonjour le monde!"

def test_main_with_piped_input(mock_chat, monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['rodeo-cli'])
    monkeypatch.setattr('src.rodeo.cli.Chat', lambda _: mock_chat)
    monkeypatch.setattr('sys.stdin.isatty', lambda: False)
    monkeypatch.setattr('sys.stdin.read', lambda: 'Hello, World!')
    mock_chat.get_response.return_value = "Bonjour le monde!"

    from src.rodeo.cli import main
    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Bonjour le monde!"
