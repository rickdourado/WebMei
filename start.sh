#!/bin/bash

# Script para iniciar backend e frontend simultaneamente
# Portal Empreendedor Unificado
# Versão simplificada no diretório raiz

echo "🚀 Iniciando Portal Empreendedor..."
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica se conda está disponível
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Conda não encontrado. Por favor, instale o Anaconda/Miniconda.${NC}"
    exit 1
fi

# Ativa ambiente conda
echo -e "${BLUE}📦 Ativando ambiente conda 'ciclo'...${NC}"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ciclo

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao ativar ambiente 'ciclo'. Certifique-se de que ele existe.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Ambiente conda ativado${NC}"
echo ""

# Função para cleanup ao sair
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Encerrando serviços...${NC}"
    kill 0
    exit 0
}

trap cleanup SIGINT SIGTERM

# Inicia backend
echo -e "${BLUE}🔧 Iniciando Backend (Flask - porta 5010)...${NC}"
cd backend
python api.py &
BACKEND_PID=$!
cd ..

# Aguarda um pouco para o backend iniciar
sleep 2

# Inicia frontend
echo -e "${BLUE}⚛️  Iniciando Frontend (React + Vite - porta 5173)...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ Serviços iniciados com sucesso!${NC}"
echo ""
echo -e "${BLUE}📍 URLs disponíveis:${NC}"
echo -e "   Backend API:  ${GREEN}http://localhost:5010${NC}"
echo -e "   Frontend:     ${GREEN}http://localhost:5173${NC}"
echo ""
echo -e "${BLUE}💡 Pressione Ctrl+C para encerrar ambos os serviços${NC}"
echo ""

# Aguarda os processos
wait
