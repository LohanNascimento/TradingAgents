import { useState, useEffect, useRef } from 'react';

export const useWebSocket = () => {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);
  const reconnectTimer = useRef(null);

  const connect = () => {
    try {
      setConnectionStatus('connecting');
      ws.current = new WebSocket('ws://localhost:8001/ws');

      ws.current.onopen = () => {
        setConnectionStatus('connected');
        console.log('WebSocket connected');
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setMessages(prev => [...prev, data]);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.current.onclose = () => {
        setConnectionStatus('disconnected');
        console.log('WebSocket disconnected');
        
        // Tentar reconectar após 3 segundos
        reconnectTimer.current = setTimeout(() => {
          connect();
        }, 3000);
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('disconnected');
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      setConnectionStatus('disconnected');
    }
  };

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
      }
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return {
    connectionStatus,
    messages,
    sendMessage: (message) => {
      if (ws.current && connectionStatus === 'connected') {
        ws.current.send(JSON.stringify(message));
      }
    }
  };
};