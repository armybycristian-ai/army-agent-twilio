from fastapi import FastAPI
from twilio.rest import Client
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/webhook/whatsapp')
async def webhook(request):
    data = await request.form()
    sender = data.get('From','').replace('whatsapp:','')
    msg = data.get('Body','')
    if sender != os.getenv('MY_PERSONAL_NUMBER'):
        return {'status':'ignored'}
    c = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    r = c.messages.create(model='claude-opus-4-6', max_tokens=500, system='ARMY Agent. 3-4 líneas, español, directo.', messages=[{'role':'user','content':msg}])
    Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN')).messages.create(from_=os.getenv('TWILIO_WHATSAPP_NUMBER'), to=f'whatsapp:{sender}', body=r.content[0].text)
    return {'status':'ok'}
