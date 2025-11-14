#!/bin/bash

echo "🧪 Testando API do Portal Empreendedor"
echo "========================================"
echo ""

API_URL="http://localhost:5010"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para testar endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -n "Testando $description... "
    
    response=$(curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}✗ FALHOU${NC} (HTTP $http_code)"
        echo "  Resposta: $body"
        return 1
    fi
}

# Verifica se API está rodando
echo "1. Verificando se API está online..."
if ! curl -s "$API_URL" > /dev/null 2>&1; then
    echo -e "${RED}✗ API não está respondendo em $API_URL${NC}"
    echo ""
    echo "Inicie a API com:"
    echo "  cd backend && python api.py"
    exit 1
fi
echo -e "${GREEN}✓ API está online${NC}"
echo ""

# Testa endpoints
echo "2. Testando endpoints públicos:"
echo ""

test_endpoint "GET" "/" "Rota raiz"
test_endpoint "GET" "/api/config" "Configurações"
test_endpoint "GET" "/api/servicos" "Lista de serviços"
test_endpoint "GET" "/api/auth/check" "Verificação de autenticação"

echo ""
echo "3. Testando endpoint de criação (POST):"
echo ""

# Cria um serviço de teste
echo -n "Criando serviço de teste... "
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/servicos" \
  -H "Content-Type: application/json" \
  -d '{
    "orgao_demandante": "Teste API",
    "titulo_servico": "Teste Automatizado",
    "tipo_atividade": "Teste",
    "especificacao_atividade": "Teste",
    "descricao_servico": "Serviço criado por teste automatizado",
    "outras_informacoes": "",
    "endereco": "Rua Teste",
    "numero": "123",
    "bairro": "Centro",
    "forma_pagamento": "Dinheiro",
    "prazo_pagamento": "30 dias",
    "prazo_expiracao": "2024-12-31",
    "data_limite_execucao": "2024-12-31"
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 201 ]; then
    echo -e "${GREEN}✓ OK${NC} (HTTP $http_code)"
    filename=$(echo "$body" | grep -o '"filename":"[^"]*"' | cut -d'"' -f4)
    echo "  Arquivo criado: $filename"
    
    # Testa download
    if [ ! -z "$filename" ]; then
        echo ""
        echo "4. Testando download do CSV:"
        test_endpoint "GET" "/api/download/$filename" "Download CSV"
    fi
else
    echo -e "${RED}✗ FALHOU${NC} (HTTP $http_code)"
    echo "  Resposta: $body"
fi

echo ""
echo "========================================"
echo "Testes concluídos!"
echo ""
echo "Para testar manualmente:"
echo "  curl $API_URL"
echo "  curl $API_URL/api/config"
echo "  curl $API_URL/api/servicos"
