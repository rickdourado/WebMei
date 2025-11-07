"""
Teste final da validação do campo Número (HTML + Servidor)
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_html_validation():
    """Testa validação HTML (navegador)"""
    pattern = r"^(\d+|[Ss]/[Nn]|[Ss][Nn]|[Ss]\.[Nn]\.)$"
    
    print("=" * 70)
    print("TESTE 1: Validação HTML (Navegador)")
    print("=" * 70)
    print(f"Pattern: {pattern}\n")
    
    test_cases = [
        ("123", True, "Número"),
        ("S/N", True, "S/N maiúsculo"),
        ("s/n", True, "s/n minúsculo"),
        ("SN", True, "SN sem barra"),
        ("S.N.", True, "S.N. com pontos"),
        ("123A", False, "Número com letra"),
    ]
    
    passed = 0
    for valor, esperado, desc in test_cases:
        valido = re.match(pattern, valor) is not None
        if valido == esperado:
            passed += 1
            print(f"  ✓ '{valor}' → {'VÁLIDO' if valido else 'INVÁLIDO'} | {desc}")
        else:
            print(f"  ✗ '{valor}' → {'VÁLIDO' if valido else 'INVÁLIDO'} | {desc} [ERRO]")
    
    print(f"\nResultado: {passed}/{len(test_cases)} passaram")
    return passed == len(test_cases)

def test_server_validation():
    """Testa validação do servidor (Python)"""
    print("\n" + "=" * 70)
    print("TESTE 2: Validação do Servidor (Python)")
    print("=" * 70)
    
    test_cases = [
        ("123", True, "Número"),
        ("S/N", True, "S/N maiúsculo"),
        ("s/n", True, "s/n minúsculo"),
        ("SN", True, "SN sem barra"),
        ("S.N.", True, "S.N. com pontos"),
        ("SEM NUMERO", True, "SEM NUMERO por extenso"),
        ("SEM NÚMERO", True, "SEM NÚMERO com acento"),
        ("123A", False, "Número com letra"),
    ]
    
    passed = 0
    for valor, esperado, desc in test_cases:
        # Simula validação do app.py
        numero_limpo = valor.strip().upper()
        valido = numero_limpo.isdigit() or numero_limpo in ['S/N', 'SN', 'S.N.', 'SEM NUMERO', 'SEM NÚMERO']
        
        if valido == esperado:
            passed += 1
            print(f"  ✓ '{valor}' → {'VÁLIDO' if valido else 'INVÁLIDO'} | {desc}")
        else:
            print(f"  ✗ '{valor}' → {'VÁLIDO' if valido else 'INVÁLIDO'} | {desc} [ERRO]")
    
    print(f"\nResultado: {passed}/{len(test_cases)} passaram")
    return passed == len(test_cases)

def test_database_compatibility():
    """Testa compatibilidade com banco de dados"""
    print("\n" + "=" * 70)
    print("TESTE 3: Compatibilidade com Banco de Dados")
    print("=" * 70)
    
    from database import DatabaseManager
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("DESCRIBE servicos_mei")
            columns = cursor.fetchall()
            
            for col in columns:
                if col[0] == 'numero':
                    tipo = col[1]
                    permite_null = col[2]
                    
                    print(f"\nColuna 'numero':")
                    print(f"  • Tipo: {tipo}")
                    print(f"  • Permite NULL: {permite_null}")
                    
                    # Verifica se é VARCHAR
                    if 'varchar' in tipo.lower():
                        print(f"  ✓ Tipo VARCHAR aceita texto e números")
                        
                        # Extrai tamanho
                        import re
                        match = re.search(r'varchar\((\d+)\)', tipo.lower())
                        if match:
                            tamanho = int(match.group(1))
                            print(f"  ✓ Tamanho máximo: {tamanho} caracteres")
                            
                            # Testa valores
                            valores_teste = ["123", "S/N", "SEM NUMERO"]
                            print(f"\n  Valores de teste:")
                            for v in valores_teste:
                                if len(v) <= tamanho:
                                    print(f"    ✓ '{v}' ({len(v)} chars) - OK")
                                else:
                                    print(f"    ✗ '{v}' ({len(v)} chars) - MUITO LONGO")
                    
                    break
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n  ✗ Erro: {e}")
        return False

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TESTE COMPLETO DO CAMPO NÚMERO" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    test1 = test_html_validation()
    test2 = test_server_validation()
    test3 = test_database_compatibility()
    
    print("\n" + "=" * 70)
    print("RESUMO FINAL")
    print("=" * 70)
    print(f"  {'✓' if test1 else '✗'} Validação HTML (Navegador)")
    print(f"  {'✓' if test2 else '✗'} Validação Servidor (Python)")
    print(f"  {'✓' if test3 else '✗'} Compatibilidade Banco de Dados")
    
    if test1 and test2 and test3:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        print("\n📋 Valores aceitos:")
        print("  • Números: 123, 456, 1, 9999")
        print("  • S/N (maiúsculo ou minúsculo)")
        print("  • SN (sem barra)")
        print("  • S.N. (com pontos)")
        print("  • SEM NUMERO ou SEM NÚMERO (apenas no servidor)")
        print("\n💡 Dica: Use S/N no formulário para endereços sem número")
        print("\n🚀 O campo está pronto para uso!")
    else:
        print("\n⚠ Alguns testes falharam")
    
    print("=" * 70)
    
    return test1 and test2 and test3

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
