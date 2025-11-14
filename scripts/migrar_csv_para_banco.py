#!/usr/bin/env python3
"""
Script para migrar dados de arquivos CSV para o banco de dados MySQL
Portal Empreendedor Unificado
"""

import os
import sys
import csv
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Importa o DatabaseManager
try:
    from backend.database import DatabaseManager
except ImportError:
    print("❌ Erro ao importar DatabaseManager")
    print("   Certifique-se de estar no diretório correto")
    sys.exit(1)

# Cores para output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'

def print_colored(message, color):
    """Imprime mensagem colorida"""
    print(f"{color}{message}{Colors.NC}")

def migrar_csv_para_banco():
    """Migra todos os CSVs da pasta CSV/ para o banco de dados"""
    
    print_colored("🔄 Iniciando migração de CSVs para banco de dados...", Colors.BLUE)
    print()
    
    # Inicializa o gerenciador de banco
    try:
        db_manager = DatabaseManager()
        print_colored("✓ Conexão com banco de dados estabelecida", Colors.GREEN)
    except Exception as e:
        print_colored(f"❌ Erro ao conectar ao banco: {e}", Colors.RED)
        return
    
    # Diretório de CSVs
    csv_dir = root_dir / 'CSV'
    
    if not csv_dir.exists():
        print_colored(f"⚠️  Diretório CSV não encontrado: {csv_dir}", Colors.YELLOW)
        return
    
    # Lista todos os arquivos CSV
    csv_files = list(csv_dir.glob('*.csv'))
    
    if not csv_files:
        print_colored("⚠️  Nenhum arquivo CSV encontrado para migrar", Colors.YELLOW)
        return
    
    print_colored(f"📁 Encontrados {len(csv_files)} arquivos CSV", Colors.BLUE)
    print()
    
    # Contadores
    sucesso = 0
    erros = 0
    duplicados = 0
    
    # Processa cada arquivo
    for csv_file in csv_files:
        try:
            print(f"   Processando: {csv_file.name}...", end=' ')
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = next(reader, None)
                
                if not data:
                    print_colored("❌ Vazio", Colors.RED)
                    erros += 1
                    continue
                
                # Verifica se já existe no banco (por título e órgão)
                # Nota: Isso é uma verificação simples, pode ser melhorada
                
                # Insere no banco
                service_id = db_manager.insert_servico(data)
                
                if service_id:
                    print_colored(f"✓ ID: {service_id}", Colors.GREEN)
                    sucesso += 1
                else:
                    print_colored("❌ Falhou", Colors.RED)
                    erros += 1
                    
        except Exception as e:
            print_colored(f"❌ Erro: {str(e)}", Colors.RED)
            erros += 1
    
    # Resumo
    print()
    print_colored("=" * 60, Colors.BLUE)
    print_colored("📊 RESUMO DA MIGRAÇÃO", Colors.BLUE)
    print_colored("=" * 60, Colors.BLUE)
    print_colored(f"   Total de arquivos: {len(csv_files)}", Colors.BLUE)
    print_colored(f"   ✓ Migrados com sucesso: {sucesso}", Colors.GREEN)
    if erros > 0:
        print_colored(f"   ❌ Erros: {erros}", Colors.RED)
    if duplicados > 0:
        print_colored(f"   ⚠️  Duplicados (ignorados): {duplicados}", Colors.YELLOW)
    print_colored("=" * 60, Colors.BLUE)
    print()
    
    # Pergunta se deseja fazer backup dos CSVs
    if sucesso > 0:
        print_colored("💡 Dica: Os arquivos CSV originais ainda estão na pasta CSV/", Colors.YELLOW)
        print_colored("   Você pode movê-los para uma pasta de backup se desejar.", Colors.YELLOW)
        print()
        
        resposta = input("Deseja mover os CSVs para uma pasta de backup? (s/N): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            backup_dir = root_dir / 'CSV_backup' / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            print()
            print_colored(f"📦 Movendo arquivos para: {backup_dir}", Colors.BLUE)
            
            for csv_file in csv_files:
                try:
                    csv_file.rename(backup_dir / csv_file.name)
                    print(f"   ✓ {csv_file.name}")
                except Exception as e:
                    print_colored(f"   ❌ Erro ao mover {csv_file.name}: {e}", Colors.RED)
            
            print()
            print_colored("✅ Backup concluído!", Colors.GREEN)

if __name__ == '__main__':
    try:
        migrar_csv_para_banco()
    except KeyboardInterrupt:
        print()
        print_colored("⚠️  Migração cancelada pelo usuário", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        print()
        print_colored(f"❌ Erro inesperado: {e}", Colors.RED)
        sys.exit(1)
