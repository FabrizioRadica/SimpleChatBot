import requests
import ollama
from fastapi import FastAPI, Response, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional,ClassVar
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import base64
from pathlib import Path
# Importa le funzioni per la gestione dello storico della chat
from history import get_chat_history,save_chat_history

app = FastAPI()

# Configura la cartella "templates" per i file HTML
templates = Jinja2Templates(directory="templates")
# Monta la cartella "static" come file statici
app.mount("/static", StaticFiles(directory="static"), name="static")
 
class ollama_model(BaseModel):
    model: ClassVar[list[str]] = ["llama3.1", "llama3.2-vision:11b"]

# Configurazione di default per la chiamata a Ollama
# Modifica i valori di default se necessario
# Per ulteriori informazioni sui parametri di configurazione, consulta la documentazione di Ollama
class ollama_query(BaseModel):
    assistant_name: str = "Gigi"
    api_system_prompt: str = "Ti chiami Gigi e sei un assistente molto preparato."
    api_chatname: str = "Chat di Gigi"
    api_prompt: str = ""
    api_model: str = ollama_model.model[1]
    api_temperature: float = 0.7
    api_top_p: float = 0.9
    api_top_k: int = 40
    api_max_tokens: int = 2048
    api_context_window: int = 4096
    api_usechathistory: bool = False
    session_id: str = "default"
    
class Theme(BaseModel):
    name: str = "terminal-theme.css"  

# Controlla che la cartella "chat" esiste, altrimenti la crea
CHAT_DIR = Path("images")
CHAT_DIR.mkdir(exist_ok=True)

def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
     
#root del sito
@app.get('/', response_class=HTMLResponse)
async def main(request: Request,  query: ollama_query = Depends(), theme: Theme =Depends()):
    return templates.TemplateResponse('index.html', {
        'request': request, 
        'assistant_name': query.assistant_name,
        'ai_model': query.api_model,
        'chat_name': query.api_chatname,
        'theme_name' : theme.name
    })


"""
#Semplice chiamata a ollama senza history
@app.get('/generate') 
async def simple_ollama_chat(query: Query = Depends()):
    try:
        system_prompt= {"role": "system", "content": query.api_system_prompt}
        user_messages = {"role": "user", "content": query.api_prompt}
        
        api_message = [system_prompt, user_messages]
        res = ollama.chat(
            model=query.api_model,
            messages=api_message,
            stream=False,
            options={
                "temperature": query.api_temperature,
                "top_p": query.api_top_p,
                "top_k": query.api_top_k,
                "num_predict": query.api_max_tokens,
                "context_window": query.api_context_window
            },
        )
        
        return Response(content=res["message"]["content"].strip(), media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""  
    
#Chiamata a ollama con history
@app.get('/generate') 
async def ollama_chat(query: ollama_query = Depends()):
    try:
        base64_image = encode_image_to_base64("images/palermo.jpg")
       # Ottieni lo storico della chat dal file
        chat_history = get_chat_history(query.session_id)
        system_prompt = query.api_system_prompt
        
        # Inizializza lo storico della chat se non esiste
        if not chat_history:
            # Aggiungi il messaggio di sistema come primo messaggio
            chat_history.append({"role": "system", "content": system_prompt})
        elif chat_history[0]["role"] == "system":
            # Aggiorna il messaggio di sistema esistente con il nuovo contesto
            chat_history[0]["content"] = system_prompt
        
        # Aggiungi il messaggio dell'utente allo storico
        user_message = {"role": "user", "content": query.api_prompt, "images": [base64_image]}
        chat_history.append(user_message)
                
        # Usa l'intero storico della chat per la richiesta a Ollama
        res = ollama.chat(
            model=query.api_model,
            #format= image_archive.model_json_schema(),
            messages=chat_history,
            options={
                "temperature": query.api_temperature,
                "top_p": query.api_top_p,
                "top_k": query.api_top_k,
                "num_predict": query.api_max_tokens,
                "context_window": query.api_context_window
            },
            stream=False
        )
        
        # Ottieni la risposta dell'assistente
        ai_response = res["message"]["content"].strip()
                
        # Aggiungi la risposta dell'assistente allo storico
        assistant_message = {
            "role": "assistant", 
            "content": ai_response,
            "images": [base64_image]
        }
        chat_history.append(assistant_message)
        
        # Salva lo storico aggiornato nel file
        save_chat_history(query.session_id, chat_history)
        
        # Restituisci la risposta dell'assistente
        return Response(content=assistant_message["content"], media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))