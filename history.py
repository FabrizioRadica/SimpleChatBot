"""
SimpleChatBot - GIGI

Ollama Web Interface
Fabrizio Radica - 2025
Questo script implementa un'interfaccia web per interagire con il modello Ollama.
L'interfaccia web consente di inviare messaggi all'assistente Ollama e visualizzare le risposte generate dal modello.

Licenza: MIT

"""

from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
from fastapi import FastAPI, Response, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import json

app = FastAPI()

# HISTORY CHAT
# Controlla che la cartella "chat" esiste, altrimenti la crea
CHAT_DIR = Path("chat")
CHAT_DIR.mkdir(exist_ok=True)

class Message(BaseModel):
    role: str
    content: str

# Modello per lo storico della chat
class ChatHistory(BaseModel):
    messages: List[Message] = []

# Funzioni per gestire lo storico delle chat in file JSON
def get_chat_history(session_id: str):
    """Legge lo storico della chat da un file JSON"""
    chat_file = CHAT_DIR / f"{session_id}.json"
    if chat_file.exists():
        with open(chat_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Funzioni per gestire lo storico delle chat in file JSON
def save_chat_history(session_id: str, messages: list):
    """Salva lo storico della chat in un file JSON"""
    chat_file = CHAT_DIR / f"{session_id}.json"
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# Endpoint per ottenere lo storico della chat
# Uso FastAPI
@app.get('/chat_history')
async def get_history(session_id: str):
    try:
        history = get_chat_history(session_id)
        return JSONResponse(content=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))