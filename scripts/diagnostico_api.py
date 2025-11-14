#!/usr/bin/env python
"""
Script de diagnóstico da API
Verifica todos os componentes necessários
"""

import os
import sys

# Adiciona o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

print("🔍 Diagnóstico da API - Portal Empreendedor")
print("="*60)

# 1. Verifica imports
print("\n1️⃣ Verificando imports...")
try:
    from flask import Flask
    print("  ✅ Flask")
except ImportError as e:
    print(f"  ❌ Flask: {e}")

try:
    from flask_cors import CORS
    print("  ✅ Flask-CORS")
except ImportError as e:
    print(f"  ❌ Flask-CORS: {e}")

try:
    import pymysql
    print("  ✅ PyMySQL")
except ImportError as e:
    print(f"  ❌ PyMySQL: {e}")

try:
    import bcrypt
    print("  ✅ bcrypt")
except ImportError as e:
    print(f"  ❌ bcrypt: {e}")

try:
    from dotenv import load_dotenv
    print("  ✅ python-dotenv")
except ImportError as e:
    print(f"  ❌ python-dotenv: {e}")

# 2. Verifica arquivos
print("\n2️⃣ Verificando arquivos...")
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')

files_to_check = [
    'api.py',
    'database.py',
    '.env',
    'refs/ServicosConsolidados.csv',
    'refs/lista_orgaos.csv',
    'refs/PortalEmpreendedorUnificado.csv'
]

for file in files_to_check:
    filepath = os.path.join(backend_dir, file)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✅ {file} ({size} bytes)")
    else:
        print(f"  ❌ {file} (não encontrado)")

# 3. Verifica diretórios
print("\n3️⃣ Verificando diretórios...")
dirs_to_check = ['CSV', 'refs']

for dir_name in dirs_to_check:
    dirpath = os.path.join(backend_dir, dir_name)
    if os.path.exists(dirpath):
        files_count = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        print(f"  ✅ {dir_name}/ ({files_count} arquivos)")
    else:
        print(f"  ❌ {dir_name}/ (não encontrado)")

# 4. Testa carregamento da API
print("\n4️⃣ Testando carregamento da API...")
try:
    os.chdir(backend_dir)
    
    # Carrega variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
    print("  ✅ Variáveis de ambiente carregadas")
    
    # Tenta importar funções auxiliares
    import csv
    
    def load_unique_ocupacoes(csv_path):
        ocupacoes = []
        vistos = set()
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    valor = (row.get('OCUPACAO') or '').strip()
                    if valor and valor not in vistos:
                        vistos.add(valor)
                        ocupacoes.append(valor)
        except Exception as e:
            print(f"    ⚠️  Erro ao carregar ocupações: {e}")
        return ocupacoes or []
    
    def load_orgaos():
        orgaos = []
        try:
            orgaos_csv = 'refs/lista_orgaos.csv'
            with open(orgaos_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    orgao = (row.get('orgao') or '').strip()
                    if orgao:
                        orgaos.append(orgao)
            orgaos.sort()
        except Exception as e:
            print(f"    ⚠️  Erro ao carregar órgãos: {e}")
        return orgaos
    
    # Testa carregamento
    ocupacoes = load_unique_ocupacoes('refs/ServicosConsolidados.csv')
    print(f"  ✅ Ocupações carregadas: {len(ocupacoes)} itens")
    
    orgaos = load_orgaos()
    print(f"  ✅ Órgãos carregados: {len(orgaos)} itens")
    
except Exception as e:
    print(f"  ❌ Erro ao carregar API: {e}")
    import traceback
    traceback.print_exc()

# 5. Verifica conexão com banco
print("\n5️⃣ Verificando conexão com banco de dados...")
try:
    from database import DatabaseManager
    db = DatabaseManager()
    print("  ✅ DatabaseManager inicializado")
    
    try:
        conn = db.get_connection()
        print("  ✅ Conexão com MySQL estabelecida")
        conn.close()
    except Exception as e:
        print(f"  ⚠️  Não foi possível conectar ao MySQL: {e}")
        print("     (A API funcionará apenas com CSV)")
        
except Exception as e:
    print(f"  ⚠️  Erro ao inicializar DatabaseManager: {e}")
    print("     (A API funcionará apenas com CSV)")

# 6. Resumo
print("\n" + "="*60)
print("📊 RESUMO")
print("="*60)
print("\nPara iniciar a API:")
print("  cd backend")
print("  python api.py")
print("\nPara testar a API:")
print("  python scripts/test_api_simple.py")
print("\nEndpoints disponíveis:")
print("  http://localhost:5010/")
print("  http://localhost:5010/api/config")
print("  http://localhost:5010/api/servicos")
print("\n" + "="*60)
