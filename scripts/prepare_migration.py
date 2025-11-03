#!/usr/bin/env python3
"""
Script para preparar dados para migração ao PythonAnywhere
"""

import os
import sys
import subprocess
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import DatabaseManager
from dotenv import load_dotenv

def export_mysql_data():
    """Exporta dados do MySQL local"""
    load_dotenv()
    
    print("📦 Preparando migração para PythonAnywhere")
    print("=" * 60)
    
    # Configurações do banco local
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'servicosmei')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"🔍 Conectando ao MySQL local: {db_user}@{db_host}/{db_name}")
    
    try:
        # Exportar estrutura e dados da tabela authuser
        dump_file = f"migration/authuser_backup_{timestamp}.sql"
        os.makedirs("migration", exist_ok=True)
        
        cmd = [
            'mysqldump',
            f'-u{db_user}',
            f'-p{db_password}',
            db_name,
            'authuser'
        ]
        
        print(f"📤 Exportando tabela authuser para: {dump_file}")
        
        with open(dump_file, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print("✅ Backup da tabela authuser criado com sucesso!")
            
            # Mostrar conteúdo do backup
            with open(dump_file, 'r') as f:
                content = f.read()
                print(f"📋 Tamanho do backup: {len(content)} caracteres")
                
                # Contar INSERTs
                insert_count = content.count('INSERT INTO')
                print(f"📊 Comandos INSERT encontrados: {insert_count}")
        else:
            print(f"❌ Erro no mysqldump: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ mysqldump não encontrado. Instale o MySQL client.")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

def create_production_env():
    """Cria arquivo .env para produção"""
    print("\n🔧 Criando arquivo .env para produção...")
    
    env_content = """# Configurações Flask para Produção
SECRET_KEY=ALTERE_ESTA_CHAVE_SECRETA_SUPER_FORTE
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_PASSWORD_HASH=$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i

# Configurações MySQL PythonAnywhere
# Substitua 'seu_usuario' pelo seu username do PythonAnywhere
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
DB_NAME=seu_usuario$servicosmei
DB_USER=seu_usuario
DB_PASSWORD=SUA_SENHA_MYSQL_PYTHONANYWHERE
DB_CHARSET=utf8mb4
"""
    
    os.makedirs("migration", exist_ok=True)
    
    with open("migration/.env.production", 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env.production criado em migration/")
    print("⚠️  IMPORTANTE: Edite este arquivo com suas credenciais reais!")

def create_wsgi_file():
    """Cria arquivo WSGI para PythonAnywhere"""
    print("\n🌐 Criando arquivo WSGI...")
    
    wsgi_content = """# WSGI file para PythonAnywhere
# Salve como: /var/www/seu_usuario_pythonanywhere_com_wsgi.py

import sys
import os

# Adicionar o diretório do projeto ao path
# ALTERE 'seu_usuario' para seu username do PythonAnywhere
project_home = '/home/seu_usuario/portal-empreendedor'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar variáveis de ambiente
os.environ['FLASK_ENV'] = 'production'

# Importar a aplicação
from app import app as application

if __name__ == "__main__":
    application.run()
"""
    
    with open("migration/wsgi.py", 'w') as f:
        f.write(wsgi_content)
    
    print("✅ Arquivo wsgi.py criado em migration/")

def list_csv_files():
    """Lista arquivos CSV existentes"""
    print("\n📁 Verificando arquivos CSV existentes...")
    
    csv_dir = "CSV"
    if os.path.exists(csv_dir):
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
        if csv_files:
            print(f"📊 Encontrados {len(csv_files)} arquivos CSV:")
            for f in csv_files[:5]:  # Mostra apenas os primeiros 5
                print(f"   - {f}")
            if len(csv_files) > 5:
                print(f"   ... e mais {len(csv_files) - 5} arquivos")
            
            print(f"\n💡 Lembre-se de fazer upload da pasta CSV/ para o PythonAnywhere")
        else:
            print("📂 Pasta CSV/ existe mas está vazia")
    else:
        print("📂 Pasta CSV/ não encontrada - será criada automaticamente")

def show_migration_summary():
    """Mostra resumo da migração"""
    print("\n" + "=" * 60)
    print("📋 RESUMO DA MIGRAÇÃO")
    print("=" * 60)
    
    print("\n📦 Arquivos criados em migration/:")
    migration_files = []
    if os.path.exists("migration"):
        migration_files = os.listdir("migration")
        for f in migration_files:
            print(f"   ✅ {f}")
    
    print(f"\n🚀 Próximos passos:")
    print("1. Criar conta no PythonAnywhere")
    print("2. Fazer upload do código do projeto")
    print("3. Configurar MySQL no PythonAnywhere")
    print("4. Importar dados: mysql < authuser_backup_*.sql")
    print("5. Configurar .env com credenciais reais")
    print("6. Configurar Web App no dashboard")
    print("7. Testar aplicação")
    
    print(f"\n📖 Documentação completa: docs/deploy-pythonanywhere.md")

def main():
    """Função principal"""
    print("🚀 Preparação para Migração - PythonAnywhere")
    
    # Exportar dados MySQL
    if export_mysql_data():
        print("✅ Dados MySQL exportados")
    else:
        print("⚠️  Falha na exportação MySQL - continue manualmente")
    
    # Criar arquivos de configuração
    create_production_env()
    create_wsgi_file()
    
    # Verificar arquivos CSV
    list_csv_files()
    
    # Mostrar resumo
    show_migration_summary()

if __name__ == "__main__":
    main()