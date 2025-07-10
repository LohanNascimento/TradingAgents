# Entry point for the TradingAgents system

import asyncio
from services.orchestrator import TradingAgentsSystem

def print_session_results(session_results):
    print("=== RESULTADOS DA SESSÃO ===")
    print(f"ID da Sessão: {session_results['session_id']}")
    print(f"Duração: {session_results['duration']:.2f} segundos")
    print(f"Símbolos analisados: {session_results['summary']['successful_analyses']}")
    print(f"Trades aprovados: {session_results['summary']['approved_trades']}")
    print(f"Trades executados: {session_results['summary']['executed_trades']}")
    print(f"Taxa de aprovação: {session_results['summary']['approval_rate']:.2%}")
    print()
    for symbol, result in session_results['results'].items():
        if 'error' in result:
            print(f"❌ {symbol}: {result['error']}")
            continue
        decision = result['trading_decision']
        print(f"📊 {symbol}:")
        print(f"  Decisão: {decision['action'].value.upper()}")
        print(f"  Quantidade: {decision['quantity']}")
        print(f"  Preço: ${decision['price']:.2f}")
        print(f"  Confiança: {decision['confidence']:.1f}%")
        print(f"  Aprovado: {'✅' if result['approval'] else '❌'}")
        if result['executed_trade']:
            print(f"  Executado: ${result['executed_trade']['executed_price']:.2f}")
        print()

def print_portfolio_performance(system):
    portfolio_perf = system.get_portfolio_performance()
    print("=== PERFORMANCE DO PORTFÓLIO ===")
    for key, value in portfolio_perf.items():
        if key != 'recent_trades':
            print(f"{key}: {value}")
    print()

def print_agent_performance(system):
    agent_perf = system.get_agent_performance()
    print("=== PERFORMANCE DOS AGENTES ===")
    for agent_name, stats in agent_perf.items():
        print(f"{agent_name}:")
        print(f"  Análises: {stats['total_analyses']}")
        print(f"  Confiança média: {stats['average_confidence']:.1f}%")
        print(f"  Recomendações: {stats['recommendations']}")
        print()

def print_discussion_messages(session_results):
    print("=== DISCUSSÃO ENTRE AGENTES ===")
    for symbol, result in session_results['results'].items():
        print(f"\nSímbolo: {symbol}")
        messages = result.get('discussion_messages', [])
        if not messages:
            print("  Nenhuma mensagem de discussão.")
            continue
        for i, msg in enumerate(messages, 1):
            print(f"  [Discussão {i}] {msg}")

def print_agent_analyses(session_results):
    print("=== ANÁLISES INDIVIDUAIS DOS AGENTES ===")
    for symbol, result in session_results['results'].items():
        print(f"\nSímbolo: {symbol}")
        analyses = result.get('analyses', [])
        if not analyses:
            print("  Nenhuma análise individual.")
        for analysis in analyses:
            agent = analysis.get('agent', 'Agente')
            resumo = analysis.get('analysis', '').strip().replace('\n', ' ')
            print(f"  [Análise] {agent}: {resumo}")
        research = result.get('research', [])
        for pesquisa in research:
            agent = pesquisa.get('agent', 'Pesquisador')
            resumo = pesquisa.get('research', '').strip().replace('\n', ' ')
            print(f"  [Pesquisa Crítica] {agent}: {resumo}")

async def main():
    system = TradingAgentsSystem(model_name="llama3.2")
    symbols = ['EURUSD=X', 'GPBUSD=X', 'ADA-USD', 'SOL-USD', 'MATIC-USD']
    print("=== SISTEMA DE TRADING MULTIAGENTE ===")
    print(f"Modelo LLM: {system.llm.model_name}")
    print(f"Agentes inicializados: {len(system.all_agents)}")
    print(f"Ollama GPU enabled: {getattr(system.llm, 'gpu_enabled', 'Indisponível')}")
    print()
    try:
        session_results = await system.run_trading_session(symbols[:2])
        print_session_results(session_results)
        print_portfolio_performance(system)
        print_agent_performance(system)
        print_agent_analyses(session_results)
        print_discussion_messages(session_results)
        if hasattr(system.llm, 'response_times') and system.llm.response_times:
            avg_time = sum(system.llm.response_times) / len(system.llm.response_times)
            print(f"Tempo médio de resposta do LLM: {avg_time:.2f} segundos")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("Iniciando TradingAgents System...")
    print("Certifique-se de que o Ollama está executando com o modelo llama3.2")
    print()
    asyncio.run(main())
