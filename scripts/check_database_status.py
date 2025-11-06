#!/usr/bin/env python3
"""
Script para verificar status do banco de dados MySQL
Portal Empreendedor - Verificação de Status
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente (procurar na pasta pai também)
load_dotenv()
if not os.path.exists('.env'):
    # Tentar na pasta pai
    load_dotenv('../.env')

def get_db_connection():
    """Retorna conexão com o banco de dados"""
    try:
        import mysql.connector
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'servicosmei'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
            'autocommit': True
        }
        
        return mysql.connector.connect(**config)
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def check_database_structure():
    """Verifica a estrutura atual do banco"""
    
    print("🔍 Verificando estrutura do banco de dados...")
    print()
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Verificar tabelas existentes
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"📊 Tabelas encontradas ({len(tables)}):")
        
        required_tables = ['servicos_mei', 'tipos_atividade', 'especificacoes_atividade']
        existing_tables = [table[0] for table in tables]
        
        for table in tables:
            table_name = table[0]
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            # Verificar se é uma tabela do sistema
            if table_name in required_tables:
                status = "🟢 Sistema"
            else:
                status = "🔵 Existente"
            
            print(f"   {status} {table_name} ({count} registros)")
        
        print()
        print("🎯 Análise das tabelas do sistema:")
        
        for required_table in required_tables:
            if required_table in existing_tables:
                print(f"   ✅ {required_table} - OK")
            else:
                print(f"   ❌ {required_table} - FALTANDO")
        
        # Se servicos_mei existe, mostrar estrutura
        if 'servicos_mei' in existing_tables:
            print("\n🔍 Estrutura da tabela servicos_mei:")
            cursor.execute("DESCRIBE servicos_mei")
            columns = cursor.fetchall()
            
            for column in columns:
                field_name = column[0]
                field_type = column[1]
                null_allowed = "NULL" if column[2] == "YES" else "NOT NULL"
                print(f"   - {field_name}: {field_type} {null_allowed}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")
        return False
        
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    print("=" * 60)
    print("📋 VERIFICAÇÃO DO BANCO DE DADOS - PORTAL EMPREENDEDOR")
    print("=" * 60)
    
    success = check_database_structure()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ VERIFICAÇÃO CONCLUÍDA")
    else:
        print("❌ VERIFICAÇÃO FALHOU")
    print("=" * 60)