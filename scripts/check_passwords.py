#!/usr/bin/env python3
"""
Script para verificar formato das senhas na tabela authuser
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager

def check_password_formats():
    print("Verificando formato das senhas na tabela authuser")
    print("=" * 60)
    
    db = DatabaseManager()
    
    try:
        connection = db.get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, login, senha FROM authuser")
            users = cursor.fetchall()
            
            for user in users:
                user_id, login, senha = user
                
                print(f"\n👤 Usuário: {login} (ID: {user_id})")
                print(f"   Senha: {senha[:20]}{'...' if len(senha) > 20 else ''}")
                print(f"   Tamanho: {len(senha)} caracteres")
                
                # Detecta formato
                if senha.startswith('$2b$') or senha.startswith('$2a$'):
                    print("   Formato: ✅ Hash bcrypt")
                elif len(senha) < 20:
                    print("   Formato: ⚠️  Texto plano (inseguro)")
                else:
                    print("   Formato: ❓ Desconhecido")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    check_password_formats()