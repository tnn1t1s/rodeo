import sys
import argparse
from rodeo.chat import Chat

def main():
    parser = argparse.ArgumentParser(description="Rodeo CLI Chat")
    parser.add_argument("--session", default="~/.rodeo.session", help="Path to session file")
    parser.add_argument("--clear", action="store_true", help="Clear the session")
    parser.add_argument("prompt", nargs="*", help="Prompt for the chat")
    args = parser.parse_args()

    chat = Chat(args.session)

    if args.clear:
        chat.clear_session()
        print("Session cleared.")
        return
    
    if args.prompt:
        prompt = " ".join(args.prompt)
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    else:
        print("Usage: rodeo-cli [--session FILE] 'Your prompt' or echo 'Your prompt' | rodeo-cli")
        sys.exit(1)

    if prompt:
        response = chat.get_response(prompt)
        print(response)

if __name__ == "__main__":
    main()
