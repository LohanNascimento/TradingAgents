import React, { useState } from 'react';
import { Play, StopCircle, Plus, X, TrendingUp, AlertCircle } from 'lucide-react';

const ControlPanel = ({ onStartAnalysis, isAnalysisRunning, agents }) => {
  const [symbols, setSymbols] = useState(['BTC-USD', 'ETH-USD']);
  const [newSymbol, setNewSymbol] = useState('');

  const addSymbol = () => {
    if (newSymbol.trim() && !symbols.includes(newSymbol.trim().toUpperCase())) {
      setSymbols([...symbols, newSymbol.trim().toUpperCase()]);
      setNewSymbol('');
    }
  };

  const removeSymbol = (symbolToRemove) => {
    setSymbols(symbols.filter(symbol => symbol !== symbolToRemove));
  };

  const handleStartAnalysis = () => {
    if (symbols.length > 0) {
      onStartAnalysis(symbols);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addSymbol();
    }
  };

  const popularSymbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD'];

  return (
    <div className="p-6 h-full overflow-y-auto scrollbar-thin">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-discord-text mb-2">Painel de Controle</h2>
          <p className="text-discord-text-muted">Configure e inicie análises de trading multiagente</p>
        </div>

        {/* Status dos Agentes */}
        <div className="bg-discord-dark p-6 rounded-lg border border-discord-light">
          <h3 className="text-lg font-semibold text-discord-text mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2" />
            Status dos Agentes
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <div key={agent.name} className="bg-discord-darker p-4 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-discord-text text-sm">{agent.name}</h4>
                  <div className="w-2 h-2 bg-discord-green rounded-full"></div>
                </div>
                <p className="text-xs text-discord-text-muted">{agent.type}</p>
                <div className="mt-2 text-xs text-discord-text-muted">
                  {agent.total_analyses} análises realizadas
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Configuração de Símbolos */}
        <div className="bg-discord-dark p-6 rounded-lg border border-discord-light">
          <h3 className="text-lg font-semibold text-discord-text mb-4">Símbolos para Análise</h3>
          
          {/* Símbolos Atuais */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-discord-text mb-2">
              Símbolos Selecionados ({symbols.length})
            </label>
            <div className="flex flex-wrap gap-2">
              {symbols.map((symbol) => (
                <span
                  key={symbol}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-discord-blue text-white"
                >
                  {symbol}
                  <button
                    onClick={() => removeSymbol(symbol)}
                    className="ml-2 hover:text-discord-red transition-colors"
                    disabled={isAnalysisRunning}
                  >
                    <X className="w-4 h-4" />
                  </button>
                </span>
              ))}
              
              {symbols.length === 0 && (
                <span className="text-discord-text-muted text-sm">
                  Nenhum símbolo selecionado
                </span>
              )}
            </div>
          </div>

          {/* Adicionar Novo Símbolo */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-discord-text mb-2">
              Adicionar Símbolo
            </label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={newSymbol}
                onChange={(e) => setNewSymbol(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ex: AAPL, BTC-USD"
                className="flex-1 px-3 py-2 bg-discord-darker border border-discord-light rounded-md text-discord-text placeholder-discord-text-muted focus:outline-none focus:ring-2 focus:ring-discord-blue"
                disabled={isAnalysisRunning}
              />
              <button
                onClick={addSymbol}
                disabled={!newSymbol.trim() || isAnalysisRunning}
                className="px-4 py-2 bg-discord-blue text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Símbolos Populares */}
          <div>
            <label className="block text-sm font-medium text-discord-text mb-2">
              Símbolos Populares
            </label>
            <div className="flex flex-wrap gap-2">
              {popularSymbols.map((symbol) => (
                <button
                  key={symbol}
                  onClick={() => {
                    if (!symbols.includes(symbol)) {
                      setSymbols([...symbols, symbol]);
                    }
                  }}
                  disabled={symbols.includes(symbol) || isAnalysisRunning}
                  className="px-3 py-1 text-sm bg-discord-darker border border-discord-light rounded-md text-discord-text hover:bg-discord-light disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {symbol}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Controles de Análise */}
        <div className="bg-discord-dark p-6 rounded-lg border border-discord-light">
          <h3 className="text-lg font-semibold text-discord-text mb-4">Controles de Análise</h3>
          
          <div className="flex items-center justify-between">
            <div className="flex-1 mr-4">
              {isAnalysisRunning ? (
                <div className="flex items-center space-x-2 text-discord-green">
                  <div className="w-3 h-3 bg-discord-green rounded-full animate-pulse"></div>
                  <span className="font-medium">Análise em Andamento</span>
                </div>
              ) : (
                <div className="text-discord-text-muted">
                  Pronto para iniciar análise
                </div>
              )}
            </div>
            
            <button
              onClick={handleStartAnalysis}
              disabled={symbols.length === 0 || isAnalysisRunning}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                isAnalysisRunning
                  ? 'bg-discord-red text-white cursor-not-allowed opacity-50'
                  : 'bg-discord-green text-white hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed'
              }`}
            >
              {isAnalysisRunning ? (
                <>
                  <StopCircle className="w-5 h-5" />
                  <span>Analisando...</span>
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" />
                  <span>Iniciar Análise</span>
                </>
              )}
            </button>
          </div>

          {symbols.length === 0 && (
            <div className="mt-4 p-3 bg-discord-yellow bg-opacity-10 border border-discord-yellow rounded-lg flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-discord-yellow" />
              <span className="text-discord-yellow text-sm">
                Adicione pelo menos um símbolo para iniciar a análise
              </span>
            </div>
          )}
        </div>

        {/* Informações */}
        <div className="bg-discord-dark p-6 rounded-lg border border-discord-light">
          <h3 className="text-lg font-semibold text-discord-text mb-4">Como Funciona</h3>
          
          <div className="space-y-3 text-sm text-discord-text-muted">
            <p>
              • <strong>Análise Multiagente:</strong> Cada símbolo é analisado por múltiplos agentes especializados
            </p>
            <p>
              • <strong>Discussão Colaborativa:</strong> Os agentes discutem suas análises em tempo real
            </p>
            <p>
              • <strong>Decisão Final:</strong> O sistema toma decisões baseadas no consenso dos agentes
            </p>
            <p>
              • <strong>Gestão de Risco:</strong> Todas as decisões passam por avaliação de risco
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;