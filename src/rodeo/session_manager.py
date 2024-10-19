import os
import json

class SessionManager:
    def __init__(self, session_file):
        self.session_file = os.path.expanduser(session_file)
        self.session_data = self.load_session()

    def load_session(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return {"history": []}

    def save_session(self):
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f)

    def add_message(self, role, content):
        self.session_data["history"].append({"role": role, "content": content})
        self.save_session()

    def get_history(self):
        return self.session_data["history"]

    def clear_history(self):
        self.session_data["history"] = []
        self.save_session()
