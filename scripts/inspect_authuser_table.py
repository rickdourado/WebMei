#!/usr/bin/env python3
"""
Script para inspecionar a estrutura da tabela authuser
"""

import os
import pymysql
from dotenv import load_dotenv

def inspect_authuser_table():
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'servicosmei'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4')
    }
    
    print("Inspecionando tabela authuser...")
    print("-" * 50)
    
    try:
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # Estrutura da tabela
            cursor.execute("DESCRIBE authuser")
            columns = cursor.fetchall()
            
            print("📋 Estrutura da tabela authuser:")
            for col in columns:
                field, type_info, null, key, default, extra = col
                print(f"   - {field}: {type_info} {'(PK)' if key == 'PRI' else ''}")
            
            print("\n" + "-" * 50)
            
            # Dados existentes (sem mostrar senhas)
            cursor.execute("SELECT COUNT(*) FROM authuser")
            count = cursor.fetchone()[0]
            print(f"📊 Total de registros: {count}")
            
            if count > 0:
                # Mostra apenas login (não senha por segurança)
                cursor.execute("SELECT login FROM authuser LIMIT 5")
                users = cursor.fetchall()
                print(f"\n👥 Usuários cadastrados:")
                for user in users:
                    print(f"   - {user[0]}")
                
                if count > 5:
                    print(f"   ... e mais {count - 5} usuários")
        
        connection.close()
        
    except pymysql.Error as e:
        print(f"❌ Erro MySQL: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    inspect_authuser_table()