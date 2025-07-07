# core/base_agent.py 
from typing import Dict, Any
from data.llm_interface import LLMInterface
from data.database import DatabaseManager

class BaseAgent:
    def __init__(self, name: str, llm: LLMInterface, db: DatabaseManager):
        self.name = name
        self.llm = llm
        self.db = db
        self.analysis_history = []
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
    
    async def participate_in_discussion(self, session_id: str, topic: str, context: str) -> str:
        prompt = f"""
        Você é {self.name}. Participe da discussão sobre: {topic}
        
        Contexto: {context}
        
        Forneça sua perspectiva baseada em sua especialização.
        Seja conciso mas informativo.
        """
        
        response = await self.llm.generate_response(prompt)
        self.db.save_discussion(session_id, self.name, response)
        return response 