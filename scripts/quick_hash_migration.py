#!/usr/bin/env python3
"""
Script rápido para migrar senhas conhecidas para hash bcrypt
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
import bcrypt as bcrypt_lib

def quick_migration():
    """Migração rápida das senhas conhecidas"""
    print("🚀 Migração Rápida - Senhas para Hash bcrypt")
    print("=" * 60)
    
    # Senhas conhecidas (baseadas no check_passwords.py)
    known_passwords = {
        'admin': 'admin123',
        'oportunidades.cariocas@prefeitura.rio': 'GPCE#2025#'
    }
    
    db = DatabaseManager()
    
    try:
        connection = db.get_connection()
        
        # Verifica usuários atuais
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, login, senha FROM authuser")
            users = cursor.fetchall()
            
            print(f"👥 Encontrados {len(users)} usuários na tabela authuser")
            
            updated_count = 0
            
            for user_id, login, current_senha in users:
                print(f"\n👤 Processando: {login}")
                
                # Verifica se já é hash
                if current_senha.startswith('$2b$') or current_senha.startswith('$2a$'):
                    print("   ✅ Já está em hash bcrypt - pulando")
                    continue
                
                # Verifica se temos a senha conhecida
                if login in known_passwords:
                    expected_password = known_passwords[login]
                    
                    # Verifica se a senha atual confere
                    if current_senha == expected_password:
                        print(f"   🔄 Convertendo senha para hash...")
                        
                        # Gera hash
                        salt = bcrypt_lib.gensalt()
                        hashed = bcrypt_lib.hashpw(expected_password.encode('utf-8'), salt)
                        hash_string = hashed.decode('utf-8')
                        
                        # Atualiza no banco
                        cursor.execute(
                            "UPDATE authuser SET senha = %s WHERE id = %s",
                            (hash_string, user_id)
                        )
                        
                        print(f"   ✅ Hash gerado: {hash_string[:30]}...")
                        
                        # Testa o hash
                        if bcrypt_lib.checkpw(expected_password.encode('utf-8'), hashed):
                            print("   ✅ Verificação: OK")
                            updated_count += 1
                        else:
                            print("   ❌ Erro na verificação!")
                    else:
                        print(f"   ⚠️  Senha atual ({current_senha}) não confere com esperada")
                        print("   ℹ️  Use o script interativo para este usuário")
                else:
                    print("   ⚠️  Senha não conhecida - use script interativo")
            
            # Commit das mudanças
            connection.commit()
            
            print(f"\n📊 Resultado:")
            print(f"   ✅ Usuários migrados: {updated_count}")
            print(f"   📋 Total de usuários: {len(users)}")
            
            if updated_count > 0:
                print("\n🎉 Migração concluída com sucesso!")
            else:
                print("\n ℹ️  Nenhuma migração necessária.")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

def test_after_migration():
    """Testa login após migração"""
    print("\n🧪 Testando autenticação após migração...")
    
    db = DatabaseManager()
    
    test_cases = [
        ("admin", "admin123"),
        ("oportunidades.cariocas@prefeitura.rio", "GPCE#2025#")
    ]
    
    for login, password in test_cases:
        print(f"\n🔍 Testando: {login}")
        result = db.authenticate_user(login, password)
        
        if result:
            print(f"   ✅ Login OK - ID: {result['id']}")
        else:
            print("   ❌ Falha no login!")

if __name__ == "__main__":
    if quick_migration():
        test_after_migration()
        
        print(f"\n📋 Próximos passos:")
        print("1. ✅ Senhas migradas para hash bcrypt")
        print("2. 🧪 Teste o login no navegador")
        print("3. 🔧 Use migrate_passwords_to_hash.py para outros usuários")
        print("4. 🚀 Deploy para produção com segurança!")
    else:
        print("❌ Falha na migração - verifique os erros acima")