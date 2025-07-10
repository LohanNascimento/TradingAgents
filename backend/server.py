from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import asyncio
import json
import logging
import sys
import os
from datetime import datetime

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.orchestrator import TradingAgentsSystem
from data.database import AsyncDatabaseManager
from utils.helpers import batcher

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TradingAgents API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexões WebSocket ativas
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Nova conexão WebSocket. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Conexão WebSocket removida. Total: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: Dict[str, Any]):
        message_json = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Erro ao enviar mensagem WebSocket: {e}")

manager = ConnectionManager()

# Sistema de trading
trading_system = None

@app.on_event("startup")
async def startup_event():
    global trading_system
    trading_system = TradingAgentsSystem(model_name="llama3.2")
    logger.info("Sistema TradingAgents inicializado")

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/agents")
async def get_agents():
    """Retorna informações sobre todos os agentes"""
    agents_info = []
    for agent in trading_system.all_agents:
        agent_data = {
            "name": agent.name,
            "type": agent.__class__.__name__,
            "total_analyses": len(getattr(agent, 'analysis_history', [])),
            "last_analysis": getattr(agent, 'analysis_history', [{}])[-1].get('timestamp') if hasattr(agent, 'analysis_history') and agent.analysis_history else None
        }
        agents_info.append(agent_data)
    
    return {"agents": agents_info}

@app.post("/api/analyze")
async def start_analysis(symbols: List[str]):
    """Inicia uma nova análise para os símbolos fornecidos"""
    if not symbols:
        return JSONResponse(content={"error": "Nenhum símbolo fornecido"}, status_code=400)
    
    logger.info(f"Iniciando análise para símbolos: {symbols}")
    
    # Iniciar análise em background
    asyncio.create_task(run_analysis_with_updates(symbols))
    
    return {
        "message": "Análise iniciada",
        "symbols": symbols,
        "timestamp": datetime.now()
    }

async def run_analysis_with_updates(symbols: List[str]):
    """Executa análise e envia atualizações via WebSocket"""
    try:
        # Notificar início da análise
        await manager.broadcast({
            "type": "analysis_started",
            "symbols": symbols,
            "timestamp": datetime.now().isoformat()
        })

        # Executar análise símbolo por símbolo
        session_id = f"session_{int(datetime.now().timestamp())}"
        
        for symbol in symbols:
            # Notificar início da análise do símbolo
            await manager.broadcast({
                "type": "symbol_analysis_started",
                "symbol": symbol,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            })

            # Executar análise do símbolo
            result = await trading_system.analyze_symbol(symbol)
            
            # Enviar discussões em tempo real
            for i, message in enumerate(result.get('discussion_messages', [])):
                parts = message.split(': ', 1)
                agent_name = parts[0] if len(parts) > 1 else "Sistema"
                agent_message = parts[1] if len(parts) > 1 else message
                
                await manager.broadcast({
                    "type": "agent_message",
                    "session_id": session_id,
                    "symbol": symbol,
                    "agent_name": agent_name,
                    "message": agent_message,
                    "timestamp": datetime.now().isoformat(),
                    "message_index": i
                })
                
                # Pequeno delay para simular conversa em tempo real
                await asyncio.sleep(0.5)
            
            # Enviar resultado final da análise
            await manager.broadcast({
                "type": "symbol_analysis_completed",
                "symbol": symbol,
                "session_id": session_id,
                "result": {
                    "trading_decision": result.get('trading_decision'),
                    "risk_assessment": result.get('risk_assessment'),
                    "approval": result.get('approval'),
                    "approval_reasoning": result.get('approval_reasoning'),
                    "executed_trade": result.get('executed_trade'),
                    "analyses_count": len(result.get('analyses', [])),
                    "market_data": result.get('market_data')
                },
                "timestamp": datetime.now().isoformat()
            })

        # Notificar fim da análise completa
        await manager.broadcast({
            "type": "analysis_completed",
            "session_id": session_id,
            "symbols": symbols,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Erro durante análise: {e}")
        await manager.broadcast({
            "type": "analysis_error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })

@app.get("/api/portfolio")
async def get_portfolio():
    """Retorna performance do portfólio"""
    return trading_system.get_portfolio_performance()

@app.get("/api/agents/performance")
async def get_agents_performance():
    """Retorna performance dos agentes"""
    return trading_system.get_agent_performance()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo de mensagens recebidas (para debug)
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)