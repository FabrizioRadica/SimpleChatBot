# SimpleChatBot
# Simple webapp written in Python, Ollama and FastAPI
# by Fabrizio Radica 2025


A lightweight web interface for interacting with [Ollama](https://ollama.ai/) language models through a clean and responsive chat interface.

## Features

- Clean, modern chat interface with dark theme
- Direct integration with Ollama API
- Customizable system prompts and assistant personality
- Responsive design that works on both desktop and mobile devices
- **Chat history persistence** - conversations are now saved between sessions
- **Session management** - support for multiple conversation threads
- ** New Theme system **
- Simple and intuitive user experience


![immagine](https://github.com/user-attachments/assets/c68e1ed5-c5da-4ca8-b5ec-210e08ea49b4)

![immagine](https://github.com/user-attachments/assets/36da53f1-144b-4938-b9b2-8f1fe82727c4)


## Project Structure

```
├── main.py               # FastAPI backend application
├── history.py            # Chat history management module
├── chat/                 # Directory for stored chat histories (JSON)
├── static/
│   ├── chat.js           # Client-side chat functionality
│   ├── dark_theme.css    # Dark theme styling
│   └── style.css         # Alternative light theme styling
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
   git clone https://github.com/FabrizioRadica/simple-ollama-chat.git
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
- `session_id`: Identifies which conversation history to use (defaults to "default")

You can also change the theme using the `Theme` class:
- `name`: CSS file name for theming (defaults to "dark_theme.css")

## Chat History System

The application now includes a chat history system:

- Conversations are persistently stored as JSON files in the `chat/` directory
- Each conversation thread is identified by a unique session ID
- History is automatically loaded and saved with each interaction
- Full conversation context is sent to the AI model for more coherent responses
- Chat history can be retrieved via the `/chat_history` endpoint

## Planned Features

- Multiple model selection from the UI
- Markdown formatting for AI responses 
- Attachment support
- User authentication
- Theme switching from the UI

## License

This project is free and open-source software released under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). You are free to use, modify, and distribute this software, but you must give appropriate credit to the original author.

## Author

Created by [RadicaDesign](https://www.radicadesign.com)

## Acknowledgments

- [Ollama](https://ollama.ai/) for the lightweight LLM server
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient Python backend

```
    _                _                _  _   _____                
   / \   _ __ ___   (_)  __ _   __ _ | || | | ____|__   __ ___ _ __ 
  / _ \ | '_ ` _ \  | | / _` | / _` || || | |  _| \ \ / // _ \ '__|
 / ___ \| | | | | | | || (_| || (_| || || | | |___ \ V /|  __/ |   
/_/   \_\_| |_| |_| |_| \__, | \__,_||_||_| |_____| \_/  \___|_|   
                        |___/                                      
```
