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

## Unix Pipe Example

Use Rodeo in a Unix pipeline to analyze command output:

```
$ ls -l | rodeo-cli "Summarize this directory listing. How many files are there, and what types?"
Based on the directory listing provided, there are [X] files in total. The types include [list types, e.g., regular files, directories, symlinks]. The largest file appears to be [filename] at [size] bytes.
```

This example demonstrates how Rodeo can be used to analyze and summarize command outputs directly in your terminal.


## Options

- `--session FILE`: Specify a custom session file (default: ~/.rodeo.session)
- `--clear`: Clear the current session
