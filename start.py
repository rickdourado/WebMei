#!/usr/bin/env python3
"""
Script para iniciar backend e frontend simultaneamente
Portal Empreendedor Unificado
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def print_colored(message, color):
    """Imprime mensagem colorida"""
    print(f"{color}{message}{Colors.NC}")

def check_conda():
    """Verifica se conda está disponível"""
    try:
        subprocess.run(['conda', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_conda_activate_command():
    """Retorna o comando para ativar o ambiente conda"""
    # Obtém o caminho base do conda
    try:
        result = subprocess.run(['conda', 'info', '--base'],
                              capture_output=True,
                              text=True,
                              check=True)
        conda_base = result.stdout.strip()
        return f"source {conda_base}/etc/profile.d/conda.sh && conda activate ciclo"
    except:
        return "conda activate ciclo"

def main():
    """Função principal"""
    print_colored("🚀 Iniciando Portal Empreendedor...", Colors.BLUE)
    print()
    
    # Verifica conda
    if not check_conda():
        print_colored("❌ Conda não encontrado. Por favor, instale o Anaconda/Miniconda.", Colors.RED)
        sys.exit(1)
    
    print_colored("📦 Ativando ambiente conda 'ciclo'...", Colors.BLUE)
    
    # Diretório raiz do projeto
    root_dir = Path(__file__).parent
    backend_dir = root_dir / 'backend'
    frontend_dir = root_dir / 'frontend'
    
    # Verifica se os diretórios existem
    if not backend_dir.exists():
        print_colored(f"❌ Diretório backend não encontrado: {backend_dir}", Colors.RED)
        sys.exit(1)
    
    if not frontend_dir.exists():
        print_colored(f"❌ Diretório frontend não encontrado: {frontend_dir}", Colors.RED)
        sys.exit(1)
    
    # Lista para armazenar processos
    processes = []
    
    def cleanup(signum=None, frame=None):
        """Encerra todos os processos ao sair"""
        print()
        print_colored("🛑 Encerrando serviços...", Colors.BLUE)
        for proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                proc.kill()
        sys.exit(0)
    
    # Registra handler para Ctrl+C
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    try:
        # Inicia backend
        print_colored("🔧 Iniciando Backend (Flask - porta 5010)...", Colors.BLUE)
        
        # Comando para ativar conda e executar o backend
        backend_cmd = f"{get_conda_activate_command()} && python api.py"
        backend_process = subprocess.Popen(
            backend_cmd,
            shell=True,
            cwd=backend_dir,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(backend_process)
        
        # Aguarda backend iniciar
        print_colored("⏳ Aguardando backend inicializar...", Colors.YELLOW)
        time.sleep(3)
        
        # Inicia frontend
        print_colored("⚛️  Iniciando Frontend (React + Vite - porta 5173)...", Colors.BLUE)
        
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(frontend_process)
        
        print()
        print_colored("✅ Serviços iniciados com sucesso!", Colors.GREEN)
        print()
        print_colored("📍 URLs disponíveis:", Colors.BLUE)
        print_colored("   Backend API:  http://localhost:5010", Colors.GREEN)
        print_colored("   Frontend:     http://localhost:5173", Colors.GREEN)
        print()
        print_colored("💡 Pressione Ctrl+C para encerrar ambos os serviços", Colors.BLUE)
        print()
        
        # Aguarda os processos
        while True:
            # Verifica se algum processo terminou
            for proc in processes:
                if proc.poll() is not None:
                    print_colored(f"⚠️  Um dos serviços encerrou inesperadamente", Colors.YELLOW)
                    cleanup()
            time.sleep(1)
            
    except Exception as e:
        print_colored(f"❌ Erro ao iniciar serviços: {e}", Colors.RED)
        cleanup()
        sys.exit(1)

if __name__ == '__main__':
    main()
