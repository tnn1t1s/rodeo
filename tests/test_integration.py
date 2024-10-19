import os
import pytest
import subprocess
import json
from unittest.mock import patch, MagicMock
from typing import List, Dict
from src.rodeo.chat import Chat
from src.rodeo.cli import process_command

class RodeoTestCase:
    def __init__(self, prompt: str, expected_outcome: str, threshold: float = 0.7):
        self.prompt = prompt
        self.expected_outcome = expected_outcome
        self.threshold = threshold

def run_rodeo_command(prompt: str) -> str:
    result = subprocess.run(['python', '-m', 'src.rodeo.cli', prompt], 
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()

def evaluate_response(chat: Chat, prompt: str, actual_response: str, expected_outcome: str) -> float:
    evaluation_prompt = f"""
    Given the following:
    
    Prompt: {prompt}
    Actual Response: {actual_response}
    Expected Outcome: {expected_outcome}

    On a scale of 0 to 1, how well does the actual response match the expected outcome?
    Provide only a numeric score without any explanation.
    """

    score_response = chat.get_response(evaluation_prompt)
    
    try:
        score = float(score_response.strip())
        return min(max(score, 0), 1)  # Ensure the score is between 0 and 1
    except ValueError:
        print(f"Error parsing score: {score_response}")
        return 0

def run_tests(test_cases: List[RodeoTestCase], session_file: str) -> Dict[str, Dict[str, float]]:
    chat = Chat(session_file)
    results = {}
    for i, test_case in enumerate(test_cases, 1):
        print(f"Running test case {i}...")
        chat.clear_session()  # Clear session before each test
        actual_response = run_rodeo_command(test_case.prompt)
        score = evaluate_response(chat, test_case.prompt, actual_response, test_case.expected_outcome)
        passed = score >= test_case.threshold
        results[f"Test {i}"] = {
            "score": score,
            "passed": passed
        }
        print(f"Test {i} {'passed' if passed else 'failed'} with score {score:.2f}")
    return results

# Define test cases
test_cases = [
    RodeoTestCase(
        prompt="Summarize the key features of Python in 3 bullet points",
        expected_outcome="The response should include 3 bullet points highlighting key features of Python, such as readability, extensive libraries, and dynamic typing.",
    ),
    RodeoTestCase(
        prompt="Translate 'Hello, how are you?' to French",
        expected_outcome="The response should be the French translation: 'Bonjour, comment allez-vous?'",
        threshold=0.8
    ),
    RodeoTestCase(
        prompt="What is 15 * 24?",
        expected_outcome="The response should include the correct calculation: 360",
        threshold=0.9
    )
]

@pytest.fixture
def mock_chat():
    with patch('src.rodeo.chat.Chat') as mock:
        yield mock

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

def test_cli_integration(mock_chat, mock_subprocess_run):
    mock_chat_instance = MagicMock()
    mock_chat_instance.get_response.return_value = "Mocked response"
    mock_chat.return_value = mock_chat_instance

    # Mock the subprocess.run to return our expected output
    mock_process = MagicMock()
    mock_process.stdout = "Mocked response"
    mock_subprocess_run.return_value = mock_process

    result = run_rodeo_command("Test prompt")
    assert result == "Mocked response"
    mock_subprocess_run.assert_called_once_with(
        ['python', '-m', 'src.rodeo.cli', 'Test prompt'],
        capture_output=True, text=True, check=True
    )

def test_process_command_integration(mock_chat):
    mock_chat_instance = MagicMock()
    mock_chat_instance.get_response.return_value = "Processed: Test input"
    mock_chat.return_value = mock_chat_instance

    result = process_command("Process this: $(cat)", mock_chat_instance, "Test input")
    assert result == "Processed: Test input"
    mock_chat_instance.get_response.assert_called_once_with("Process this: Test input")

def test_chat_session_persistence():
    session_file = "test_session.json"
    chat = Chat(session_file)
    
    # Test that messages are saved
    chat.get_response("Hello")
    chat.get_response("How are you?")
    
    # Create a new chat instance with the same session file
    new_chat = Chat(session_file)
    
    # Check if the messages were loaded
    assert len(new_chat.messages) == 4  # 2 user messages and 2 assistant responses
    
    # Clean up
    os.remove(session_file)

@patch('src.rodeo.cli.Chat')
def test_full_integration(mock_chat):
    mock_chat_instance = MagicMock()
    mock_chat.return_value = mock_chat_instance

    # Mock responses for each test case
    mock_chat_instance.get_response.side_effect = [
        "- Readability\n- Extensive libraries\n- Dynamic typing",
        "Bonjour, comment allez-vous?",
        "The result of 15 * 24 is 360.",
        "0.9",  # Score for the first test
        "1.0",  # Score for the second test
        "1.0",  # Score for the third test
    ]

    session_file = "integration_test_session.json"
    results = run_tests(test_cases, session_file)
    
    # Check if all tests passed
    assert all(result['passed'] for result in results.values())
    
    # Clean up
    if os.path.exists(session_file):
        os.remove(session_file)

if __name__ == "__main__":
    pytest.main([__file__])
