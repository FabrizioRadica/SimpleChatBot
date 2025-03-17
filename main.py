"""
SimpleChatBot - GIGI

Ollama Web Interface
Fabrizio Radica - 2025
Questo script implementa un'interfaccia web per interagire con il modello Ollama.
L'interfaccia web consente di inviare messaggi all'assistente Ollama e visualizzare le risposte generate dal modello.

Main Features:
- Interfaccia web per inviare messaggi all'assistente Ollama
- Visualizzazione delle risposte generate dal modello Ollama
- Gestione dello storico della chat
- Configurazione dei parametri di Ollama tramite l'interfaccia web
- Supporto per l'uso di Computer Vision (Vision API)

Licenza: MIT

"""

import requests
import ollama
from fastapi import FastAPI, Response, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional,ClassVar
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from pathlib import Path
# Importa le funzioni per la gestione dello storico della chat
from history import get_chat_history,save_chat_history
from utils import encode_image_to_base64

app = FastAPI()

# Configura la cartella "templates" per i file HTML
templates = Jinja2Templates(directory="templates")

# Monta la cartella "static" come file statici
app.mount("/static", StaticFiles(directory="static"), name="static")

# Controlla che la cartella "chat" esiste, altrimenti la crea
IMG_DIR = Path("images")
IMG_DIR.mkdir(exist_ok=True)
 
class ollama_model(BaseModel):
    model: ClassVar[list[str]] = ["llama3.1", "llama3.2-vision:11b","llava:7b"]

class ollama_images(BaseModel):
    images: ClassVar[list[str]] = ["images/palermo.jpg", "images/roma.jpg", "images/milano.jpg"]
    
class Theme(BaseModel):
    name: str = "terminal-theme.css" 

# Configurazione di default per la chiamata a Ollama
# Modifica i valori di default se necessario
# Per ulteriori informazioni sui parametri di configurazione, consulta la documentazione di Ollama
class ollama_query(BaseModel):
    assistant_name: str = "Gigi"
    api_system_prompt: str = "Ti chiami Gigi e sei un assistente molto preparato."
    api_chatname: str = "Chatta con Gigi, il tuo assistente preferito!"
    api_prompt: str = ""
    api_model: str = ollama_model.model[1]
    api_temperature: float = 0.7
    api_top_p: float = 0.9
    api_top_k: int = 40
    api_max_tokens: int = 2048
    api_context_window: int = 4096
    #api_use_chathistory: bool = False
    api_use_computervision: bool = True  #computer vision
    session_id: str = "default"
     
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
        
        # Se l'API Computer Vision è attiva, codifica l'immagine selezionata in base64
        if query.api_use_computervision:
            # Usa solo l'immagine selezionata dal parametro vision_image
            base64_image = [encode_image_to_base64(ollama_images.images[1])]
            user_message = {"role": "user", "content": query.api_prompt, "images": base64_image}
        else:
            user_message = {"role": "user", "content": query.api_prompt}
            
        chat_history.append(user_message)
                
        # Usa l'intero storico della chat per la richiesta a Ollama
        res = ollama.chat(
            model=query.api_model,
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
            "content": ai_response
        }
        chat_history.append(assistant_message)
        
        # Salva lo storico aggiornato nel file
        save_chat_history(query.session_id, chat_history)
        
        # Restituisci la risposta dell'assistente
        return Response(content=assistant_message["content"], media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))