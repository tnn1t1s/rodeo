# Rodeo CLI Chatbot

A command-line interface chatbot that maintains conversation context across multiple invocations.

## Installation

```
pip install -e .
```

## Usage

Basic usage:
```
rodeo-cli "Your prompt here"
```

or pipe input:
```
echo "Your prompt" | rodeo-cli
```

## Session Management Examples

1. Start a conversation:
```
$ rodeo-cli "My name is Alice"
Hello Alice! It's nice to meet you. How can I assist you today?
```

2. Continue the conversation:
```
$ rodeo-cli "What's my name?"
Your name is Alice, as you mentioned earlier.
```

3. Clear the session:
```
$ rodeo-cli --clear
Session cleared.
```

4. Start a new conversation:
```
$ rodeo-cli "What's my name?"
I'm sorry, but I don't have any information about your name. We haven't been introduced in this conversation. Could you please tell me your name?
```

## Unix Pipe Examples

1. Use Rodeo to interpret basic system information:

```
$ uname -a | rodeo-cli "Explain this system information: $(cat)"

[Rodeo's response explaining the uname output, including OS type, kernel version, etc.]
```

This example demonstrates how Rodeo can interpret system information passed through a pipe. The `$(cat)` command substitution reads the piped input and includes it in the prompt sent to Rodeo.

2. Analyze directory contents:

```
$ ls -l | rodeo-cli "Summarize this directory listing. How many items are there, and what types of files do you see? $(cat)"

[Rodeo's response analyzing the directory contents, including:
- Total number of items
- Number of directories
- Number of regular files
- Any special files (symlinks, etc.)
- Largest file (if apparent from the listing)
- Most recent modification (if apparent from the listing)]

## Options

- `--session FILE`: Specify a custom session file (default: ~/.rodeo.session)
- `--clear`: Clear the current session
