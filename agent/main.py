from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
import logging
from agent.brain import ArmyBrain
from agent.memory import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ARMY Agent")
brain = ArmyBrain()
memory = MemoryManager()

MY_PERSONAL_NUMBER = os.getenv("MY_PERSONAL_NUMBER", "")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        sender = form_data.get("From", "").replace("whatsapp:", "").replace("+", "")
        message_text = form_data.get("Body", "")
        logger.info(f"Message from {sender}: {message_text}")
        if not sender.endswith(MY_PERSONAL_NUMBER):
            return PlainTextResponse("<?xml version='1.0'?><Response></Response>", media_type="application/xml")
        history = memory.get_history(sender)
        response_text = brain.get_response(message_text, history)
        memory.add_message(sender, "user", message_text)
        memory.add_message(sender, "assistant", response_text)
        xml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{response_text}</Message></Response>'
        return PlainTextResponse(xml, media_type="application/xml")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return PlainTextResponse('<?xml version="1.0"?><Response><Message>Error.</Message></Response>', media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
