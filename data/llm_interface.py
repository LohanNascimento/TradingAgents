# data/llm_interface.py 
import asyncio
import ollama
import logging
import time
# Removi: from utils.cache import make_cache_key, get_cache, set_cache

logger = logging.getLogger(__name__)

class LLMInterface:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.client = ollama.Client()
        self.response_times = []
        # Tenta detectar se há suporte a GPU (Ollama)
        try:
            info = self.client.show(self.model_name)
            self.gpu_enabled = info.get('details', {}).get('gpu', False)
            logger.info(f"Ollama GPU enabled: {self.gpu_enabled}")
        except Exception as e:
            self.gpu_enabled = False
            logger.warning(f"Não foi possível detectar GPU no Ollama: {e}")
        
    async def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        # Removi toda a lógica de cache
        start = time.perf_counter()
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.generate(
                    model=self.model_name,
                    prompt=prompt,
                    system=system_prompt,
                    options={
                        "temperature": 0.7, 
                        "num_predict": 150,
                        "num_ctx": 1024,
                        "num_gpu_layers": 20,
                        "num_thread": 4
                    }
                )
            )
            elapsed = time.perf_counter() - start
            self.response_times.append(elapsed)
            logger.info(f"Tempo de resposta do LLM para o prompt: {elapsed:.2f} segundos")
            return response['response']
        except Exception as e:
            logger.error(f"Erro ao gerar resposta LLM: {e}")
            return "Erro na análise" 