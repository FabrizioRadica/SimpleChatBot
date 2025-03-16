import requests
import ollama
from fastapi import FastAPI, Response, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Monta la cartella "static" come file statici
app.mount("/static", StaticFiles(directory="static"), name="static")

class Query(BaseModel):
    api_system_prompt: str = "Ti chiami Gigi e sei un assistente molto preparato."
    api_chatname: str = "Chat di Gigi"
    assistant_name: str = "Gigi"
    api_prompt: str = ""
    api_model: str = "llama3.1"
    api_temperature: float = 0.7
    api_usechathistory: bool = False

#root del sito
@app.get('/', response_class=HTMLResponse)
async def main(request: Request,  query: Query = Depends()):
    return templates.TemplateResponse('index.html', {
        'request': request, 
        'assistant_name': query.assistant_name,
        'ai_model': query.api_model,
        'chat_name': query.api_chatname
    })

#chiamata a ollama
@app.get('/generate') 
async def ollama_chat(query: Query = Depends()):
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
            },
        )
        
        return Response(content=res["message"]["content"].strip(), media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))