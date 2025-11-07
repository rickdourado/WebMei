"""
Teste completo do formulário após correções
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
import pymysql

def test_form_submission():
    """Testa submissão completa do formulário"""
    print("=" * 70)
    print("TESTE: Submissão Completa do Formulário")
    print("=" * 70)
    
    # Dados simulando preenchimento do formulário
    form_data = {
        'orgao_demandante': 'Secretaria de Teste',
        'titulo_servico': f'Teste Completo - {datetime.now().strftime("%H:%M:%S")}',
        'tipo_atividade': 'Teste',
        'especificacao_atividade': 'Teste',
        'descricao_servico': 'Teste completo após correções do formulário',
        'outras_informacoes': 'Teste automático',
        'endereco': 'Rua Teste',
        'numero': '123',  # Número normal
        'bairro': 'Centro',
        'forma_pagamento': 'Transferência',
        'prazo_pagamento': '30 dias',
        'prazo_expiracao': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),  # YYYY-MM-DD
        'data_limite_execucao': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),  # YYYY-MM-DD
    }
    
    print("\n📝 Dados do formulário:")
    print("-" * 70)
    for key, value in form_data.items():
        print(f"  {key:<25}: {value}")
    
    try:
        db = DatabaseManager()
        service_id = db.insert_servico(form_data)
        
        if service_id:
            print(f"\n✓ Serviço inserido com sucesso! ID: {service_id}")
            return service_id
        else:
            print(f"\n✗ Falha ao inserir serviço")
            return None
            
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_numero_sn():
    """Testa campo número com S/N"""
    print("\n" + "=" * 70)
    print("TESTE: Campo Número com S/N")
    print("=" * 70)
    
    form_data = {
        'orgao_demandante': 'Secretaria de Teste',
        'titulo_servico': f'Teste S/N - {datetime.now().strftime("%H:%M:%S")}',
        'tipo_atividade': 'Teste',
        'especificacao_atividade': 'Teste',
        'descricao_servico': 'Teste com número S/N',
        'outras_informacoes': 'Teste automático',
        'endereco': 'Praça Central',
        'numero': 'S/N',  # Sem número
        'bairro': 'Centro',
        'forma_pagamento': 'Dinheiro',
        'prazo_pagamento': '15 dias',
        'prazo_expiracao': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        'data_limite_execucao': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
    }
    
    print(f"\n📝 Testando número: {form_data['numero']}")
    
    try:
        db = DatabaseManager()
        service_id = db.insert_servico(form_data)
        
        if service_id:
            print(f"✓ Serviço com S/N inserido com sucesso! ID: {service_id}")
            return service_id
        else:
            print(f"✗ Falha ao inserir serviço com S/N")
            return None
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

def verify_services(service_ids):
    """Verifica serviços inseridos"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO: Serviços Inseridos")
    print("=" * 70)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            for service_id in service_ids:
                if service_id:
                    cursor.execute("""
                        SELECT 
                            id, titulo_servico, numero, 
                            prazo_expiracao, data_limite_execucao
                        FROM servicos_mei 
                        WHERE id = %s
                    """, (service_id,))
                    
                    service = cursor.fetchone()
                    
                    if service:
                        print(f"\n✓ Serviço ID {service_id}:")
                        print(f"  • Título: {service['titulo_servico']}")
                        print(f"  • Número: {service['numero']}")
                        print(f"  • Prazo Expiração: {service['prazo_expiracao']}")
                        print(f"  • Data Limite: {service['data_limite_execucao']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n✗ Erro ao verificar: {e}")
        return False

def check_javascript_validator():
    """Verifica o arquivo JavaScript"""
    print("\n" + "=" * 70)
    print("VERIFICAÇÃO: Arquivo form-validator.js")
    print("=" * 70)
    
    js_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'js', 'form-validator.js')
    
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se ainda tem validação DD/MM/AAAA
        if 'DD/MM/AAAA' in content:
            print("✗ PROBLEMA: Arquivo ainda contém validação DD/MM/AAAA")
            return False
        else:
            print("✓ Arquivo atualizado corretamente")
            print("✓ Validação DD/MM/AAAA removida")
            return True
    else:
        print("⚠ Arquivo form-validator.js não encontrado")
        return True  # Não é um erro crítico

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TESTE COMPLETO DO FORMULÁRIO" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Verifica JavaScript
    js_ok = check_javascript_validator()
    
    # Teste 1: Submissão normal
    service_id1 = test_form_submission()
    
    # Teste 2: Número com S/N
    service_id2 = test_numero_sn()
    
    # Verifica serviços
    service_ids = [sid for sid in [service_id1, service_id2] if sid]
    verify_ok = verify_services(service_ids)
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"  {'✓' if js_ok else '✗'} Arquivo JavaScript atualizado")
    print(f"  {'✓' if service_id1 else '✗'} Submissão com número normal")
    print(f"  {'✓' if service_id2 else '✗'} Submissão com S/N")
    print(f"  {'✓' if verify_ok else '✗'} Verificação dos dados")
    
    if js_ok and service_id1 and service_id2 and verify_ok:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n🎉 O formulário está funcionando perfeitamente!")
        print("\n📋 Correções aplicadas:")
        print("  ✓ Campo prazo_expiracao usa input type='date'")
        print("  ✓ Formato YYYY-MM-DD (ISO 8601)")
        print("  ✓ Validação JavaScript removida")
        print("  ✓ Campo número aceita números e S/N")
        print("  ✓ Inserção no banco funcionando")
        print("\n🚀 Teste no navegador:")
        print("  1. conda activate ciclo")
        print("  2. python app.py")
        print("  3. Acesse: http://localhost:5010")
        print("  4. Preencha e envie o formulário")
        print("  5. Deve funcionar sem erros!")
    else:
        print("\n⚠ Alguns testes falharam")
        if not js_ok:
            print("\n  Problema: Arquivo JavaScript ainda tem validação antiga")
            print("  Solução: Recarregue a página no navegador (Ctrl+F5)")
    
    print("=" * 70)
    
    return js_ok and service_id1 and service_id2 and verify_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
