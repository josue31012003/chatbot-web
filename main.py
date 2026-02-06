from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from chatbot import ChatbotSeguridad

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(title="Chatbot de Seguridad y Prevención")

# Inicializa el chatbot
bot = ChatbotSeguridad()

class Pregunta(BaseModel):
    mensaje: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
def chat(p: Pregunta):
    respuesta = bot.preguntar(p.mensaje)
    return {"respuesta": respuesta}
