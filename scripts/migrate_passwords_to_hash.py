#!/usr/bin/env python3
"""
Script para migrar senhas em texto plano para hash bcrypt na tabela authuser
"""

import sys
import os
import getpass
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
import bcrypt as bcrypt_lib

def show_current_passwords():
    """Mostra o estado atual das senhas (sem expor valores)"""
    print("📋 Estado atual das senhas na tabela authuser")
    print("=" * 60)
    
    db = DatabaseManager()
    
    try:
        connection = db.get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, login, senha FROM authuser ORDER BY id")
            users = cursor.fetchall()
            
            for user in users:
                user_id, login, senha = user
                
                print(f"\n👤 ID: {user_id} | Login: {login}")
                
                # Detecta formato da senha
                if senha.startswith('$2b$') or senha.startswith('$2a$'):
                    print("   🔐 Status: ✅ Hash bcrypt (seguro)")
                    print(f"   🔍 Hash: {senha[:30]}...")
                else:
                    print("   ⚠️  Status: ❌ Texto plano (inseguro)")
                    print(f"   🔍 Tamanho: {len(senha)} caracteres")
        
        connection.close()
        return users
        
    except Exception as e:
        print(f"❌ Erro ao consultar banco: {e}")
        return []

def migrate_user_password(user_id, login, current_password):
    """Migra senha de um usuário específico para hash"""
    print(f"\n🔄 Migrando senha do usuário: {login}")
    
    # Gera hash bcrypt
    salt = bcrypt_lib.gensalt()
    hashed = bcrypt_lib.hashpw(current_password.encode('utf-8'), salt)
    hash_string = hashed.decode('utf-8')
    
    print(f"   🔐 Hash gerado: {hash_string[:30]}...")
    
    # Testa o hash antes de salvar
    if bcrypt_lib.checkpw(current_password.encode('utf-8'), hashed):
        print("   ✅ Verificação do hash: OK")
    else:
        print("   ❌ Erro na verificação do hash!")
        return False
    
    # Atualiza no banco
    db = DatabaseManager()
    
    try:
        connection = db.get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE authuser SET senha = %s WHERE id = %s",
                (hash_string, user_id)
            )
            connection.commit()
            
            if cursor.rowcount > 0:
                print("   ✅ Senha atualizada no banco de dados!")
                return True
            else:
                print("   ❌ Nenhuma linha foi atualizada!")
                return False
                
    except Exception as e:
        print(f"   ❌ Erro ao atualizar banco: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

def migrate_all_passwords():
    """Migra todas as senhas em texto plano para hash"""
    print("\n🚀 Iniciando migração de senhas para hash bcrypt")
    print("=" * 60)
    
    users = show_current_passwords()
    
    if not users:
        print("❌ Nenhum usuário encontrado!")
        return
    
    # Identifica usuários com senha em texto plano
    plain_text_users = []
    for user_id, login, senha in users:
        if not (senha.startswith('$2b$') or senha.startswith('$2a$')):
            plain_text_users.append((user_id, login, senha))
    
    if not plain_text_users:
        print("\n✅ Todas as senhas já estão em hash bcrypt!")
        print("   Nenhuma migração necessária.")
        return
    
    print(f"\n⚠️  Encontrados {len(plain_text_users)} usuários com senha em texto plano:")
    for user_id, login, senha in plain_text_users:
        print(f"   - {login} (ID: {user_id})")
    
    # Confirmação de segurança
    print(f"\n🔒 ATENÇÃO: Esta operação irá:")
    print("   1. Converter senhas de texto plano para hash bcrypt")
    print("   2. Tornar as senhas irreversíveis")
    print("   3. Manter a funcionalidade de login")
    
    confirm = input("\nDeseja continuar? (digite 'CONFIRMO' para prosseguir): ").strip()
    
    if confirm != 'CONFIRMO':
        print("❌ Operação cancelada pelo usuário.")
        return
    
    # Migrar cada usuário
    success_count = 0
    for user_id, login, current_password in plain_text_users:
        if migrate_user_password(user_id, login, current_password):
            success_count += 1
        else:
            print(f"   ❌ Falha na migração de {login}")
    
    print(f"\n📊 Resultado da migração:")
    print(f"   ✅ Sucessos: {success_count}")
    print(f"   ❌ Falhas: {len(plain_text_users) - success_count}")
    
    if success_count == len(plain_text_users):
        print("\n🎉 Migração concluída com sucesso!")
        print("   Todas as senhas agora estão em hash bcrypt seguro.")
    else:
        print("\n⚠️  Migração parcialmente concluída.")
        print("   Verifique os erros acima e tente novamente se necessário.")

def test_authentication_after_migration():
    """Testa autenticação após migração"""
    print("\n🧪 Testando autenticação após migração")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Credenciais conhecidas para teste
    test_cases = [
        ("admin", "admin123"),
        ("oportunidades.cariocas@prefeitura.rio", "GPCE#2025#")
    ]
    
    for login, password in test_cases:
        print(f"\n🔍 Testando: {login}")
        result = db.authenticate_user(login, password)
        
        if result:
            print("   ✅ Autenticação bem-sucedida!")
        else:
            print("   ❌ Falha na autenticação!")
            print("   ⚠️  Verifique se a senha está correta")

def interactive_password_update():
    """Permite atualizar senha de usuário específico interativamente"""
    print("\n🔧 Atualização interativa de senha")
    print("=" * 60)
    
    users = show_current_passwords()
    
    if not users:
        print("❌ Nenhum usuário encontrado!")
        return
    
    print(f"\n👥 Usuários disponíveis:")
    for user_id, login, senha in users:
        status = "Hash" if (senha.startswith('$2b$') or senha.startswith('$2a$')) else "Texto plano"
        print(f"   {user_id}. {login} ({status})")
    
    try:
        user_choice = int(input("\nEscolha o ID do usuário: "))
        selected_user = next((u for u in users if u[0] == user_choice), None)
        
        if not selected_user:
            print("❌ Usuário não encontrado!")
            return
        
        user_id, login, current_senha = selected_user
        
        print(f"\n👤 Usuário selecionado: {login}")
        
        # Se já é hash, pede nova senha
        if current_senha.startswith('$2b$') or current_senha.startswith('$2a$'):
            print("   ℹ️  Senha atual já está em hash")
            new_password = getpass.getpass("Digite a nova senha: ")
            confirm_password = getpass.getpass("Confirme a nova senha: ")
            
            if new_password != confirm_password:
                print("❌ Senhas não coincidem!")
                return
            
            if migrate_user_password(user_id, login, new_password):
                print("✅ Senha atualizada com sucesso!")
            else:
                print("❌ Erro ao atualizar senha!")
        else:
            # Senha em texto plano - oferece opções
            print(f"   ⚠️  Senha atual em texto plano: {current_senha}")
            
            choice = input("Deseja (1) manter senha atual em hash ou (2) definir nova senha? [1/2]: ")
            
            if choice == "1":
                if migrate_user_password(user_id, login, current_senha):
                    print("✅ Senha migrada para hash com sucesso!")
                else:
                    print("❌ Erro na migração!")
            elif choice == "2":
                new_password = getpass.getpass("Digite a nova senha: ")
                confirm_password = getpass.getpass("Confirme a nova senha: ")
                
                if new_password != confirm_password:
                    print("❌ Senhas não coincidem!")
                    return
                
                if migrate_user_password(user_id, login, new_password):
                    print("✅ Nova senha definida com sucesso!")
                else:
                    print("❌ Erro ao definir nova senha!")
            else:
                print("❌ Opção inválida!")
                
    except ValueError:
        print("❌ ID inválido!")
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário.")

def main():
    """Menu principal"""
    print("🔐 Migração de Senhas para Hash bcrypt")
    print("=" * 60)
    
    while True:
        print(f"\n📋 Opções disponíveis:")
        print("1. 👀 Mostrar estado atual das senhas")
        print("2. 🚀 Migrar TODAS as senhas para hash")
        print("3. 🔧 Atualizar senha de usuário específico")
        print("4. 🧪 Testar autenticação")
        print("5. 🚪 Sair")
        
        try:
            choice = input("\nEscolha uma opção [1-5]: ").strip()
            
            if choice == "1":
                show_current_passwords()
            elif choice == "2":
                migrate_all_passwords()
            elif choice == "3":
                interactive_password_update()
            elif choice == "4":
                test_authentication_after_migration()
            elif choice == "5":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida! Escolha entre 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()