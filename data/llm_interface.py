# data/llm_interface.py 
import asyncio
import ollama
import logging

logger = logging.getLogger(__name__)

class LLMInterface:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.client = ollama.Client()
        
    async def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    system=system_prompt,
                    options={"temperature": 0.7, "num_predict": 500}
                )
            )
            return response['response']
        except Exception as e:
            logger.error(f"Erro ao gerar resposta LLM: {e}")
            return "Erro na análise" 