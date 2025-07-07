# TradingAgents - Sistema de Negociação Multiagente

## Visão Geral

O TradingAgents é um sistema avançado de negociação que utiliza múltiplos agentes especializados para análise colaborativa de mercado e tomada de decisões de trading. Cada agente possui expertise específica e trabalha em conjunto para produzir estratégias de negociação robustas.

## Arquitetura do Sistema

### 1. Equipe de Analistas
- **Analista Fundamentalista**: Avalia métricas financeiras e valor intrínseco
- **Analista de Sentimentos**: Monitora sentimento de mercado e mídias sociais
- **Analista de Notícias**: Interpreta impactos macroeconômicos e eventos globais
- **Analista Técnico**: Utiliza indicadores técnicos e padrões de preço

### 2. Equipe de Pesquisa
- **Pesquisador Otimista**: Avalia com viés bullish, identifica oportunidades
- **Pesquisador Pessimista**: Avalia com viés bearish, identifica riscos

### 3. Agentes de Decisão
- **Agente de Negociação**: Compila análises e toma decisões de trading
- **Gestor de Risco**: Avalia riscos de portfólio e operações
- **Gestor de Portfólio**: Aprova/rejeita operações baseado em critérios estratégicos

### 4. Infraestrutura
- **Interface LLM**: Comunicação com modelos de linguagem (Llama, Gemma)
- **Provedor de Dados**: Coleta dados de mercado em tempo real
- **Banco de Dados**: Armazena decisões, análises e discussões
- **Exchange Simulada**: Executa ordens de trading

## Instalação e Configuração

### Pré-requisitos

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar e configurar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo Llama 3.2
ollama pull llama3.2

# Ou baixar modelo Gemma
ollama pull gemma:7b
```

### Arquivo requirements.txt

```txt
asyncio
pandas>=1.5.0
numpy>=1.21.0
yfinance>=0.2.0
textstat>=0.7.0
ollama>=0.1.0
sqlite3
aiofiles>=23.0.0
python-dotenv>=1.0.0
logging
concurrent.futures
threading
dataclasses
enum34
```

### Configuração de Ambiente

```python
# config.py
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TradingConfig:
    # Configurações do modelo LLM
    llm_model: str = "llama3.2"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 500
    
    # Configurações de trading
    max_position_size: int = 1000
    risk_threshold: float = 70.0
    confidence_threshold: float = 60.0
    
    # Configurações de dados
    data_cache_duration: int = 300  # segundos
    market_data_symbols: List[str] = None
    
    # Configurações de monitoramento
    monitoring_interval: int = 300  # segundos
    alert_threshold: float = 2.0  # % de mudança
    
    # Configurações de banco de dados
    database_path: str = "trading_agents.db"
    
    def __post_init__(self):
        if self.market_data_symbols is None:
            self.market_data_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']

# Configuração de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'trading_agents.log',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```

## Guia de Uso

### 1. Inicialização Básica

```python
import asyncio
from trading_agents import TradingAgentsSystem

async def main():
    # Inicializa o sistema
    system = TradingAgentsSystem(model_name="llama3.2")
    
    # Analisa um símbolo
    result = await system.analyze_symbol('AAPL')
    
    # Mostra resultados
    print(f"Decisão: {result['trading_decision']['action']}")
    print(f"Confiança: {result['trading_decision']['confidence']:.1f}%")
    print(f"Aprovado: {result['approval']}")

# Executa
asyncio.run(main())
```

### 2. Sessão de Trading Completa

```python
async def run_trading_session():
    system = TradingAgentsSystem()
    
    # Lista de símbolos para análise
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    # Executa sessão
    results = await system.run_trading_session(symbols)
    
    # Processa resultados
    for symbol, result in results['results'].items():
        if 'error' not in result:
            decision = result['trading_decision']
            print(f"{symbol}: {decision['action']} - {decision['confidence']:.1f}%")

asyncio.run(run_trading_session())
```

### 3. Monitoramento em Tempo Real

```python
from trading_agents import TradingAgentsSystem, RealTimeMonitor

def start_monitoring():
    system = TradingAgentsSystem()
    monitor = RealTimeMonitor(system)
    
    # Inicia monitoramento (verifica a cada 5 minutos)
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    monitor.start_monitoring(symbols, interval=300)
    
    # Executa por 1 hora
    import time
    time.sleep(3600)
    
    # Para monitoramento
    monitor.stop_monitoring()

start_monitoring()
```

### 4. Configuração Avançada

