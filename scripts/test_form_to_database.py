"""
Script de teste para validar preenchimento do formulário e inserção na tabela servicos_mei
"""

import sys
import os
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
import pymysql

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("=" * 60)
    print("TESTE 1: Conexão com Banco de Dados")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        print("✓ Conexão estabelecida com sucesso!")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✓ Banco de dados ativo: {db_name}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return False

def test_table_exists():
    """Verifica se a tabela servicos_mei existe"""
    print("\n" + "=" * 60)
    print("TESTE 2: Verificação da Tabela servicos_mei")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = 'servicos_mei'
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                print("✓ Tabela servicos_mei encontrada!")
                
                # Mostra estrutura da tabela
                cursor.execute("DESCRIBE servicos_mei")
                columns = cursor.fetchall()
                print("\nEstrutura da tabela:")
                print("-" * 60)
                for col in columns:
                    print(f"  {col[0]:<30} {col[1]:<20} {col[2]}")
                
                conn.close()
                return True
            else:
                print("✗ Tabela servicos_mei não encontrada!")
                conn.close()
                return False
                
    except Exception as e:
        print(f"✗ Erro ao verificar tabela: {e}")
        return False

def insert_test_service():
    """Insere um serviço de teste na tabela"""
    print("\n" + "=" * 60)
    print("TESTE 3: Inserção de Serviço de Teste")
    print("=" * 60)
    
    # Dados de teste simulando preenchimento do formulário
    test_data = {
        'orgao_demandante': 'Prefeitura Municipal de Teste',
        'titulo_servico': f'Serviço de Teste - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
        'tipo_atividade': 'Construção Civil',
        'especificacao_atividade': 'Pedreiro',
        'descricao_servico': 'Serviço de teste para validar integração do formulário com banco de dados MySQL. Este é um registro de teste criado automaticamente.',
        'outras_informacoes': 'Teste realizado via script automatizado',
        'endereco': 'Rua de Teste',
        'numero': '123',
        'bairro': 'Centro',
        'forma_pagamento': 'Transferência',
        'prazo_pagamento': '30 dias após conclusão',
        'prazo_expiracao': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'data_limite_execucao': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    }
    
    print("\nDados do serviço de teste:")
    print("-" * 60)
    for key, value in test_data.items():
        print(f"  {key:<25}: {value}")
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO servicos_mei (
                    orgao_demandante, titulo_servico, tipo_atividade, 
                    especificacao_atividade, descricao_servico, outras_informacoes,
                    endereco, numero, bairro, forma_pagamento, prazo_pagamento,
                    prazo_expiracao, data_limite_execucao
                ) VALUES (
                    %(orgao_demandante)s, %(titulo_servico)s, %(tipo_atividade)s,
                    %(especificacao_atividade)s, %(descricao_servico)s, %(outras_informacoes)s,
                    %(endereco)s, %(numero)s, %(bairro)s, %(forma_pagamento)s, %(prazo_pagamento)s,
                    %(prazo_expiracao)s, %(data_limite_execucao)s
                )
            """
            
            cursor.execute(sql, test_data)
            conn.commit()
            
            inserted_id = cursor.lastrowid
            print(f"\n✓ Serviço inserido com sucesso! ID: {inserted_id}")
            
        conn.close()
        return inserted_id
        
    except Exception as e:
        print(f"\n✗ Erro ao inserir serviço: {e}")
        return None

def verify_inserted_service(service_id):
    """Verifica se o serviço foi inserido corretamente"""
    print("\n" + "=" * 60)
    print("TESTE 4: Verificação do Serviço Inserido")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM servicos_mei WHERE id = %s
            """, (service_id,))
            
            service = cursor.fetchone()
            
            if service:
                print(f"✓ Serviço ID {service_id} encontrado no banco!")
                print("\nDados recuperados:")
                print("-" * 60)
                for key, value in service.items():
                    print(f"  {key:<25}: {value}")
                
                conn.close()
                return True
            else:
                print(f"✗ Serviço ID {service_id} não encontrado!")
                conn.close()
                return False
                
    except Exception as e:
        print(f"✗ Erro ao verificar serviço: {e}")
        return False

def count_services():
    """Conta total de serviços na tabela"""
    print("\n" + "=" * 60)
    print("TESTE 5: Contagem de Serviços")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM servicos_mei")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM servicos_mei WHERE ativo = TRUE")
            ativos = cursor.fetchone()[0]
            
            print(f"✓ Total de serviços: {total}")
            print(f"✓ Serviços ativos: {ativos}")
            print(f"✓ Serviços inativos: {total - ativos}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Erro ao contar serviços: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "TESTE DE FORMULÁRIO → BANCO DE DADOS" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # Teste 1: Conexão
    results.append(("Conexão com banco", test_database_connection()))
    
    if not results[0][1]:
        print("\n⚠ Testes interrompidos: falha na conexão com banco de dados")
        return
    
    # Teste 2: Tabela existe
    results.append(("Verificação da tabela", test_table_exists()))
    
    if not results[1][1]:
        print("\n⚠ Testes interrompidos: tabela servicos_mei não encontrada")
        print("\nPara criar a tabela, execute:")
        print("  python scripts/create_tables.py")
        return
    
    # Teste 3: Inserção
    service_id = insert_test_service()
    results.append(("Inserção de serviço", service_id is not None))
    
    if service_id:
        # Teste 4: Verificação
        results.append(("Verificação do serviço", verify_inserted_service(service_id)))
    
    # Teste 5: Contagem
    results.append(("Contagem de serviços", count_services()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"  {test_name:<30} {status}")
    
    print("-" * 60)
    print(f"  Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram com sucesso!")
        print("\nO formulário está pronto para inserir dados na tabela servicos_mei.")
    else:
        print(f"\n⚠ {total - passed} teste(s) falharam. Verifique os erros acima.")
    
    print("=" * 60)

if __name__ == '__main__':
    run_all_tests()
