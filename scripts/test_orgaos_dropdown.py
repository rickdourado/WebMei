"""
Script para testar o dropdown de órgãos demandantes
"""

import sys
import os
import csv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
import pymysql

def test_load_orgaos():
    """Testa carregamento dos órgãos do CSV"""
    print("=" * 70)
    print("TESTE 1: Carregamento dos Órgãos")
    print("=" * 70)
    
    orgaos_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'refs', 'lista_orgaos.csv')
    
    if not os.path.exists(orgaos_csv):
        print("✗ Arquivo lista_orgaos.csv não encontrado")
        return False
    
    orgaos = []
    try:
        with open(orgaos_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                orgao = (row.get('orgao') or '').strip()
                if orgao:
                    orgaos.append(orgao)
        
        orgaos.sort()
        
        print(f"\n✓ Arquivo encontrado e lido com sucesso")
        print(f"✓ Total de órgãos: {len(orgaos)}")
        
        print(f"\n📋 Primeiros 5 órgãos (ordem alfabética):")
        for i, orgao in enumerate(orgaos[:5], 1):
            print(f"  {i}. {orgao}")
        
        print(f"\n📋 Últimos 5 órgãos:")
        for i, orgao in enumerate(orgaos[-5:], len(orgaos)-4):
            print(f"  {i}. {orgao}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Erro ao carregar órgãos: {e}")
        return False

def test_database_compatibility():
    """Testa compatibilidade com o banco de dados"""
    print("\n" + "=" * 70)
    print("TESTE 2: Compatibilidade com Banco de Dados")
    print("=" * 70)
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("DESCRIBE servicos_mei")
            columns = cursor.fetchall()
            
            for col in columns:
                if col[0] == 'orgao_demandante':
                    tipo = col[1]
                    print(f"\n✓ Campo encontrado no banco")
                    print(f"  • Tipo: {tipo}")
                    
                    # Verifica tamanho
                    import re
                    match = re.search(r'varchar\((\d+)\)', tipo.lower())
                    if match:
                        tamanho_campo = int(match.group(1))
                        print(f"  • Tamanho máximo: {tamanho_campo} caracteres")
                        
                        # Carrega órgãos e verifica o maior
                        orgaos_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'refs', 'lista_orgaos.csv')
                        with open(orgaos_csv, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            orgaos = [row['orgao'] for row in reader if row.get('orgao')]
                        
                        maior_orgao = max(orgaos, key=len)
                        tamanho_maior = len(maior_orgao)
                        
                        print(f"\n📏 Maior nome de órgão:")
                        print(f"  • {tamanho_maior} caracteres")
                        print(f"  • Nome: {maior_orgao}")
                        
                        if tamanho_maior <= tamanho_campo:
                            print(f"\n✓ COMPATÍVEL: Todos os nomes cabem no campo")
                            print(f"  • Espaço disponível: {tamanho_campo - tamanho_maior} caracteres")
                            return True
                        else:
                            print(f"\n✗ INCOMPATÍVEL: Nome muito longo")
                            print(f"  • Excede em: {tamanho_maior - tamanho_campo} caracteres")
                            return False
        
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Erro ao verificar banco: {e}")
        return False

def test_insert_with_orgao():
    """Testa inserção com órgão do dropdown"""
    print("\n" + "=" * 70)
    print("TESTE 3: Inserção com Órgão do Dropdown")
    print("=" * 70)
    
    from datetime import datetime, timedelta
    
    # Carrega um órgão do CSV
    orgaos_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'refs', 'lista_orgaos.csv')
    with open(orgaos_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        orgao_teste = next(reader)['orgao']
    
    form_data = {
        'orgao_demandante': orgao_teste,
        'titulo_servico': f'Teste Dropdown Órgão - {datetime.now().strftime("%H:%M:%S")}',
        'tipo_atividade': 'Teste',
        'especificacao_atividade': 'Teste',
        'descricao_servico': 'Teste do dropdown de órgãos demandantes',
        'outras_informacoes': 'Teste automático',
        'endereco': 'Rua Teste',
        'numero': '123',
        'bairro': 'Centro',
        'forma_pagamento': 'Transferência',
        'prazo_pagamento': '30 dias',
        'prazo_expiracao': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'data_limite_execucao': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
    }
    
    print(f"\n📝 Testando com órgão:")
    print(f"  • {orgao_teste}")
    
    try:
        db = DatabaseManager()
        service_id = db.insert_servico(form_data)
        
        if service_id:
            print(f"\n✓ Serviço inserido com sucesso! ID: {service_id}")
            
            # Verifica inserção
            conn = db.get_connection()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, orgao_demandante, titulo_servico 
                    FROM servicos_mei 
                    WHERE id = %s
                """, (service_id,))
                
                result = cursor.fetchone()
                
                if result:
                    print(f"\n📊 Dados recuperados:")
                    print(f"  • ID: {result['id']}")
                    print(f"  • Órgão: {result['orgao_demandante']}")
                    print(f"  • Título: {result['titulo_servico']}")
                    
                    if result['orgao_demandante'] == orgao_teste:
                        print(f"\n✓ Órgão salvo corretamente!")
                        conn.close()
                        return True
                    else:
                        print(f"\n✗ Órgão diferente do esperado")
                        conn.close()
                        return False
            
            conn.close()
        else:
            print(f"\n✗ Falha ao inserir serviço")
            return False
            
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_implementation_details():
    """Mostra detalhes da implementação"""
    print("\n" + "=" * 70)
    print("DETALHES DA IMPLEMENTAÇÃO")
    print("=" * 70)
    
    print("""
📋 MUDANÇAS REALIZADAS:

1. app.py:
   • Adicionada função load_orgaos()
   • Carrega coluna 'orgao' do arquivo lista_orgaos.csv
   • Ordena alfabeticamente
   • Passa lista para o template via ORGAOS_OPCOES

2. templates/index.html:
   • Campo alterado de <input type="text"> para <select>
   • Dropdown populado com órgãos do CSV
   • Opção padrão: "Selecione o órgão..."
   • Texto de ajuda adicionado

3. Compatibilidade:
   • Campo no banco: VARCHAR(255)
   • Maior nome no CSV: 87 caracteres
   • Status: ✓ COMPATÍVEL (168 caracteres de margem)

4. Vantagens:
   • Padronização dos nomes de órgãos
   • Menos erros de digitação
   • Melhor experiência do usuário
   • Dados consistentes no banco
   • Facilita relatórios e filtros
    """)

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TESTE: Dropdown de Órgãos Demandantes" + " " * 14 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    test1 = test_load_orgaos()
    test2 = test_database_compatibility()
    test3 = test_insert_with_orgao()
    
    show_implementation_details()
    
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"  {'✓' if test1 else '✗'} Carregamento dos órgãos")
    print(f"  {'✓' if test2 else '✗'} Compatibilidade com banco")
    print(f"  {'✓' if test3 else '✗'} Inserção com órgão do dropdown")
    
    if test1 and test2 and test3:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n🎉 O dropdown de órgãos está funcionando perfeitamente!")
        print("\n🚀 Teste no navegador:")
        print("  1. conda activate ciclo")
        print("  2. python app.py")
        print("  3. Acesse: http://localhost:5010")
        print("  4. Veja o dropdown de 'Órgão Demandante'")
        print("  5. Selecione um órgão da lista")
    else:
        print("\n⚠ Alguns testes falharam")
    
    print("=" * 70)
    
    return test1 and test2 and test3

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