```python
# Configuração customizada
config = TradingConfig(
    llm_model="gemma:7b",
    llm_temperature=0.5,
    max_position_size=500,
    risk_threshold=60.0,
    confidence_threshold=70.0
)

# Sistema com configuração customizada
system = TradingAgentsSystem(
    model_name=config.llm_model,
    config=config
)
```

## Fluxo de Operação

### 1. Coleta de Dados
- Dados de mercado em tempo real
- Indicadores técnicos
- Sentimento de mercado
- Notícias e eventos

### 2. Análise Multiagente
- Cada analista avalia os dados com sua expertise
- Análises paralelas para eficiência
- Confiança individual de cada agente

### 3. Pesquisa Crítica
- Pesquisadores avaliam análises com viés específico
- Identificação de riscos e oportunidades
- Questionamento de premissas

### 4. Discussão Colaborativa
- Agentes discutem findings em rodadas estruturadas
- Síntese de informações
- Resolução de conflitos

### 5. Decisão de Trading
- Agente de trading agrega todas as análises
- Votação ponderada por confiança
- Decisão final com justificativa

### 6. Gestão de Risco
- Avaliação de volatilidade e liquidez
- Cálculo de risk score
- Recomendações de mitigação

### 7. Aprovação de Portfólio
- Gestor avalia decisão vs. critérios estratégicos
- Aprovação/rejeição baseada em risco e confiança
- Justificativa da decisão

### 8. Execução
- Submissão de ordens à exchange
- Monitoramento de execução
- Registro de performance

## Componentes Técnicos

### Base de Dados

```sql
-- Tabela de decisões
CREATE TABLE trading_decisions (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    action TEXT,
    quantity INTEGER,
    price REAL,
    confidence REAL,
    reasoning TEXT,
    risk_level TEXT,
    timestamp DATETIME,
    agent_type TEXT
);

-- Tabela de avaliações de risco
CREATE TABLE risk_assessments (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    risk_score REAL,
    volatility REAL,
    liquidity_score REAL,
    correlation_risk REAL,
    recommendation TEXT,
    timestamp DATETIME
);

-- Tabela de discussões
CREATE TABLE agent_discussions (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    agent_name TEXT,
    message TEXT,
    timestamp DATETIME
);
```

### Métricas de Performance

```python
# Métricas de trading
- Taxa de aprovação de trades
- Precisão das previsões
- Retorno ajustado ao risco
- Drawdown máximo
- Sharpe ratio

# Métricas de agentes
- Confiança média por agente
- Concordância entre agentes
- Tempo de resposta
- Qualidade das análises
```

### Alertas e Notificações

```python
# Configuração de alertas
ALERT_CONFIG = {
    'price_change_threshold': 2.0,  # %
    'volume_spike_threshold': 3.0,  # múltiplo da média
    'rsi_extreme_levels': [20, 80],
    'risk_score_threshold': 85.0,
    'confidence_drop_threshold': 20.0  # %
}
```

## Personalização e Extensões

### 1. Novos Agentes

```python
class CustomAnalyst(BaseAgent):
    def __init__(self, llm: LLMInterface, db: DatabaseManager):
        super().__init__("Analista Customizado", llm, db)
        self.system_prompt = """
        Sua especialização específica aqui...
        """
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementar lógica de análise
        pass
```

### 2. Integração com APIs Externas

```python
class ExternalDataProvider:
    async def get_news_sentiment(self, symbol: str):
        # Integração com API de notícias
        pass
    
    async def get_social_sentiment(self, symbol: str):
        # Integração com API de sentimento
        pass
    
    async def get_economic_indicators(self):
        # Integração com API de indicadores econômicos
        pass
```

### 3. Estratégias Personalizadas

```python
class CustomStrategy:
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
    
    async def evaluate(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Implementar lógica de estratégia
        pass
```

## Monitoramento e Debugging

### 1. Logs Detalhados

