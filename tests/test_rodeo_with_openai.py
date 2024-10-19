import subprocess
import json
from openai import OpenAI
import os
import pytest

# Ensure you have set your OpenAI API key in your environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_rodeo_command(command):
    result = subprocess.run(['rodeo', command], capture_output=True, text=True)
    return result.stdout.strip()

def evaluate_with_openai(context, command, response):
    prompt = f"""
    Context: {context}
    Command given to Rodeo: {command}
    Rodeo's response: {response}

    Please evaluate Rodeo's response based on the following criteria:
    1. Relevance: How well does the response address the command and context?
    2. Accuracy: Is the information provided correct and reliable?
    3. Clarity: Is the response clear and easy to understand?
    4. Completeness: Does the response fully address the command?

    Provide your evaluation as a JSON object with the following structure:
    {{
        "relevance": <score from 1-10>,
        "accuracy": <score from 1-10>,
        "clarity": <score from 1-10>,
        "completeness": <score from 1-10>,
        "overall_score": <average of the above scores>,
        "explanation": "<brief explanation of the evaluation>"
    }}

    Respond only with the JSON object, no other text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant tasked with evaluating the quality of responses from another AI system."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

@pytest.fixture
def test_cases():
    return [
        {
            "context": "The user is starting a new conversation.",
            "command": "Say hello and introduce yourself briefly."
        },
        {
            "context": "The user is a beginner programmer asking about Python.",
            "command": "Explain what a Python list is and give an example."
        },
        {
            "context": "The user is asking about the weather.",
            "command": "What's the weather like today in New York?"
        }
    ]

def test_rodeo_with_openai(test_cases):
    for case in test_cases:
        context = case['context']
        command = case['command']
        
        print(f"\n{'='*50}")
        print(f"Test Case: {command}")
        print(f"Context: {context}")
        print(f"{'='*50}")

        rodeo_response = run_rodeo_command(command)
        print(f"Rodeo Response:\n{rodeo_response}\n")

        openai_evaluation = evaluate_with_openai(context, command, rodeo_response)
        print("OpenAI Evaluation:")
        print(json.dumps(openai_evaluation, indent=2))

        # Add some assertions to make this a proper test
        assert isinstance(openai_evaluation, dict), "OpenAI evaluation should return a dictionary"
        assert 'overall_score' in openai_evaluation, "Evaluation should include an overall score"
        assert openai_evaluation['overall_score'] > 5, "Overall score should be greater than 5"

