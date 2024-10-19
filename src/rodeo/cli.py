import sys
import argparse
from rodeo.chat import Chat

def process_command(command: str, chat: Chat, input_text: str = '') -> str:
    """
    Process a command using the Chat instance.
    
    :param command: The command or prompt to process
    :param chat: An instance of the Chat class
    :param input_text: Optional input text (e.g., from piped input)
    :return: The response from the chat
    """
    if '$(cat)' in command and input_text:
        full_command = command.replace('$(cat)', input_text)
    else:
        full_command = command

    return chat.get_response(full_command)

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
        command = " ".join(args.prompt)
        input_text = ''
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
        command = "$(cat)"
    else:
        print("Usage: rodeo [--session FILE] 'Your prompt' or echo 'Your prompt' | rodeo")
        sys.exit(1)

    response = process_command(command, chat, input_text)
    print(response)

if __name__ == "__main__":
    main()
