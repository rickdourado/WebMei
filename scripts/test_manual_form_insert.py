"""
Script para testar inserção manual simulando dados do formulário
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
import pymysql

def insert_form_data_to_database():
    """Insere dados simulando preenchimento do formulário"""
    print("=" * 70)
    print("TESTE: Inserção de Dados do Formulário na Tabela servicos_mei")
    print("=" * 70)
    
    # Simula 3 serviços diferentes
    servicos_teste = [
        {
            'orgao_demandante': 'Secretaria Municipal de Obras',
            'titulo_servico': 'Pintura de Escola Municipal',
            'tipo_atividade': 'Pintura',
            'especificacao_atividade': 'Pintor',
            'descricao_servico': 'Pintura interna e externa da Escola Municipal João Silva. Área aproximada de 500m². Inclui preparação de superfície e duas demãos de tinta.',
            'outras_informacoes': 'Material será fornecido pela prefeitura',
            'endereco': 'Rua das Flores',
            'numero': '789',
            'bairro': 'Jardim Primavera',
            'forma_pagamento': 'Cheque',
            'prazo_pagamento': '30 dias após conclusão',
            'prazo_expiracao': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
            'data_limite_execucao': (datetime.now() + timedelta(days=50)).strftime('%Y-%m-%d'),
        },
        {
            'orgao_demandante': 'Secretaria de Saúde',
            'titulo_servico': 'Manutenção Elétrica em UBS',
            'tipo_atividade': 'Serviços Elétricos',
            'especificacao_atividade': 'Eletricista',
            'descricao_servico': 'Manutenção preventiva e corretiva do sistema elétrico da UBS Central. Inclui troca de lâmpadas, verificação de quadros e instalação de novos pontos.',
            'outras_informacoes': 'Trabalho deve ser realizado aos finais de semana',
            'endereco': 'Avenida da Saúde',
            'numero': '1500',
            'bairro': 'Centro',
            'forma_pagamento': 'Transferência',
            'prazo_pagamento': '15 dias após conclusão',
            'prazo_expiracao': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'data_limite_execucao': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        },
        {
            'orgao_demandante': 'Secretaria de Meio Ambiente',
            'titulo_servico': 'Jardinagem em Praça Pública',
            'tipo_atividade': 'Jardinagem',
            'especificacao_atividade': 'Jardineiro',
            'descricao_servico': 'Serviço de jardinagem completo na Praça da Matriz. Inclui poda de árvores, plantio de flores, limpeza de canteiros e manutenção de gramado.',
            'outras_informacoes': 'Serviço mensal com possibilidade de renovação',
            'endereco': 'Praça da Matriz',
            'numero': 'S/N',
            'bairro': 'Centro',
            'forma_pagamento': 'Dinheiro',
            'prazo_pagamento': 'Pagamento ao final de cada mês',
            'prazo_expiracao': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'data_limite_execucao': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
        }
    ]
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        inserted_ids = []
        
        for i, servico in enumerate(servicos_teste, 1):
            print(f"\n📝 Inserindo serviço {i}/3: {servico['titulo_servico']}")
            print("-" * 70)
            
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
                
                cursor.execute(sql, servico)
                conn.commit()
                
                inserted_id = cursor.lastrowid
                inserted_ids.append(inserted_id)
                
                print(f"  ✓ Inserido com sucesso! ID: {inserted_id}")
                print(f"  • Órgão: {servico['orgao_demandante']}")
                print(f"  • Bairro: {servico['bairro']}")
                print(f"  • Pagamento: {servico['forma_pagamento']}")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS SERVIÇOS FORAM INSERIDOS COM SUCESSO!")
        print("=" * 70)
        
        return inserted_ids
        
    except Exception as e:
        print(f"\n❌ Erro ao inserir serviços: {e}")
        return []

def list_all_services():
    """Lista todos os serviços cadastrados"""
    print("\n" + "=" * 70)
    print("LISTAGEM DE TODOS OS SERVIÇOS CADASTRADOS")
    print("=" * 70)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    id, 
                    orgao_demandante, 
                    titulo_servico, 
                    bairro, 
                    forma_pagamento,
                    prazo_expiracao,
                    ativo,
                    data_criacao
                FROM servicos_mei 
                ORDER BY id DESC
            """)
            
            services = cursor.fetchall()
            
            if services:
                print(f"\n📊 Total de serviços: {len(services)}\n")
                
                for service in services:
                    status = "🟢 ATIVO" if service['ativo'] else "🔴 INATIVO"
                    print(f"ID {service['id']:3d} | {status}")
                    print(f"  📋 {service['titulo_servico']}")
                    print(f"  🏢 {service['orgao_demandante']}")
                    print(f"  📍 {service['bairro']}")
                    print(f"  💰 {service['forma_pagamento']}")
                    print(f"  📅 Expira em: {service['prazo_expiracao']}")
                    print(f"  🕐 Criado em: {service['data_criacao']}")
                    print("-" * 70)
            else:
                print("\n⚠ Nenhum serviço encontrado no banco de dados")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Erro ao listar serviços: {e}")

def show_statistics():
    """Mostra estatísticas dos serviços"""
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS")
    print("=" * 70)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Total geral
            cursor.execute("SELECT COUNT(*) as total FROM servicos_mei")
            total = cursor.fetchone()['total']
            
            # Por status
            cursor.execute("SELECT COUNT(*) as total FROM servicos_mei WHERE ativo = TRUE")
            ativos = cursor.fetchone()['total']
            
            # Por forma de pagamento
            cursor.execute("""
                SELECT forma_pagamento, COUNT(*) as total 
                FROM servicos_mei 
                GROUP BY forma_pagamento
                ORDER BY total DESC
            """)
            por_pagamento = cursor.fetchall()
            
            # Por bairro
            cursor.execute("""
                SELECT bairro, COUNT(*) as total 
                FROM servicos_mei 
                GROUP BY bairro
                ORDER BY total DESC
                LIMIT 5
            """)
            por_bairro = cursor.fetchall()
            
            print(f"\n📊 Resumo Geral:")
            print(f"  • Total de serviços: {total}")
            print(f"  • Serviços ativos: {ativos}")
            print(f"  • Serviços inativos: {total - ativos}")
            
            if por_pagamento:
                print(f"\n💰 Por Forma de Pagamento:")
                for item in por_pagamento:
                    print(f"  • {item['forma_pagamento']}: {item['total']}")
            
            if por_bairro:
                print(f"\n📍 Top 5 Bairros:")
                for item in por_bairro:
                    print(f"  • {item['bairro']}: {item['total']}")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Erro ao gerar estatísticas: {e}")

def run_complete_test():
    """Executa teste completo"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TESTE COMPLETO DE FORMULÁRIO → BANCO" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Insere serviços de teste
    inserted_ids = insert_form_data_to_database()
    
    if inserted_ids:
        # Lista todos os serviços
        list_all_services()
        
        # Mostra estatísticas
        show_statistics()
        
        print("\n" + "=" * 70)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("""
A tabela servicos_mei está funcionando perfeitamente!

Próximos passos:
1. ✓ Tabela criada e testada
2. ✓ Inserção de dados funcionando
3. ⚠ Integrar a rota /create_service do Flask para salvar no MySQL
4. ⚠ Atualizar rotas de listagem para buscar do MySQL

Para integrar com o formulário web, modifique app.py na rota
/create_service para incluir a inserção no banco de dados.
        """)
        print("=" * 70)
    else:
        print("\n❌ Teste falhou. Verifique os erros acima.")

if __name__ == '__main__':
    run_complete_test()
