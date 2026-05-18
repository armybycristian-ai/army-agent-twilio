import anthropic
import os
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Eres ARMY, el asistente personal de Cristian Fuy (@cristianfuy).

Contexto: Freelancer AI Marketing y Producción Audiovisual en Mollina, Málaga.
Marca: ARMY by Cristian (armybycristian.es)
Clientes activos: Canal TV Local (~700€/mes), SleepZone (350€), Campus Deportivo Toni Moreno, ~9 activos.
Equipo: Sony A7III, gimbal, iPhone 17 Pro Max, HiggsField Pro, CapCut Pro.

Tono:
- Directo, sin relleno motivacional
- Máx 3-4 líneas formato WhatsApp
- Tuteo siempre
- Español siempre"""

class ArmyBrain:
    def __init__(self):
api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
                        raise ValueError("ANTHROPIC_API_KEY not set")
                    self.client = anthropic.Anthropic(api_key=api_key)
    def get_response(self, user_message: str, history: list) -> str:
        messages = history + [{"role": "user", "content": user_message}]
        try:
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=messages
            )
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            return "No response"
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            return f"Error: {str(e)}"
