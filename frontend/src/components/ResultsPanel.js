import React from 'react';
import { TrendingUp, TrendingDown, Minus, CheckCircle, XCircle, AlertTriangle, DollarSign, BarChart3, Clock } from 'lucide-react';

const ResultsPanel = ({ results, isAnalysisRunning }) => {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatPercentage = (value) => {
    return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'buy': return <TrendingUp className="w-4 h-4 text-discord-green" />;
      case 'sell': return <TrendingDown className="w-4 h-4 text-discord-red" />;
      case 'hold': return <Minus className="w-4 h-4 text-discord-yellow" />;
      default: return <BarChart3 className="w-4 h-4 text-discord-text-muted" />;
    }
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'buy': return 'text-discord-green';
      case 'sell': return 'text-discord-red';
      case 'hold': return 'text-discord-yellow';
      default: return 'text-discord-text-muted';
    }
  };

  const getActionText = (action) => {
    switch (action) {
      case 'buy': return 'Comprar';
      case 'sell': return 'Vender';
      case 'hold': return 'Manter';
      default: return 'N/A';
    }
  };

  const getRiskColor = (riskScore) => {
    if (riskScore >= 70) return 'text-discord-red';
    if (riskScore >= 40) return 'text-discord-yellow';
    return 'text-discord-green';
  };

  const getRiskLevel = (riskScore) => {
    if (riskScore >= 70) return 'Alto';
    if (riskScore >= 40) return 'Médio';
    return 'Baixo';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-discord-green';
    if (confidence >= 60) return 'text-discord-yellow';
    return 'text-discord-red';
  };

  return (
    <div className="p-6 h-full overflow-y-auto scrollbar-thin">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-discord-text mb-2">Resultados da Análise</h2>
          <p className="text-discord-text-muted">Decisões de trading e avaliações de risco</p>
        </div>

        {/* Status Geral */}
        <div className="bg-discord-dark p-6 rounded-lg border border-discord-light">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-discord-text">{Object.keys(results).length}</div>
              <div className="text-sm text-discord-text-muted">Símbolos Analisados</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-discord-green">
                {Object.values(results).filter(r => r.approval).length}
              </div>
              <div className="text-sm text-discord-text-muted">Trades Aprovados</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-discord-blue">
                {Object.values(results).filter(r => r.executed_trade).length}
              </div>
              <div className="text-sm text-discord-text-muted">Trades Executados</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-discord-text">
                {Object.keys(results).length > 0 
                  ? ((Object.values(results).filter(r => r.approval).length / Object.keys(results).length) * 100).toFixed(0)
                  : 0}%
              </div>
              <div className="text-sm text-discord-text-muted">Taxa de Aprovação</div>
            </div>
          </div>
        </div>

        {/* Resultados por Símbolo */}
        {Object.keys(results).length === 0 ? (
          <div className="bg-discord-dark p-12 rounded-lg border border-discord-light text-center">
            <BarChart3 className="w-16 h-16 mx-auto mb-4 text-discord-text-muted opacity-50" />
            <h3 className="text-lg font-semibold text-discord-text mb-2">
              {isAnalysisRunning ? 'Análise em Andamento' : 'Nenhum Resultado Disponível'}
            </h3>
            <p className="text-discord-text-muted">
              {isAnalysisRunning 
                ? 'Aguarde enquanto os agentes analisam os símbolos...' 
                : 'Inicie uma análise para ver os resultados aqui'
              }
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(results).map(([symbol, result]) => (
              <div key={symbol} className="bg-discord-dark p-6 rounded-lg border border-discord-light">
                {/* Header do Símbolo */}
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-discord-text">{symbol}</h3>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-sm text-discord-text-muted">
                        {formatCurrency(result.market_data?.price || 0)}
                      </span>
                      <span className={`text-sm ${
                        (result.market_data?.change_percent || 0) >= 0 
                          ? 'text-discord-green' 
                          : 'text-discord-red'
                      }`}>
                        {formatPercentage(result.market_data?.change_percent || 0)}
                      </span>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    {result.approval ? (
                      <CheckCircle className="w-8 h-8 text-discord-green" />
                    ) : (
                      <XCircle className="w-8 h-8 text-discord-red" />
                    )}
                  </div>
                </div>

                {/* Decisão de Trading */}
                <div className="bg-discord-darker p-4 rounded-lg mb-4">
                  <h4 className="text-sm font-semibold text-discord-text mb-2 flex items-center">
                    <DollarSign className="w-4 h-4 mr-2" />
                    Decisão de Trading
                  </h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="flex items-center space-x-2 mb-1">
                        {getActionIcon(result.trading_decision?.action)}
                        <span className={`font-semibold ${getActionColor(result.trading_decision?.action)}`}>
                          {getActionText(result.trading_decision?.action)}
                        </span>
                      </div>
                      <div className="text-sm text-discord-text-muted">
                        Quantidade: {result.trading_decision?.quantity || 0}
                      </div>
                      <div className="text-sm text-discord-text-muted">
                        Preço: {formatCurrency(result.trading_decision?.price || 0)}
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-right">
                        <div className={`text-lg font-bold ${getConfidenceColor(result.trading_decision?.confidence || 0)}`}>
                          {(result.trading_decision?.confidence || 0).toFixed(0)}%
                        </div>
                        <div className="text-sm text-discord-text-muted">Confiança</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Avaliação de Risco */}
                <div className="bg-discord-darker p-4 rounded-lg mb-4">
                  <h4 className="text-sm font-semibold text-discord-text mb-2 flex items-center">
                    <AlertTriangle className="w-4 h-4 mr-2" />
                    Avaliação de Risco
                  </h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className={`text-lg font-bold ${getRiskColor(result.risk_assessment?.risk_score || 0)}`}>
                        {getRiskLevel(result.risk_assessment?.risk_score || 0)}
                      </div>
                      <div className="text-sm text-discord-text-muted">
                        Score: {(result.risk_assessment?.risk_score || 0).toFixed(0)}
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-discord-text">
                        Volatilidade: {((result.risk_assessment?.volatility || 0) * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-discord-text">
                        Liquidez: {(result.risk_assessment?.liquidity_score || 0).toFixed(0)}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Status da Execução */}
                <div className="flex items-center justify-between">
                  <div>
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      result.approval 
                        ? 'bg-discord-green bg-opacity-20 text-discord-green' 
                        : 'bg-discord-red bg-opacity-20 text-discord-red'
                    }`}>
                      {result.approval ? 'Aprovado' : 'Rejeitado'}
                    </span>
                    
                    {result.executed_trade && (
                      <span className="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-discord-blue bg-opacity-20 text-discord-blue">
                        Executado
                      </span>
                    )}
                  </div>
                  
                  <div className="flex items-center text-xs text-discord-text-muted">
                    <Clock className="w-3 h-3 mr-1" />
                    {result.analyses_count || 0} análises
                  </div>
                </div>

                {/* Justificativa */}
                {result.approval_reasoning && (
                  <div className="mt-4 p-3 bg-discord-light bg-opacity-30 rounded-lg">
                    <div className="text-xs text-discord-text-muted mb-1">Justificativa:</div>
                    <div className="text-sm text-discord-text">{result.approval_reasoning}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;