#!/bin/bash

# Script para iniciar o ambiente de desenvolvimento React + Flask

echo "🚀 Iniciando Portal Empreendedor (React + Flask)"
echo ""

# Verifica se está no ambiente conda correto
if [[ "$CONDA_DEFAULT_ENV" != "ciclo" ]]; then
    echo "⚠️  Ativando ambiente conda 'ciclo'..."
    eval "$(conda shell.bash hook)"
    conda activate ciclo
fi

# Função para cleanup ao sair
cleanup() {
    echo ""
    echo "🛑 Encerrando servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Inicia o backend
echo "📡 Iniciando API Flask (Backend)..."
cd backend
python api.py &
BACKEND_PID=$!
cd ..

# Aguarda o backend iniciar
sleep 3

# Inicia o frontend
echo "⚛️  Iniciando React (Frontend)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servidores iniciados!"
echo ""
echo "📍 Backend API: http://localhost:5010"
echo "📍 Frontend React: http://localhost:5173"
echo ""
echo "Pressione Ctrl+C para encerrar ambos os servidores"
echo ""

# Mantém o script rodando
wait
