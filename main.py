import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="Chatbot de Seguridad", version="1.0")

# Si sirves FRONT + API desde el mismo dominio (Render), CORS no es necesario.
# Pero lo dejamos abierto por si luego quieres usar GitHub Pages también.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Prompt base modificable
SYSTEM_PROMPT = """
Eres un chatbot especializado en seguridad industrial y minera.
Respondes únicamente consultas relacionadas con SST, EPP, procedimientos seguros e IPERC.
Si la consulta no está relacionada con seguridad, responde exactamente:
"No estoy autorizado para responder esa consulta."
Responde de forma clara, profesional y concisa.
"""

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en Render (Environment Variables) o en un .env local.")

client = OpenAI(api_key=api_key)

# 👉 Página principal (la web)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Contrato actual: recibe "mensaje"
class ChatRequest(BaseModel):
    mensaje: str

# Endpoint del chat
@app.post("/chat")
def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.mensaje},
        ],
        temperature=0.3,
    )
    return {"respuesta": completion.choices[0].message.content}
