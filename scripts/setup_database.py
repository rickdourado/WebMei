#!/usr/bin/env python3
"""
Script para configurar estrutura do banco de dados MySQL
Portal Empreendedor - Setup de Tabelas
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_db_connection():
    """Retorna conexão com o banco de dados"""
    try:
        import mysql.connector
        from mysql.connector import Error
        
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

def check_table_exists(cursor, table_name):
    """Verifica se uma tabela existe"""
    cursor.execute("SHOW TABLES LIKE %s", (table_name,))
    return cursor.fetchone() is not None

def create_servicos_mei_table(cursor):
    """Cria a tabela principal servicos_mei"""
    
    sql = """
    CREATE TABLE servicos_mei (
        id INT AUTO_INCREMENT PRIMARY KEY,
        orgao_demandante VARCHAR(255) NOT NULL COMMENT 'Órgão que está demandando o serviço',
        titulo_servico VARCHAR(255) NOT NULL COMMENT 'Título/nome do serviço',
        tipo_atividade VARCHAR(100) NULL COMMENT 'Categoria/tipo da atividade',
        especificacao_atividade VARCHAR(255) NOT NULL COMMENT 'Especificação detalhada da atividade',
        descricao_servico TEXT NOT NULL COMMENT 'Descrição completa do serviço',
        outras_informacoes TEXT NULL COMMENT 'Informações adicionais opcionais',
        endereco VARCHAR(255) NOT NULL COMMENT 'Endereço onde o serviço será executado',
        numero VARCHAR(20) NOT NULL COMMENT 'Número do endereço',
        bairro VARCHAR(100) NOT NULL COMMENT 'Bairro do endereço',
        forma_pagamento ENUM('Cheque', 'Dinheiro', 'Cartão', 'Transferência') NOT NULL COMMENT 'Forma de pagamento',
        prazo_pagamento VARCHAR(100) NOT NULL COMMENT 'Prazo para pagamento (ex: 30 dias)',
        prazo_expiracao DATE NOT NULL COMMENT 'Data de expiração da oportunidade',
        data_limite_execucao DATE NOT NULL COMMENT 'Data limite para execução do serviço',
        arquivo_csv VARCHAR(255) NULL COMMENT 'Nome do arquivo CSV original (para compatibilidade)',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação do registro',
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data da última atualização',
        ativo BOOLEAN DEFAULT TRUE COMMENT 'Indica se o serviço está ativo/disponível',
        
        -- Índices para melhor performance
        INDEX idx_orgao_demandante (orgao_demandante),
        INDEX idx_tipo_atividade (tipo_atividade),
        INDEX idx_bairro (bairro),
        INDEX idx_prazo_expiracao (prazo_expiracao),
        INDEX idx_data_limite_execucao (data_limite_execucao),
        INDEX idx_ativo (ativo),
        INDEX idx_data_criacao (data_criacao)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela para armazenar oportunidades de serviços para MEI'
    """
    
    cursor.execute(sql)
    print("✅ Tabela 'servicos_mei' criada com sucesso")

def create_tipos_atividade_table(cursor):
    """Cria tabela auxiliar tipos_atividade"""
    
    sql = """
    CREATE TABLE tipos_atividade (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL UNIQUE,
        ativo BOOLEAN DEFAULT TRUE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    cursor.execute(sql)
    print("✅ Tabela 'tipos_atividade' criada com sucesso")

def create_especificacoes_atividade_table(cursor):
    """Cria tabela auxiliar especificacoes_atividade"""
    
    sql = """
    CREATE TABLE especificacoes_atividade (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo_atividade_id INT,
        nome VARCHAR(255) NOT NULL,
        ativo BOOLEAN DEFAULT TRUE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tipo_atividade_id) REFERENCES tipos_atividade(id) ON DELETE SET NULL,
        INDEX idx_tipo_atividade (tipo_atividade_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    cursor.execute(sql)
    print("✅ Tabela 'especificacoes_atividade' criada com sucesso")

def setup_database():
    """Configura a estrutura completa do banco"""
    
    print("🔧 Configurando estrutura do banco de dados...")
    print()
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Verificar tabelas existentes
        tables_to_check = [
            ('servicos_mei', create_servicos_mei_table),
            ('tipos_atividade', create_tipos_atividade_table),
            ('especificacoes_atividade', create_especificacoes_atividade_table)
        ]
        
        for table_name, create_function in tables_to_check:
            if check_table_exists(cursor, table_name):
                print(f"✅ Tabela '{table_name}' já existe")
            else:
                print(f"⏳ Criando tabela '{table_name}'...")
                create_function(cursor)
        
        print()
        print("🎉 Estrutura do banco configurada com sucesso!")
        
        # Mostrar resumo
        print("\n📊 Resumo das tabelas:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]} ({count} registros)")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False
        
    finally:
        if connection.is_connected():
            connection.close()

def show_current_status():
    """Mostra status atual do banco"""
    
    print("📋 Status atual do banco de dados:")
    print()
    
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if not tables:
            print("   ⚠️  Nenhuma tabela encontrada")
            return
        
        for table in tables:
            table_name = table[0]
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            # Verificar se é uma das nossas tabelas principais
            if table_name in ['servicos_mei', 'tipos_atividade', 'especificacoes_atividade']:
                status = "🟢 Sistema"
            else:
                status = "🔵 Outra"
            
            print(f"   {status} {table_name} ({count} registros)")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  SETUP DO BANCO DE DADOS - PORTAL EMPREENDEDOR")
    print("=" * 60)
    
    # Verificar se arquivo .env existe
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        sys.exit(1)
    
    # Mostrar status atual
    show_current_status()
    
    print("\n" + "=" * 40)
    print("🔧 CONFIGURAÇÃO")
    print("=" * 40)
    
    # Perguntar se quer criar as tabelas
    response = input("\n❓ Deseja criar/verificar as tabelas do sistema? (s/N): ").lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        success = setup_database()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("⚠️  CONFIGURAÇÃO FALHOU")
            print("=" * 60)
    else:
        print("\n✋ Configuração cancelada pelo usuário")