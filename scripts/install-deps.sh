#!/bin/bash

echo "📦 Instalando dependências..."

# Backend
echo "🐍 Instalando dependências do backend..."
cd /app && pip install -r requirements.txt
cd /app/backend && pip install -r requirements.txt

# Frontend
echo "⚛️ Instalando dependências do frontend..."
cd /app/frontend && yarn install

echo "✅ Todas as dependências instaladas!"