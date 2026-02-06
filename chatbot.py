import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Verificación explícita (para evitar errores silenciosos)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no encontrada. Revisa el archivo .env")

MODEL_NAME = "gpt-4o-mini"

SYSTEM_PROMPT = """
Eres un asistente especializado en seguridad y prevención de riesgos.

Responde de forma:
- Clara
- Técnica pero comprensible
- Profesional y didáctica

Siempre en español.
"""

# Inicializar cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

class ChatbotSeguridad:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def preguntar(self, pregunta: str) -> str:
        self.messages.append(
            {"role": "user", "content": pregunta}
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=self.messages,
            temperature=0.3
        )

        respuesta = response.choices[0].message.content

        self.messages.append(
            {"role": "assistant", "content": respuesta}
        )

        return respuesta
