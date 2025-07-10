import React from 'react';
import { Wifi, WifiOff, MessageSquare, Activity } from 'lucide-react';

const StatusBar = ({ connectionStatus, messagesCount, analysisRunning }) => {
  const getConnectionIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <Wifi className="w-4 h-4 text-discord-green" />;
      case 'connecting':
        return <Wifi className="w-4 h-4 text-discord-yellow animate-pulse" />;
      case 'disconnected':
        return <WifiOff className="w-4 h-4 text-discord-red" />;
      default:
        return <WifiOff className="w-4 h-4 text-discord-text-muted" />;
    }
  };

  const getConnectionText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Conectado';
      case 'connecting':
        return 'Conectando...';
      case 'disconnected':
        return 'Desconectado';
      default:
        return 'Inicializando...';
    }
  };

  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'text-discord-green';
      case 'connecting':
        return 'text-discord-yellow';
      case 'disconnected':
        return 'text-discord-red';
      default:
        return 'text-discord-text-muted';
    }
  };

  return (
    <div className="bg-discord-dark border-t border-discord-light px-4 py-2">
      <div className="flex items-center justify-between text-sm">
        {/* Status de Conexão */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            {getConnectionIcon()}
            <span className={getConnectionColor()}>
              {getConnectionText()}
            </span>
          </div>

          <div className="flex items-center space-x-2 text-discord-text-muted">
            <MessageSquare className="w-4 h-4" />
            <span>{messagesCount} mensagens</span>
          </div>

          {analysisRunning && (
            <div className="flex items-center space-x-2 text-discord-green">
              <Activity className="w-4 h-4 animate-pulse" />
              <span>Análise ativa</span>
            </div>
          )}
        </div>

        {/* Informações Adicionais */}
        <div className="flex items-center space-x-4 text-discord-text-muted">
          <span>TradingAgents v1.0</span>
          <span>•</span>
          <span>
            {new Date().toLocaleTimeString('pt-BR', { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </span>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;