```python
import logging

# Configurar logging detalhado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('trading_agents_debug.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Métricas de Sistema

```python
# Monitoramento de performance
- Tempo de análise por símbolo
- Uso de memória
- Tempo de resposta do LLM
- Taxa de erro
- Throughput de operações
```

### 3. Dashboard de Monitoramento

```python
# Implementar dashboard web para visualização
- Status dos agentes
- Performance em tempo real
- Alertas e notificações
- Histórico de decisões
- Análise de risco
```

## Melhores Práticas

### 1. Gestão de Risco
- Sempre validar decisões através do gestor de risco
- Implementar stop-loss automático
- Diversificar portfólio
- Monitorar correlações

### 2. Qualidade dos Dados
- Validar dados de entrada
- Implementar cache inteligente
- Tratar dados ausentes
- Verificar consistência

### 3. Performance
- Usar análises paralelas
- Implementar cache de resultados
- Otimizar consultas de banco
- Monitorar uso de recursos

### 4. Manutenibilidade
- Documentar decisões
- Versionamento de modelos
- Testes automatizados
- Backup de dados

## Troubleshooting

### Problemas Comuns

1. **Modelo LLM não encontrado**
   ```bash
   ollama pull llama3.2
   ```

2. **Erro de conexão com banco de dados**
   ```python
   # Verificar permissões do arquivo
   chmod 666 trading_agents.db
   ```

3. **Timeout em análises**
   ```python
   # Ajustar timeout
   config.llm_timeout = 60  # segundos
   ```

4. **Erro de memória**
   ```python
   # Reduzir batch size
   config.max_concurrent_analyses = 2
   ```

### Logs de Debug

```python
# Ativar logs detalhados
export TRADING_AGENTS_DEBUG=1

# Verificar logs
tail -f trading_agents.log
```

## Roadmap de Desenvolvimento

### Versão 1.1 (Próxima Release)
- **Integração com Exchange Real**: Suporte para Binance, Coinbase Pro
- **Backtesting Avançado**: Sistema de teste histórico com métricas detalhadas
- **Interface Web**: Dashboard interativo para monitoramento
- **Alertas Push**: Notificações em tempo real via Telegram/Discord

### Versão 1.2 (Médio Prazo)
- **Machine Learning**: Modelos de predição complementares aos LLMs
- **Análise de Criptomoedas**: Suporte especializado para crypto markets
- **Portfolio Rebalancing**: Rebalanceamento automático de portfólio
- **API REST**: Interface para integração com sistemas externos

### Versão 1.3 (Longo Prazo)
- **Multi-Exchange**: Operação simultânea em múltiplas exchanges
- **Arbitragem**: Detecção e execução automática de oportunidades
- **Social Trading**: Compartilhamento de estratégias entre usuários
- **IA Generativa**: Geração automática de relatórios e insights

## Contribuição

### Como Contribuir

1. **Fork do repositório**
   ```bash
   git clone https://github.com/seu-usuario/trading-agents.git
   cd trading-agents
   ```

2. **Configurar ambiente de desenvolvimento**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   pip install -r requirements-dev.txt
   ```

3. **Executar testes**
   ```bash
   pytest tests/ -v
   python -m pytest --cov=trading_agents tests/
   ```

4. **Criar branch para feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

5. **Commit e push**
   ```bash
   git add .
   git commit -m "Adiciona nova funcionalidade"
   git push origin feature/nova-funcionalidade
   ```

### Diretrizes de Contribuição

- Seguir PEP 8 para código Python
- Adicionar testes para novas funcionalidades
- Documentar funções e classes
- Manter compatibilidade com versões anteriores
- Atualizar README se necessário

### Tipos de Contribuição

- **Bug fixes**: Correções de bugs identificados
- **Features**: Novas funcionalidades
- **Documentação**: Melhorias na documentação
- **Performance**: Otimizações de performance
- **Testes**: Adição de testes unitários

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 TradingAgents

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contato e Suporte

### Comunidade

- **GitHub Issues**: [Reportar bugs ou solicitar features](https://github.com/seu-usuario/trading-agents/issues)
- **Discord**: [Servidor da comunidade](https://discord.gg/trading-agents)
- **Telegram**: [Grupo de discussão](https://t.me/trading_agents)

### Documentação Adicional

- **Wiki**: [Documentação técnica detalhada](https://github.com/seu-usuario/trading-agents/wiki)
- **Tutoriais**: [Guias passo a passo](https://github.com/seu-usuario/trading-agents/wiki/Tutorials)
- **FAQ**: [Perguntas frequentes](https://github.com/seu-usuario/trading-agents/wiki/FAQ)

### Suporte Comercial

Para suporte comercial, integrações customizadas ou consultoria:
- **Email**: support@trading-agents.com
- **LinkedIn**: [Perfil da empresa](https://linkedin.com/company/trading-agents)

---

**Disclaimer**: Este sistema é para fins educacionais e de pesquisa. Trading envolve riscos significativos e você pode perder todo o seu capital. Sempre faça sua própria pesquisa e consulte um consultor financeiro qualificado antes de tomar decisões de investimento.

---

*Última atualização: Dezembro 2024*
*Versão: 1.0.0*