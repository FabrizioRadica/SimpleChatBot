# SimpleChatBot
# Simple webapp written in Python, Ollama and FastAPI
# by Fabrizio Radica 2025


![immagine](https://github.com/user-attachments/assets/c68e1ed5-c5da-4ca8-b5ec-210e08ea49b4)


A lightweight web interface for interacting with [Ollama](https://ollama.ai/) language models through a clean and responsive chat interface.

## Features

- Clean, modern chat interface with dark theme
- Direct integration with Ollama API
- Customizable system prompts and assistant personality
- Responsive design that works on both desktop and mobile devices
- Simple and intuitive user experience

## Project Structure

```
├── main.py               # FastAPI backend application
├── static/
│   ├── chat.js           # Client-side chat functionality
│   ├── dark_theme.css    # Dark theme styling
│   └── style.css         # Alternative light theme styling (not currently used)
└── templates/
    └── index.html        # Main HTML template
```

## Prerequisites

- Python 3.7+
- FastAPI
- Ollama running locally or on an accessible server
- Modern web browser

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/simple-ollama-chat.git
   cd simple-ollama-chat
   ```

2. Install the required dependencies:
   ```
   pip install fastapi uvicorn jinja2 ollama requests
   ```

3. Make sure Ollama is installed and running with your preferred models

## Usage

1. Start the application:
   ```
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000`

3. Start chatting with the AI assistant

## Configuration

You can modify the default settings in the `Query` class in `main.py`:

- `api_system_prompt`: The system instructions for the AI assistant
- `api_chatname`: The name displayed in the chat window header
- `assistant_name`: The name of the AI assistant
- `api_model`: The default Ollama model to use
- `api_temperature`: Controls randomness in responses (0.0 to 1.0)

## Current Limitations

- **No Chat History**: This version does not yet persist chat history. Each page refresh starts a new conversation.
- Single-turn conversations only (working on multi-turn support)

## Planned Features

- Chat history persistence
- Multiple model selection from the UI
- Markdown formatting for AI responses
- Attachment support
- User authentication

## License

This project is free and open-source software released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Acknowledgments

- [Ollama](https://ollama.ai/) for the lightweight LLM server
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient Python backend


_                _                _  _   _____                
   / \   _ __ ___   (_)  __ _   __ _ | || | | ____|__   __ ___ _ __ 
  / _ \ | '_ ` _ \  | | / _` | / _` || || | |  _| \ \ / // _ \ '__|
 / ___ \| | | | | | | || (_| || (_| || || | | |___ \ V /|  __/ |   
/_/   \_\_| |_| |_| |_| \__, | \__,_||_||_| |_____| \_/  \___|_|   
                        |___/

