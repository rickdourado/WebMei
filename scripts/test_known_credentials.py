#!/usr/bin/env python3
"""
Script para testar autenticação com credenciais conhecidas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager

def test_known_credentials():
    print("Testando autenticação com credenciais conhecidas")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Credenciais conhecidas da tabela
    test_cases = [
        ("admin", "admin123"),
        ("oportunidades.cariocas@prefeitura.rio", "GPCE#2025#"),
        ("admin", "senha_errada"),  # Teste de falha
    ]
    
    for login, password in test_cases:
        print(f"\n🔍 Testando: {login}")
        print(f"   Senha: {'*' * len(password)}")
        
        result = db.authenticate_user(login, password)
        
        if result:
            print("   ✅ Autenticação bem-sucedida!")
            print(f"   📋 Dados: ID={result['id']}, Login={result['login']}")
        else:
            print("   ❌ Falha na autenticação")
    
    print("\n" + "=" * 60)
    print("✅ Teste de autenticação via banco de dados concluído!")

if __name__ == "__main__":
    test_known_credentials()