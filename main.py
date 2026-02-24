import os
import json
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from agent import run_agent_trace 

load_dotenv(override=True)

try:
    from langfuse.decorators import langfuse_context
    print("✅ ESTATUS: Langfuse v3 Conectado. Monitoreo activo.")
except (ImportError, ModuleNotFoundError):
    print("⚠️ MODO LOCAL: Langfuse no detectado. Continuando sin telemetría.")
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

@server.post("/chat")
async def chat_endpoint(request: ChatRequest, user: dict = Depends(get_current_user)):
    """Endpoint de streaming con manejo de Server-Sent Events (SSE)."""
    async def event_generator():
        try:
            agent_stream = await run_agent_trace(request.message)
            
            async for event in agent_stream:
                yield f"data: {json.dumps(event, default=serialize_ai_message)}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'error': 'Agent Execution Failure', 'details': str(e)})}\n\n"
        finally:
            langfuse_context.flush()

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "═"*60)
    print("🚀 AMAZON FINANCIAL AGENT - DEPLOYED")
    print(f"🌍 ENDPOINT: http://localhost:8000/chat")
    print("═"*60 + "\n")
    uvicorn.run(server, host="0.0.0.0", port=8000)
