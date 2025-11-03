#!/usr/bin/env python3
"""
Script para testar o sistema de autenticação via banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
import getpass

def test_authentication():
    print("Testando Sistema de Autenticação via Banco de dados")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Lista usuários disponíveis
    print("👥 Usuários cadastrados na tabela authuser:")
    users = db.list_users()
    for user in users:
        print(f"   - ID: {user['id']}, Login: {user['login']}")
    
    if not users:
        print("   ❌ Nenhum usuário encontrado!")
        return
    
    print("\n" + "-" * 60)
    
    # Teste de autenticação interativo
    print("🔐 Teste de Autenticação")
    login = input("Digite o login: ").strip()
    
    if not login:
        print("❌ Login não pode estar vazio!")
        return
    
    password = getpass.getpass("Digite a senha: ")
    
    print(f"\n🔍 Testando autenticação para: {login}")
    
    # Testa autenticação
    result = db.authenticate_user(login, password)
    
    if result:
        print("✅ Autenticação bem-sucedida!")
        print(f"   - ID: {result['id']}")
        print(f"   - Login: {result['login']}")
    else:
        print("❌ Falha na autenticação!")
        print("   Verifique se o login e senha estão corretos.")
    
    print("\n" + "-" * 60)
    
    # Opção para atualizar senha com hash
    if result:
        update = input(f"\nDeseja atualizar a senha de '{login}' para usar hash bcrypt? (s/n): ").lower().strip()
        if update == 's':
            new_password = getpass.getpass("Digite a nova senha: ")
            confirm = getpass.getpass("Confirme a nova senha: ")
            
            if new_password != confirm:
                print("❌ Senhas não coincidem!")
                return
            
            if db.update_user_password_hash(login, new_password):
                print("✅ Senha atualizada com hash bcrypt!")
                
                # Testa a nova senha
                test_result = db.authenticate_user(login, new_password)
                if test_result:
                    print("✅ Verificação da nova senha: OK")
                else:
                    print("❌ Erro na verificação da nova senha!")
            else:
                print("❌ Erro ao atualizar senha!")

def test_connection():
    """Testa conexão básica com o banco"""
    print("🔌 Testando conexão com banco de dados...")
    
    try:
        db = DatabaseManager()
        connection = db.get_connection()
        connection.close()
        print("✅ Conexão com banco: OK")
        return True
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        test_authentication()
    else:
        print("❌ Não foi possível conectar ao banco de dados!")
        print("   Verifique as configurações no arquivo .env")