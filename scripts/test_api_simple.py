#!/usr/bin/env python
"""
Script simples para testar a API do Portal Empreendedor
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:5010"

def test_endpoint(method, endpoint, description, data=None):
    """Testa um endpoint da API"""
    url = f"{API_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testando: {description}")
    print(f"Método: {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Método {method} não suportado")
            return False
        
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"✅ SUCESSO")
            try:
                json_data = response.json()
                print(f"Resposta (primeiras linhas):")
                print(json.dumps(json_data, indent=2, ensure_ascii=False)[:500])
            except:
                print(f"Resposta: {response.text[:200]}")
            return True
        else:
            print(f"❌ FALHOU")
            print(f"Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ ERRO: Não foi possível conectar à API em {API_URL}")
        print(f"\nCertifique-se de que a API está rodando:")
        print(f"  cd backend && python api.py")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def main():
    print("🧪 Teste da API - Portal Empreendedor")
    print("="*60)
    
    # Verifica se API está online
    print("\n1️⃣ Verificando se API está online...")
    try:
        response = requests.get(API_URL, timeout=2)
        print(f"✅ API está respondendo!")
        print(f"Status: {response.status_code}")
    except:
        print(f"❌ API não está respondendo em {API_URL}")
        print(f"\nInicie a API com:")
        print(f"  cd backend")
        print(f"  python api.py")
        return
    
    # Testa endpoints
    print("\n2️⃣ Testando endpoints públicos...")
    
    test_endpoint("GET", "/", "Rota raiz")
    test_endpoint("GET", "/api/config", "Configurações")
    test_endpoint("GET", "/api/servicos", "Lista de serviços")
    test_endpoint("GET", "/api/auth/check", "Verificação de autenticação")
    
    # Testa criação de serviço
    print("\n3️⃣ Testando criação de serviço...")
    
    data = {
        "orgao_demandante": "Teste API Python",
        "titulo_servico": f"Teste {datetime.now().strftime('%H:%M:%S')}",
        "tipo_atividade": "Teste",
        "especificacao_atividade": "Teste Automatizado",
        "descricao_servico": "Serviço criado por teste automatizado Python",
        "outras_informacoes": "",
        "endereco": "Rua Teste",
        "numero": "123",
        "bairro": "Centro",
        "forma_pagamento": "Dinheiro",
        "prazo_pagamento": "30 dias",
        "prazo_expiracao": "2024-12-31",
        "data_limite_execucao": "2024-12-31"
    }
    
    test_endpoint("POST", "/api/servicos", "Criar serviço", data)
    
    print("\n" + "="*60)
    print("✅ Testes concluídos!")
    print("\nPara testar manualmente no navegador:")
    print(f"  {API_URL}")
    print(f"  {API_URL}/api/config")
    print(f"  {API_URL}/api/servicos")

if __name__ == "__main__":
    main()
