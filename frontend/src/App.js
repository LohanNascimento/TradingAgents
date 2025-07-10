import React, { useState, useEffect } from 'react';
import { Users, Activity, TrendingUp, Bot, MessageSquare, BarChart3, AlertCircle } from 'lucide-react';
import AgentMeeting from './components/AgentMeeting';
import ControlPanel from './components/ControlPanel';
import StatusBar from './components/StatusBar';
import ResultsPanel from './components/ResultsPanel';
import { useWebSocket } from './hooks/useWebSocket';
import { useAgents } from './hooks/useAgents';

function App() {
  const [activeTab, setActiveTab] = useState('meeting');
  const [analysisResults, setAnalysisResults] = useState({});
  const [currentSession, setCurrentSession] = useState(null);
  const [agentMessages, setAgentMessages] = useState([]);
  const [isAnalysisRunning, setIsAnalysisRunning] = useState(false);

  const { agents, loading: agentsLoading } = useAgents();
  const { connectionStatus, messages } = useWebSocket();

  // Processar mensagens do WebSocket
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      
      switch (lastMessage.type) {
        case 'analysis_started':
          setIsAnalysisRunning(true);
          setCurrentSession(lastMessage.session_id);
          setAgentMessages([]);
          setAnalysisResults({});
          break;
          
        case 'agent_message':
          setAgentMessages(prev => [...prev, {
            id: `${lastMessage.session_id}-${lastMessage.message_index}`,
            agentName: lastMessage.agent_name,
            message: lastMessage.message,
            timestamp: lastMessage.timestamp,
            symbol: lastMessage.symbol
          }]);
          break;
          
        case 'symbol_analysis_completed':
          setAnalysisResults(prev => ({
            ...prev,
            [lastMessage.symbol]: lastMessage.result
          }));
          break;
          
        case 'analysis_completed':
          setIsAnalysisRunning(false);
          break;
          
        case 'analysis_error':
          setIsAnalysisRunning(false);
          console.error('Analysis error:', lastMessage.error);
          break;
      }
    }
  }, [messages]);

  const handleStartAnalysis = async (symbols) => {
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(symbols),
      });

      if (!response.ok) {
        throw new Error('Failed to start analysis');
      }

      const result = await response.json();
      console.log('Analysis started:', result);
    } catch (error) {
      console.error('Error starting analysis:', error);
    }
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'text-discord-green';
      case 'connecting': return 'text-discord-yellow';
      case 'disconnected': return 'text-discord-red';
      default: return 'text-discord-text-muted';
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return 'Conectado';
      case 'connecting': return 'Conectando...';
      case 'disconnected': return 'Desconectado';
      default: return 'Inicializando...';
    }
  };

  return (
    <div className="flex flex-col h-screen bg-discord-darker text-discord-text">
      {/* Header */}
      <header className="flex items-center justify-between p-4 bg-discord-dark border-b border-discord-light">
        <div className="flex items-center space-x-3">
          <Bot className="w-8 h-8 text-discord-blue" />
          <h1 className="text-xl font-bold">TradingAgents - Reunião Virtual</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${getConnectionStatusColor()}`} />
            <span className={`text-sm ${getConnectionStatusColor()}`}>
              {getConnectionStatusText()}
            </span>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-discord-text-muted">
            <Users className="w-4 h-4" />
            <span>{agents.length} agentes</span>
          </div>
          
          {isAnalysisRunning && (
            <div className="flex items-center space-x-2 text-sm text-discord-green">
              <Activity className="w-4 h-4 animate-pulse" />
              <span>Análise em andamento</span>
            </div>
          )}
        </div>
      </header>

      {/* Navigation */}
      <nav className="flex border-b border-discord-light bg-discord-dark">
        <button
          onClick={() => setActiveTab('meeting')}
          className={`flex items-center space-x-2 px-4 py-2 border-b-2 transition-colors ${
            activeTab === 'meeting' 
              ? 'border-discord-blue text-discord-blue' 
              : 'border-transparent text-discord-text-muted hover:text-discord-text'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Reunião</span>
        </button>
        
        <button
          onClick={() => setActiveTab('results')}
          className={`flex items-center space-x-2 px-4 py-2 border-b-2 transition-colors ${
            activeTab === 'results' 
              ? 'border-discord-blue text-discord-blue' 
              : 'border-transparent text-discord-text-muted hover:text-discord-text'
          }`}
        >
          <BarChart3 className="w-4 h-4" />
          <span>Resultados</span>
        </button>
        
        <button
          onClick={() => setActiveTab('control')}
          className={`flex items-center space-x-2 px-4 py-2 border-b-2 transition-colors ${
            activeTab === 'control' 
              ? 'border-discord-blue text-discord-blue' 
              : 'border-transparent text-discord-text-muted hover:text-discord-text'
          }`}
        >
          <TrendingUp className="w-4 h-4" />
          <span>Controle</span>
        </button>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'meeting' && (
          <AgentMeeting 
            agents={agents}
            messages={agentMessages}
            isAnalysisRunning={isAnalysisRunning}
            currentSession={currentSession}
          />
        )}
        
        {activeTab === 'results' && (
          <ResultsPanel 
            results={analysisResults}
            isAnalysisRunning={isAnalysisRunning}
          />
        )}
        
        {activeTab === 'control' && (
          <ControlPanel 
            onStartAnalysis={handleStartAnalysis}
            isAnalysisRunning={isAnalysisRunning}
            agents={agents}
          />
        )}
      </main>

      {/* Status Bar */}
      <StatusBar 
        connectionStatus={connectionStatus}
        messagesCount={agentMessages.length}
        analysisRunning={isAnalysisRunning}
      />
    </div>
  );
}

export default App;