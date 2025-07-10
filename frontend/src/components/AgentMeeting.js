import React, { useEffect, useRef } from 'react';
import { Bot, Clock, MessageCircle, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';

const AgentAvatar = ({ agentName, isActive, agentType }) => {
  const getAgentColor = (name) => {
    const colors = {
      'Analista Fundamentalista': 'bg-blue-500',
      'Analista de Sentimentos': 'bg-green-500',
      'Analista de Notícias': 'bg-yellow-500',
      'Analista Técnico': 'bg-purple-500',
      'Pesquisador Otimista': 'bg-emerald-500',
      'Pesquisador Pessimista': 'bg-red-500',
      'Agente de Negociação': 'bg-orange-500',
      'Gestor de Risco': 'bg-pink-500',
      'Gestor de Portfólio': 'bg-indigo-500',
    };
    return colors[name] || 'bg-gray-500';
  };

  const getAgentIcon = (name) => {
    if (name.includes('Analista')) return TrendingUp;
    if (name.includes('Pesquisador')) return MessageCircle;
    if (name.includes('Gestor')) return AlertTriangle;
    return Bot;
  };

  const Icon = getAgentIcon(agentName);

  return (
    <div className={`relative ${isActive ? 'ring-2 ring-discord-green' : ''}`}>
      <div className={`w-10 h-10 rounded-full ${getAgentColor(agentName)} flex items-center justify-center ${isActive ? 'animate-pulse' : ''}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      {isActive && (
        <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-discord-green rounded-full flex items-center justify-center">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
        </div>
      )}
    </div>
  );
};

const AgentMessage = ({ message, isLatest }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getAgentColor = (name) => {
    const colors = {
      'Analista Fundamentalista': 'text-blue-400',
      'Analista de Sentimentos': 'text-green-400',
      'Analista de Notícias': 'text-yellow-400',
      'Analista Técnico': 'text-purple-400',
      'Pesquisador Otimista': 'text-emerald-400',
      'Pesquisador Pessimista': 'text-red-400',
      'Agente de Negociação': 'text-orange-400',
      'Gestor de Risco': 'text-pink-400',
      'Gestor de Portfólio': 'text-indigo-400',
    };
    return colors[name] || 'text-gray-400';
  };

  return (
    <div className={`flex space-x-3 p-3 rounded-lg transition-colors ${
      isLatest ? 'bg-discord-blue bg-opacity-10 animate-slide-in-right' : 'hover:bg-discord-light hover:bg-opacity-50'
    }`}>
      <AgentAvatar 
        agentName={message.agentName} 
        isActive={isLatest}
        agentType={message.agentType}
      />
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center space-x-2 mb-1">
          <span className={`font-semibold ${getAgentColor(message.agentName)}`}>
            {message.agentName}
          </span>
          <span className="text-xs text-discord-text-muted">
            {formatTime(message.timestamp)}
          </span>
          {message.symbol && (
            <span className="text-xs bg-discord-blue px-2 py-1 rounded text-white">
              {message.symbol}
            </span>
          )}
        </div>
        
        <div className="text-discord-text text-sm leading-relaxed">
          {message.message}
        </div>
      </div>
    </div>
  );
};

const TypingIndicator = ({ agentName }) => {
  return (
    <div className="flex space-x-3 p-3 rounded-lg bg-discord-light bg-opacity-30">
      <AgentAvatar agentName={agentName} isActive={true} />
      <div className="flex-1 min-w-0">
        <div className="flex items-center space-x-2 mb-1">
          <span className="font-semibold text-discord-text-muted">
            {agentName}
          </span>
          <span className="text-xs text-discord-text-muted">analisando...</span>
        </div>
        <div className="flex space-x-1">
          <div className="typing-indicator"></div>
          <div className="typing-indicator"></div>
          <div className="typing-indicator"></div>
        </div>
      </div>
    </div>
  );
};

const AgentMeeting = ({ agents, messages, isAnalysisRunning, currentSession }) => {
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getActiveAgents = () => {
    if (!isAnalysisRunning) return [];
    
    const recentMessages = messages.slice(-5);
    const activeAgentNames = new Set(recentMessages.map(msg => msg.agentName));
    
    return agents.filter(agent => activeAgentNames.has(agent.name));
  };

  const activeAgents = getActiveAgents();

  return (
    <div className="flex h-full">
      {/* Sidebar - Agentes */}
      <div className="w-64 bg-discord-dark border-r border-discord-light p-4">
        <h2 className="text-lg font-semibold mb-4 text-discord-text">Participantes</h2>
        
        <div className="space-y-3">
          {agents.map((agent, index) => {
            const isActive = activeAgents.some(a => a.name === agent.name);
            return (
              <div key={agent.name} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-discord-light hover:bg-opacity-50">
                <AgentAvatar 
                  agentName={agent.name} 
                  isActive={isActive}
                  agentType={agent.type}
                />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-discord-text truncate">
                    {agent.name}
                  </div>
                  <div className="text-xs text-discord-text-muted">
                    {agent.type}
                  </div>
                </div>
                
                {isActive && (
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-discord-green rounded-full animate-pulse" />
                    <span className="text-xs text-discord-green">Ativo</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Status da Sessão */}
        <div className="mt-6 p-3 bg-discord-darker rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <Clock className="w-4 h-4 text-discord-text-muted" />
            <span className="text-sm text-discord-text-muted">Status da Sessão</span>
          </div>
          
          <div className="text-sm">
            {isAnalysisRunning ? (
              <div className="flex items-center space-x-2 text-discord-green">
                <div className="w-2 h-2 bg-discord-green rounded-full animate-pulse" />
                <span>Análise em andamento</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2 text-discord-text-muted">
                <CheckCircle className="w-4 h-4" />
                <span>Aguardando análise</span>
              </div>
            )}
          </div>
          
          {currentSession && (
            <div className="mt-2 text-xs text-discord-text-muted">
              Sessão: {currentSession.split('_').pop()}
            </div>
          )}
        </div>
      </div>

      {/* Área de Mensagens */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-discord-text-muted">
              <div className="text-center">
                <MessageCircle className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg mb-2">Nenhuma discussão em andamento</p>
                <p className="text-sm">Inicie uma análise para ver os agentes discutindo</p>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {messages.map((message, index) => (
                <AgentMessage 
                  key={message.id || index}
                  message={message}
                  isLatest={index === messages.length - 1}
                />
              ))}
              
              {isAnalysisRunning && (
                <TypingIndicator agentName="Sistema" />
              )}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Barra de Status da Conversa */}
        <div className="border-t border-discord-light bg-discord-dark p-3">
          <div className="flex items-center justify-between text-sm text-discord-text-muted">
            <div className="flex items-center space-x-4">
              <span>{messages.length} mensagens</span>
              <span>{agents.length} agentes</span>
            </div>
            
            {isAnalysisRunning && (
              <div className="flex items-center space-x-2 text-discord-green">
                <div className="w-2 h-2 bg-discord-green rounded-full animate-pulse" />
                <span>Análise em tempo real</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentMeeting;