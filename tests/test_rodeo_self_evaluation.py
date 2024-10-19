"""
Self-Evaluation for Rodeo Chatbot

This module implements a self-evaluation mechanism for the Rodeo chatbot. 
Self-evaluation is a meta-testing approach where the AI is used to assess its own outputs.
This method is particularly valuable for AI-driven tools like Rodeo because:

1. Contextual Assessment: It allows for evaluation of responses within specific contexts,
   which is crucial for understanding the appropriateness of AI-generated content.

2. Scalability: As the AI's capabilities expand, its ability to self-evaluate can also improve,
   potentially allowing for more nuanced and accurate assessments over time.

3. Continuous Learning: By analyzing its own responses, the system can potentially
   identify areas for improvement, aiding in the refinement of its language model.

4. Handling Variability: Traditional unit tests may struggle with the inherent variability
   of AI responses. Self-evaluation can assess the quality and relevance of responses,
   even when they differ from predefined expected outputs.

5. Ethical Considerations: Self-evaluation can include checks for adherence to ethical
   guidelines, helping to catch potentially problematic responses.

Limitations to consider:
- The reliability of self-evaluation depends on the AI's own capabilities and potential biases.
- There's a risk of self-reinforcing errors if the evaluation logic is flawed.
- Regular human oversight and validation of the self-evaluation process is crucial.

Usage of this module should be complemented with traditional testing methods and
human review to ensure comprehensive quality assurance of the Rodeo chatbot.
"""
import subprocess
import json

def run_rodeo_command(command):
    result = subprocess.run(['rodeo', command], capture_output=True, text=True)
    return result.stdout.strip()

def evaluate_rodeo_response(context, command, response):
    evaluation_prompt = f"""
    Context: {context}
    Command: {command}
    Response: {response}

    Based on the given context and command, evaluate if the response is reasonable and appropriate.
    Provide your assessment as a JSON object with the following fields:
    - reasonable (boolean): Is the response generally reasonable?
    - relevance (int): On a scale of 1-10, how relevant is the response to the command and context?
    - explanation (string): A brief explanation of your assessment.

    Respond only with the JSON object, no other text.
    """
    
    evaluation_result = run_rodeo_command(evaluation_prompt)
    
    try:
        evaluation_json = json.loads(evaluation_result)
        print(f"\n{'='*50}")
        print(f"Test Case: {command}")
        print(f"Context: {context}")
        print(f"Response: {response}")
        print(f"Result: {evaluation_result}")
        print(f"{'='*50}")
        return evaluation_json
    except json.JSONDecodeError:
        return {"error": "Failed to parse evaluation result as JSON", "raw_result": evaluation_result}

def test_rodeo_self_evaluation():
    # Test case 1: Simple greeting
    context = "The user is starting a new conversation."
    command = "Say hello and introduce yourself briefly."
    response = run_rodeo_command(command)
    evaluation = evaluate_rodeo_response(context, command, response)
    
    print(f"Test Case 1:")
    print(f"Command: {command}")
    print(f"Response: {response}")
    print(f"Evaluation: {json.dumps(evaluation, indent=2)}")
    print()

    # Test case 2: Technical question
    context = "The user is a beginner programmer asking about Python."
    command = "Explain what a Python list is and give an example."
    response = run_rodeo_command(command)
    evaluation = evaluate_rodeo_response(context, command, response)
    
    print(f"Test Case 2:")
    print(f"Command: {command}")
    print(f"Response: {response}")
    print(f"Evaluation: {json.dumps(evaluation, indent=2)}")
    print()

    # Add more test cases as needed

if __name__ == "__main__":
    test_rodeo_self_evaluation()
