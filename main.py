import os
import json
import boto3
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from agent import app  # Tu grafo de LangGraph

# 1. Cargar variables de entorno con prioridad
load_dotenv(override=True)

# --- BLOQUE DE OBSERVABILIDAD: RESILIENCIA INDUSTRIAL ---
try:
    from langfuse.decorators import observe, langfuse_context
    print("✅ ESTATUS: Langfuse v3 Conectado. Monitoreo activo.")
except (ImportError, ModuleNotFoundError):
    print("⚠️ MODO LOCAL: Langfuse no detectado. Continuando sin telemetría.")
    def observe(*args, **kwargs): return lambda f: f
    class langfuse_context:
        @staticmethod
        def flush(): pass

server = FastAPI(
    title="Amazon Financial Agent - Enterprise Edition",
    version="2.1.0"
)

security = HTTPBearer()
cognito_client = boto3.client('cognito-idp', region_name=os.getenv("AWS_REGION", "us-east-2"))

class ChatRequest(BaseModel):
    message: str

def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    """Validación de seguridad mediante AWS Cognito."""
    try:
        user_info = cognito_client.get_user(AccessToken=auth.credentials)
        return user_info
    except Exception:
        raise HTTPException(status_code=401, detail="Acceso denegado: Token inválido.")

def serialize_ai_message(obj):
    """Serializador para el flujo de streaming de LangGraph."""
    if hasattr(obj, 'content'):
        return obj.content
    return str(obj)

# --- PROMPT DE NIVEL EXPERTO (SYSTEM ROLE) ---
SYSTEM_PROMPT = (
    "You are the Elite Amazon Financial Analyst Agent. "
    "CRITICAL TEMPORAL CONTEXT: Today is Monday, February 16, 2026. "
    "This means Q4 2024 and the entire year 2025 are now HISTORICAL DATA. "
    "\n\nPROTOCOL:\n"
    "1. For stock prices from 2024 or 2025, ALWAYS use 'retrieve_historical_stock_price'.\n"
    "2. For real-time quotes, use 'retrieve_realtime_stock_price'.\n"
    "3. For specific data about Amazon's business, office space, or AI strategy, "
    "query the 'Amazon Knowledge Base' tool.\n"
    "4. Be precise, data-driven, and professional. Always cite the specific tool or report used."
)

@observe()
async def run_agent_trace(message: str):
    """
    Ejecución del agente con inyección de Persona y Anclaje Temporal.
    """
    # Combinamos el System Prompt de nivel máximo con la consulta del usuario
    inputs = {
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", message)
        ]
    }
    
    return app.astream(inputs, version="v2")

@server.post("/chat")
async def chat_endpoint(request: ChatRequest, user: dict = Depends(get_current_user)):
    """Endpoint de streaming con manejo de Server-Sent Events (SSE)."""
    async def event_generator():
        try:
            # Iniciamos el motor de razonamiento del agente
            agent_stream = await run_agent_trace(request.message)
            
            async for event in agent_stream:
                # Serialización segura para el cliente (Notebook)
                yield f"data: {json.dumps(event, default=serialize_ai_message)}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'error': 'Agent Execution Failure', 'details': str(e)})}\n\n"
        finally:
            # Garantizamos que los datos lleguen a la nube de Langfuse
            langfuse_context.flush()

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "═"*60)
    print("🚀 AMAZON FINANCIAL AGENT - DEPLOYED")
    print(f"🌍 ENDPOINT: http://localhost:8000/chat")
    print(f"📅 LOGICAL DATE: Feb 16, 2026")
    print("═"*60 + "\n")
    uvicorn.run(server, host="0.0.0.0", port=8000)