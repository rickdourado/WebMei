#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados MySQL
"""

import os
import pymysql
from dotenv import load_dotenv

def test_mysql_connection():
    # Carrega variáveis do .env
    load_dotenv()
    
    # Configurações do banco
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'servicosmei'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4')
    }
    
    print("Testando conexão com MySQL...")
    print(f"Host: {config['host']}:{config['port']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print("-" * 50)
    
    try:
        # Tenta conectar
        connection = pymysql.connect(**config)
        print("✅ Conexão estabelecida com sucesso!")
        
        # Testa uma query simples
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Versão do MySQL: {version[0]}")
            
            # Lista as tabelas existentes
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"✅ Tabelas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("ℹ️  Nenhuma tabela encontrada no banco")
        
        connection.close()
        print("✅ Conexão fechada com sucesso!")
        return True
        
    except pymysql.Error as e:
        print(f"❌ Erro de conexão MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_mysql_connection()
    exit(0 if success else 1)