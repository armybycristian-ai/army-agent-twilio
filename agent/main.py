from fastapi import FastAPI, Request
from twilio.rest import Client
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MY_PERSONAL_NUMBER = os.getenv("MY_PERSONAL_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

if not all([ANTHROPIC_API_KEY, MY_PERSONAL_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER]):
    raise ValueError("Missing required environment variables")

anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres ARMY Agent, asistente de Cristian Fuy (Cris), especialista en AI Marketing y Producción Audiovisual.
Respuesta: 3-4 líneas máximo en WhatsApp. Español siempre. Tono directo, sin relleno. Tuteo.
Contexto: Cris opera desde Mollina, Málaga. Clientes: Canal TV Local, SleepZone, Campus Deportivo Toni Moreno. Equipo: Sony A7III, gimbal, iPhone 17 Pro Max, HiggsField Pro, CapCut Pro."""

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/whatsapp")
async def webhook_whatsapp(request: Request):
    try:
        data = await request.form()
        sender = data.get("From", "").replace("whatsapp:", "")
        message = data.get("Body", "")
        
        if sender != MY_PERSONAL_NUMBER:
            return {"status": "ignored"}
        
        response = anthropic_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}]
        )
        
        reply = response.content[0].text
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{sender}",
            body=reply
        )
        return {"status": "success"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}