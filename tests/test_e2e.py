import pytest
import subprocess
import os

@pytest.fixture
def temp_session_file(tmp_path):
    return str(tmp_path / "test_session.json")

def run_rodeo_command(command, session_file, input_text=None):
    if input_text:
        process = subprocess.Popen(
            ['echo', input_text],
            stdout=subprocess.PIPE
        )
        result = subprocess.run(
            ['python', '-m', 'src.rodeo.cli', '--session', session_file] + command.split(),
            stdin=process.stdout,
            capture_output=True,
            text=True
        )
    else:
        result = subprocess.run(
            ['python', '-m', 'src.rodeo.cli', '--session', session_file] + command.split(),
            capture_output=True,
            text=True
        )
    return result

def test_basic_conversation(temp_session_file):
    # First interaction
    result = run_rodeo_command("What is Python?", temp_session_file)
    assert "programming language" in result.stdout.lower()

    # Follow-up question
    result = run_rodeo_command("What year was it created?", temp_session_file)
    assert "1991" in result.stdout

def test_clear_session(temp_session_file):
    # Have a conversation
    run_rodeo_command("What is Python?", temp_session_file)
    
    # Clear the session
    result = run_rodeo_command("--clear", temp_session_file)
    assert "Session cleared" in result.stdout

    # Check that the session is indeed cleared
    result = run_rodeo_command("What year was it created?", temp_session_file)
    assert "1991" not in result.stdout  # It shouldn't remember the previous context

def test_piped_input(temp_session_file):
    result = run_rodeo_command("Acknowledge the input", temp_session_file, input_text="Hello, Rodeo!")
    
    print(f"Chatbot response: {result.stdout}")  # This will print the full response for debugging
    
    response_lower = result.stdout.lower()
    
    assert any(word in response_lower for word in ["input", "acknowledge", "received", "got", "understand"]), "The response should indicate acknowledgment of the input"
    assert len(response_lower) > 10, "The response should be more than a few characters long"
    assert "hello" not in response_lower, "The response should not repeat the input verbatim"
