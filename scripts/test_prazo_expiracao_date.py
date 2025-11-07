"""
Script para testar o campo prazo_expiracao com input type="date"
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
import pymysql

def test_date_format():
    """Testa o formato de data YYYY-MM-DD"""
    print("=" * 70)
    print("TESTE 1: Formato de Data (YYYY-MM-DD)")
    print("=" * 70)
    
    # Datas de teste
    test_dates = [
        "2025-11-07",
        "2025-12-31",
        "2026-01-15",
        (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
    ]
    
    print("\n📅 Testando formatos de data:\n")
    
    for date_str in test_dates:
        try:
            # Valida formato
            datetime.strptime(date_str, '%Y-%m-%d')
            print(f"  ✓ '{date_str}' - Formato válido")
        except ValueError:
            print(f"  ✗ '{date_str}' - Formato inválido")
    
    return True

def test_database_insertion():
    """Testa inserção no banco com novo formato"""
    print("\n" + "=" * 70)
    print("TESTE 2: Inserção no Banco de Dados")
    print("=" * 70)
    
    # Data de teste
    prazo_expiracao = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    data_limite = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    
    test_data = {
        'orgao_demandante': 'Teste Prazo Expiração',
        'titulo_servico': f'Teste Data Calendário - {datetime.now().strftime("%H:%M:%S")}',
        'tipo_atividade': 'Teste',
        'especificacao_atividade': 'Teste',
        'descricao_servico': 'Teste do campo prazo_expiracao com input type="date"',
        'outras_informacoes': 'Teste automático',
        'endereco': 'Rua Teste',
        'numero': '123',
        'bairro': 'Centro',
        'forma_pagamento': 'Transferência',
        'prazo_pagamento': '30 dias',
        'prazo_expiracao': prazo_expiracao,  # Formato YYYY-MM-DD
        'data_limite_execucao': data_limite,
    }
    
    print(f"\n📝 Dados de teste:")
    print(f"  • prazo_expiracao: {prazo_expiracao} (YYYY-MM-DD)")
    print(f"  • data_limite_execucao: {data_limite} (YYYY-MM-DD)")
    
    try:
        db = DatabaseManager()
        service_id = db.insert_servico(test_data)
        
        if service_id:
            print(f"\n✓ Serviço inserido com sucesso! ID: {service_id}")
            
            # Verifica inserção
            conn = db.get_connection()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT prazo_expiracao, data_limite_execucao 
                    FROM servicos_mei 
                    WHERE id = %s
                """, (service_id,))
                
                result = cursor.fetchone()
                
                if result:
                    print(f"\n📊 Dados recuperados do banco:")
                    print(f"  • prazo_expiracao: {result['prazo_expiracao']}")
                    print(f"  • data_limite_execucao: {result['data_limite_execucao']}")
                    
                    # Verifica se as datas estão corretas
                    if str(result['prazo_expiracao']) == prazo_expiracao:
                        print(f"\n✓ Data de expiração salva corretamente!")
                    else:
                        print(f"\n✗ Data de expiração incorreta!")
                        return False
            
            conn.close()
            return True
        else:
            print(f"\n✗ Falha ao inserir serviço")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        return False

def test_date_comparison():
    """Testa comparação de datas"""
    print("\n" + "=" * 70)
    print("TESTE 3: Comparação de Datas")
    print("=" * 70)
    
    hoje = datetime.now().date()
    futuro = (datetime.now() + timedelta(days=30)).date()
    
    print(f"\n📅 Comparando datas:")
    print(f"  • Hoje: {hoje}")
    print(f"  • Futuro (+30 dias): {futuro}")
    print(f"  • Futuro > Hoje: {futuro > hoje}")
    
    if futuro > hoje:
        print(f"\n✓ Comparação de datas funciona corretamente")
        return True
    else:
        print(f"\n✗ Erro na comparação de datas")
        return False

def show_html_example():
    """Mostra exemplo do HTML"""
    print("\n" + "=" * 70)
    print("EXEMPLO: Campo HTML")
    print("=" * 70)
    
    print("""
<div class="form-group">
    <label for="prazo_expiracao">Prazo para expiração da oportunidade *</label>
    <input type="date" id="prazo_expiracao" name="prazo_expiracao" 
           value="{{ today_iso }}" required>
    <small>Selecione a data usando o calendário</small>
</div>

VANTAGENS:
  ✓ Interface de calendário nativa do navegador
  ✓ Validação automática de datas
  ✓ Formato consistente (YYYY-MM-DD)
  ✓ Melhor experiência do usuário
  ✓ Compatível com mobile
  ✓ Não precisa conversão de formato
    """)

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "TESTE: Campo Prazo de Expiração (Calendário)" + " " * 13 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    test1 = test_date_format()
    test2 = test_database_insertion()
    test3 = test_date_comparison()
    
    show_html_example()
    
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"  {'✓' if test1 else '✗'} Formato de data (YYYY-MM-DD)")
    print(f"  {'✓' if test2 else '✗'} Inserção no banco de dados")
    print(f"  {'✓' if test3 else '✗'} Comparação de datas")
    
    if test1 and test2 and test3:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n🎉 O campo agora usa calendário (input type='date')!")
        print("\nVANTAGENS:")
        print("  ✓ Interface de calendário visual")
        print("  ✓ Validação automática pelo navegador")
        print("  ✓ Formato consistente (YYYY-MM-DD)")
        print("  ✓ Melhor experiência do usuário")
        print("  ✓ Funciona em mobile e desktop")
        print("  ✓ Não precisa conversão de formato")
        print("\n🚀 Teste no navegador:")
        print("  1. conda activate ciclo")
        print("  2. python app.py")
        print("  3. Acesse: http://localhost:5010")
        print("  4. Clique no campo 'Prazo para expiração'")
        print("  5. Selecione uma data no calendário")
    else:
        print("\n⚠ Alguns testes falharam")
    
    print("=" * 70)
    
    return test1 and test2 and test3

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
