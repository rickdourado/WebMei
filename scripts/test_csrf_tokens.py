#!/usr/bin/env python3
"""
Script para testar se os tokens CSRF estão funcionando corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from app import app

def test_csrf_implementation():
    print("Testando implementação de tokens CSRF")
    print("=" * 60)
    
    # Inicia o app em modo de teste
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    
    with app.test_client() as client:
        print("🔍 Testando páginas com formulários...")
        
        # Testa página de login
        print("\n1. Página de login (/admin/login)")
        response = client.get('/admin/login')
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            if 'csrf_token' in content or 'name="csrf_token"' in content:
                print("   ✅ Token CSRF encontrado no HTML")
            else:
                print("   ❌ Token CSRF NÃO encontrado no HTML")
        else:
            print(f"   ❌ Erro ao acessar página: {response.status_code}")
        
        # Testa página principal
        print("\n2. Página principal (/)")
        response = client.get('/')
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            if 'csrf_token' in content or 'name="csrf_token"' in content:
                print("   ✅ Token CSRF encontrado no HTML")
            else:
                print("   ❌ Token CSRF NÃO encontrado no HTML")
        else:
            print(f"   ❌ Erro ao acessar página: {response.status_code}")
        
        # Testa login sem token CSRF
        print("\n3. Teste de login sem token CSRF")
        response = client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        if response.status_code == 400:
            print("   ✅ Requisição rejeitada (400 Bad Request) - CSRF funcionando")
        else:
            print(f"   ⚠️  Resposta inesperada: {response.status_code}")
        
        print("\n" + "=" * 60)
        print("✅ Teste de CSRF concluído!")
        print("\nℹ️  Para testar login completo, use o navegador web")
        print("   O Flask-WTF gera tokens únicos por sessão")

if __name__ == "__main__":
    test_csrf_implementation()