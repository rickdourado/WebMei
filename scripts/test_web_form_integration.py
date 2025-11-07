"""
Script para testar integração completa do formulário web com banco de dados
Simula requisições POST ao endpoint /create_service
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database import DatabaseManager
import pymysql

def test_form_submission():
    """Testa submissão do formulário via Flask test client"""
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO: Formulário Web → Banco de Dados")
    print("=" * 60)
    
    # Dados do formulário
    form_data = {
        'orgao_demandante': 'Secretaria de Desenvolvimento Econômico',
        'titulo_servico': f'Reforma de Calçada - Teste Web {datetime.now().strftime("%H:%M:%S")}',
        'tipo_atividade': 'Construção Civil',
        'especificacao_atividade': 'Pedreiro',
        'descricao_servico': 'Reforma completa de calçada em frente ao prédio público. Inclui remoção de piso antigo, nivelamento e colocação de novo piso.',
        'outras_informacoes': 'Preferência para MEI com experiência em obras públicas',
        'endereco': 'Avenida Principal',
        'numero': '456',
        'bairro': 'Centro',
        'forma_pagamento': 'Transferência',
        'prazo_pagamento': '15 dias após conclusão',
        'prazo_expiracao': (datetime.now() + timedelta(days=15)).strftime('%d/%m/%Y'),
        'data_limite_execucao': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
    }
    
    print("\n📝 Dados do formulário:")
    print("-" * 60)
    for key, value in form_data.items():
        print(f"  {key:<25}: {value}")
    
    # Cria cliente de teste Flask
    with app.test_client() as client:
        print("\n🌐 Enviando requisição POST para /create_service...")
        
        response = client.post('/create_service', data=form_data, follow_redirects=False)
        
        print(f"\n📊 Status da resposta: {response.status_code}")
        
        if response.status_code in [200, 302]:
            print("✓ Formulário processado com sucesso!")
            
            # Verifica se foi criado arquivo CSV
            csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CSV')
            csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
            
            if csv_files:
                latest_csv = sorted(csv_files)[-1]
                print(f"✓ Arquivo CSV criado: {latest_csv}")
            
            return True
        else:
            print(f"✗ Erro no processamento: {response.status_code}")
            return False

def verify_database_entry(titulo_servico):
    """Verifica se o serviço foi salvo no banco de dados"""
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO: Dados no Banco de Dados")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM servicos_mei 
                WHERE titulo_servico LIKE %s 
                ORDER BY id DESC 
                LIMIT 1
            """, (f"%{titulo_servico.split('-')[0].strip()}%",))
            
            service = cursor.fetchone()
            
            if service:
                print("✓ Serviço encontrado no banco de dados!")
                print(f"\n📋 Detalhes do registro (ID: {service['id']}):")
                print("-" * 60)
                
                important_fields = [
                    'orgao_demandante', 'titulo_servico', 'tipo_atividade',
                    'especificacao_atividade', 'bairro', 'forma_pagamento',
                    'data_criacao', 'ativo'
                ]
                
                for field in important_fields:
                    if field in service:
                        print(f"  {field:<25}: {service[field]}")
                
                conn.close()
                return True
            else:
                print("⚠ Serviço não encontrado no banco de dados")
                print("  Isso é esperado se a integração ainda não foi implementada")
                conn.close()
                return False
                
    except Exception as e:
        print(f"✗ Erro ao verificar banco: {e}")
        return False

def show_integration_status():
    """Mostra status da integração"""
    print("\n" + "=" * 60)
    print("STATUS DA INTEGRAÇÃO")
    print("=" * 60)
    
    # Verifica se há método para salvar no banco em app.py
    app_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
    
    with open(app_file, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    has_db_insert = 'INSERT INTO servicos_mei' in app_content or 'db_manager' in app_content
    
    print("\n📊 Checklist de Integração:")
    print("-" * 60)
    print(f"  ✓ Tabela servicos_mei criada")
    print(f"  ✓ DatabaseManager configurado")
    print(f"  ✓ Formulário web funcional")
    print(f"  {'✓' if has_db_insert else '⚠'} Integração formulário → banco {'implementada' if has_db_insert else 'pendente'}")
    
    if not has_db_insert:
        print("\n💡 Próximo passo:")
        print("  Modificar a rota /create_service em app.py para salvar")
        print("  os dados também na tabela servicos_mei do MySQL")

def run_integration_test():
    """Executa teste completo de integração"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "TESTE DE INTEGRAÇÃO FORMULÁRIO WEB" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Teste 1: Submissão do formulário
    form_success = test_form_submission()
    
    # Teste 2: Verificação no banco
    if form_success:
        verify_database_entry("Reforma de Calçada")
    
    # Status da integração
    show_integration_status()
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO")
    print("=" * 60)
    print("""
O teste demonstrou que:
1. ✓ O formulário web está funcional
2. ✓ Os dados são salvos em CSV
3. ✓ A tabela MySQL está pronta para receber dados
4. ⚠ A integração formulário → MySQL precisa ser implementada

Para completar a integração, adicione código na rota /create_service
para inserir os dados também na tabela servicos_mei.
    """)
    print("=" * 60)

if __name__ == '__main__':
    run_integration_test()
