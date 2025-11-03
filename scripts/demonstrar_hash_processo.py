#!/usr/bin/env python3
"""
Demonstração prática de como o hash bcrypt funciona com suas senhas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
import bcrypt as bcrypt_lib

def demonstrar_processo():
    print("🔬 Demonstração: Como Suas Senhas Foram Processadas")
    print("=" * 70)
    
    # Senhas originais conhecidas
    senhas_originais = {
        'admin': 'admin123',
        'oportunidades.cariocas@prefeitura.rio': 'GPCE#2025#'
    }
    
    db = DatabaseManager()
    
    try:
        connection = db.get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT login, senha FROM authuser")
            usuarios = cursor.fetchall()
            
            for login, hash_armazenado in usuarios:
                if login in senhas_originais:
                    senha_original = senhas_originais[login]
                    
                    print(f"\n👤 Usuário: {login}")
                    print(f"🔑 Senha original: {senha_original}")
                    print(f"🔐 Hash no banco: {hash_armazenado[:50]}...")
                    
                    # Demonstrar verificação
                    print(f"\n🧪 Teste de verificação:")
                    
                    # Teste 1: Senha correta
                    resultado = bcrypt_lib.checkpw(senha_original.encode('utf-8'), 
                                                 hash_armazenado.encode('utf-8'))
                    print(f"   Senha '{senha_original}': {'✅ APROVADO' if resultado else '❌ NEGADO'}")
                    
                    # Teste 2: Senha errada
                    senha_errada = senha_original + "X"
                    resultado_errado = bcrypt_lib.checkpw(senha_errada.encode('utf-8'), 
                                                        hash_armazenado.encode('utf-8'))
                    print(f"   Senha '{senha_errada}': {'✅ APROVADO' if resultado_errado else '❌ NEGADO'}")
                    
                    # Anatomia do hash
                    print(f"\n🔍 Anatomia do hash:")
                    partes = hash_armazenado.split('$')
                    if len(partes) >= 4:
                        print(f"   Algoritmo: {partes[1]} (bcrypt)")
                        print(f"   Custo: {partes[2]} (2^{partes[2]} = {2**int(partes[2])} iterações)")
                        print(f"   Salt: {partes[3][:22]}...")
                        print(f"   Hash: {partes[3][22:]}...")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def demonstrar_criacao_hash():
    """Demonstra como um hash é criado do zero"""
    print(f"\n" + "=" * 70)
    print("🧮 Demonstração: Criando um Hash do Zero")
    print("=" * 70)
    
    senha_exemplo = "admin123"
    
    print(f"🔑 Senha de exemplo: {senha_exemplo}")
    
    # Gerar 3 hashes diferentes da mesma senha
    print(f"\n🎲 Gerando 3 hashes da MESMA senha:")
    
    for i in range(1, 4):
        salt = bcrypt_lib.gensalt()
        hash_gerado = bcrypt_lib.hashpw(senha_exemplo.encode('utf-8'), salt)
        hash_string = hash_gerado.decode('utf-8')
        
        print(f"\n   Hash #{i}: {hash_string}")
        
        # Testar se funciona
        verificacao = bcrypt_lib.checkpw(senha_exemplo.encode('utf-8'), hash_gerado)
        print(f"   Verifica '{senha_exemplo}': {'✅ SIM' if verificacao else '❌ NÃO'}")
    
    print(f"\n💡 Observe: Mesma senha, hashes diferentes, mas todos verificam corretamente!")

def demonstrar_processo_login():
    """Demonstra o que acontece durante o login"""
    print(f"\n" + "=" * 70)
    print("🚪 Demonstração: O Que Acontece no Login")
    print("=" * 70)
    
    # Simular hash armazenado
    senha_real = "admin123"
    hash_armazenado = bcrypt_lib.hashpw(senha_real.encode('utf-8'), bcrypt_lib.gensalt()).decode('utf-8')
    
    print(f"💾 Hash armazenado no banco: {hash_armazenado[:50]}...")
    
    # Simular tentativas de login
    tentativas = [
        ("admin123", "Senha correta"),
        ("admin124", "Senha com erro de digitação"),
        ("ADMIN123", "Senha em maiúscula"),
        ("admin", "Senha incompleta"),
        ("", "Senha vazia")
    ]
    
    print(f"\n🧪 Simulando tentativas de login:")
    
    for senha_tentativa, descricao in tentativas:
        if senha_tentativa:
            resultado = bcrypt_lib.checkpw(senha_tentativa.encode('utf-8'), hash_armazenado.encode('utf-8'))
        else:
            resultado = False
        
        status = "✅ APROVADO" if resultado else "❌ NEGADO"
        print(f"   '{senha_tentativa}' ({descricao}): {status}")

def mostrar_comparacao_seguranca():
    """Mostra comparação de segurança"""
    print(f"\n" + "=" * 70)
    print("🛡️ Comparação: Antes vs Depois da Migração")
    print("=" * 70)
    
    print(f"\n❌ ANTES (INSEGURO):")
    print(f"   Banco de dados: login='admin', senha='admin123'")
    print(f"   👀 Qualquer pessoa vê: admin123")
    print(f"   💾 Backup expõe: admin123")
    print(f"   🕵️ Logs podem mostrar: admin123")
    
    print(f"\n✅ DEPOIS (SEGURO):")
    print(f"   Banco de dados: login='admin', senha='$2b$12$aT530K4dhk6qi...'")
    print(f"   👀 Pessoa vê: Hash incompreensível")
    print(f"   💾 Backup expõe: Apenas hash inútil")
    print(f"   🕵️ Logs mostram: Hash que não revela senha")
    
    print(f"\n🔑 MAS O LOGIN AINDA FUNCIONA:")
    print(f"   Usuário digita: admin123")
    print(f"   Sistema verifica: ✅ Aprovado!")
    print(f"   Experiência do usuário: Idêntica!")

def main():
    """Função principal com menu"""
    print("🎭 Demonstração Interativa: Hash bcrypt")
    
    while True:
        print(f"\n📋 Escolha uma demonstração:")
        print("1. 🔬 Como suas senhas foram processadas")
        print("2. 🧮 Criação de hash do zero")
        print("3. 🚪 Processo de login simulado")
        print("4. 🛡️ Comparação de segurança")
        print("5. 🎯 Todas as demonstrações")
        print("6. 🚪 Sair")
        
        try:
            escolha = input("\nEscolha [1-6]: ").strip()
            
            if escolha == "1":
                demonstrar_processo()
            elif escolha == "2":
                demonstrar_criacao_hash()
            elif escolha == "3":
                demonstrar_processo_login()
            elif escolha == "4":
                mostrar_comparacao_seguranca()
            elif escolha == "5":
                demonstrar_processo()
                demonstrar_criacao_hash()
                demonstrar_processo_login()
                mostrar_comparacao_seguranca()
            elif escolha == "6":
                print("👋 Saindo...")
                break
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()