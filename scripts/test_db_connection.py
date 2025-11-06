#!/usr/bin/env python3
"""
Script para testar conexão com banco de dados MySQL
Portal Empreendedor - Teste de Conectividade
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente (procurar na pasta pai também)
load_dotenv()
if not os.path.exists('.env'):
    # Tentar na pasta pai
    load_dotenv('../.env')

def test_mysql_connection():
    """Testa a conexão com o banco MySQL usando as configurações do .env"""
    
    try:
        import mysql.connector
        from mysql.connector import Error
    except ImportError:
        print("❌ Erro: mysql-connector-python não está instalado")
        print("Execute: pip install mysql-connector-python")
        return False
    
    # Configurações do banco
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_NAME', 'servicosmei'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
        'autocommit': True
    }
    
    print("🔍 Testando conexão com MySQL...")
    print(f"   Host: {config['host']}:{config['port']}")
    print(f"   Database: {config['database']}")
    print(f"   User: {config['user']}")
    print(f"   Charset: {config['charset']}")
    print()
    
    connection = None
    
    try:
        # Tentar conectar
        print("⏳ Conectando...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Conexão estabelecida com sucesso!")
            
            # Informações do servidor
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   Versão do MySQL: {version[0]}")
            
            # Verificar se o banco existe
            cursor.execute("SHOW DATABASES LIKE %s", (config['database'],))
            db_exists = cursor.fetchone()
            
            if db_exists:
                print(f"✅ Banco de dados '{config['database']}' encontrado")
                
                # Listar tabelas existentes
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"   Tabelas encontradas ({len(tables)}):")
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                        count = cursor.fetchone()[0]
                        print(f"   - {table[0]} ({count} registros)")
                else:
                    print("   ⚠️  Nenhuma tabela encontrada no banco")
                    
            else:
                print(f"⚠️  Banco de dados '{config['database']}' não existe")
                print("   Você pode criá-lo com: CREATE DATABASE servicosmei;")
            
            cursor.close()
            return True
            
    except Error as e:
        print(f"❌ Erro de conexão: {e}")
        
        # Diagnósticos específicos
        if "Access denied" in str(e):
            print("   💡 Verifique usuário e senha no arquivo .env")
        elif "Can't connect to MySQL server" in str(e):
            print("   💡 Verifique se o MySQL está rodando")
            print("   💡 Verifique host e porta no arquivo .env")
        elif "Unknown database" in str(e):
            print(f"   💡 Crie o banco: CREATE DATABASE {config['database']};")
            
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("🔌 Conexão fechada")

def test_without_database():
    """Testa conexão sem especificar banco (para diagnóstico)"""
    
    try:
        import mysql.connector
        from mysql.connector import Error
    except ImportError:
        return False
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4')
    }
    
    print("\n🔍 Testando conexão básica (sem banco específico)...")
    
    try:
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Conexão básica OK - MySQL está acessível")
            
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print("   Bancos disponíveis:")
            for db in databases:
                print(f"   - {db[0]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Erro na conexão básica: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO - PORTAL EMPREENDEDOR")
    print("=" * 60)
    
    # Verificar se arquivo .env existe
    if not os.path.exists('.env') and not os.path.exists('../.env'):
        print("❌ Arquivo .env não encontrado!")
        print("   Crie o arquivo .env com as configurações do banco")
        print("   Procurado em: . e ../")
        sys.exit(1)
    
    # Teste principal
    success = test_mysql_connection()
    
    # Se falhou, tentar diagnóstico
    if not success:
        print("\n" + "=" * 40)
        print("🔧 DIAGNÓSTICO")
        print("=" * 40)
        test_without_database()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("⚠️  TESTE FALHOU - Verifique as configurações")
    print("=" * 60)