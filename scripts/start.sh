#!/bin/bash

# Script para iniciar o sistema TradingAgents Web

echo "🚀 Iniciando TradingAgents Web Application..."

# Verificar se o Ollama está rodando
echo "📡 Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama não encontrado. Por favor, instale o Ollama primeiro."
    exit 1
fi

# Verificar se o modelo llama3.2 está disponível
echo "🧠 Verificando modelo llama3.2..."
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 Baixando modelo llama3.2..."
    ollama pull llama3.2
fi

echo "✅ Configuração inicial concluída!"
echo "🌐 Acesse: http://localhost:3000"
echo "📡 API Backend: http://localhost:8001"