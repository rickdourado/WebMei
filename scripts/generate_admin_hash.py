#!/usr/bin/env python3
"""
Script para gerar hash da senha do admin
"""

import bcrypt
import getpass
from dotenv import load_dotenv
import os

def generate_password_hash():
    load_dotenv()
    
    # Pega a senha atual do .env ou solicita uma nova
    current_password = os.getenv('ADMIN_PASSWORD', 'admin')
    
    print("Gerador de Hash para Senha do Admin")
    print("-" * 40)
    print(f"Senha atual no .env: {current_password}")
    
    # Solicita nova senha ou usa a atual
    choice = input("\nDeseja usar a senha atual? (s/n): ").lower().strip()
    
    if choice == 'n':
        password = getpass.getpass("Digite a nova senha do admin: ")
        confirm = getpass.getpass("Confirme a senha: ")
        
        if password != confirm:
            print("❌ Senhas não coincidem!")
            return
    else:
        password = current_password
    
    # Gera o hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hash_string = hashed.decode('utf-8')
    
    print(f"\n✅ Hash gerado com sucesso!")
    print(f"Hash: {hash_string}")
    print(f"\nAdicione esta linha ao seu .env:")
    print(f"ADMIN_PASSWORD_HASH={hash_string}")
    
    # Testa o hash
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        print("✅ Verificação do hash: OK")
    else:
        print("❌ Erro na verificação do hash")

if __name__ == "__main__":
    generate_password_hash()