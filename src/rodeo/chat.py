import os
import json
import requests

class Chat:
    def __init__(self, session_file):
        self.session_file = os.path.expanduser(session_file)
        self.messages = self._load_session()
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_url = "https://api.anthropic.com/v1/messages"

    def _load_session(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return []

    def _save_session(self):
        with open(self.session_file, 'w') as f:
            json.dump(self.messages, f)

    def clear_session(self):
        self.messages = []
        self._save_session()

    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        
        response = requests.post(
            self.api_url,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-sonnet-20240229",
                "messages": self.messages,
                "max_tokens": 1000
            }
        )
        
        response.raise_for_status()
        assistant_message = response.json()['content'][0]['text']
        self.messages.append({"role": "assistant", "content": assistant_message})
        self._save_session()
        return assistant_message
