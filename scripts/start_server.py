#!/usr/bin/env python3
"""
Script para iniciar o servidor Flask
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    print("📋 Credenciais disponíveis:")
    print("   - admin / admin123")
    print("   - oportunidades.cariocas@prefeitura.rio / GPCE#2025#")
    print("\n🌐 Acesse: http://localhost:5010")
    print("🔐 Admin: http://localhost:5010/admin/login")
    print("\n⏹️  Para parar: Ctrl+C")
    print("-" * 60)
    
    app.run(host='0.0.0.0', port=5010, debug=True)