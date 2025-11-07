"""
Script para testar a validação HTML do campo Número
"""

import re

def test_html_pattern():
    """Testa o pattern HTML do campo número"""
    
    # Pattern do HTML
    pattern = r"^(\d+|[Ss]/[Nn]|[Ss][Nn]|[Ss]\.[Nn]\.|[Ss][Ee][Mm]\s*[NnÚú][Uu][Mm][Ee][Rr][Oo])$"
    
    print("=" * 70)
    print("TESTE: Validação HTML do Campo Número")
    print("=" * 70)
    print(f"\nPattern HTML: {pattern}\n")
    
    # Casos de teste
    test_cases = [
        # (valor, esperado, descrição)
        ("123", True, "Número simples"),
        ("456", True, "Número com 3 dígitos"),
        ("1", True, "Número de 1 dígito"),
        ("9999", True, "Número com 4 dígitos"),
        ("12345", True, "Número com 5 dígitos"),
        ("S/N", True, "Sem número maiúsculo (S/N)"),
        ("s/n", True, "Sem número minúsculo (s/n)"),
        ("S/n", True, "Sem número misto (S/n)"),
        ("s/N", True, "Sem número misto (s/N)"),
        ("SN", True, "Sem número sem barra maiúsculo"),
        ("sn", True, "Sem número sem barra minúsculo"),
        ("Sn", True, "Sem número sem barra misto"),
        ("S.N.", True, "Sem número com pontos maiúsculo"),
        ("s.n.", True, "Sem número com pontos minúsculo"),
        ("SEM NUMERO", True, "Sem número por extenso"),
        ("sem numero", True, "Sem número por extenso minúsculo"),
        ("Sem Numero", True, "Sem número por extenso misto"),
        ("SEM NÚMERO", True, "Sem número por extenso com acento"),
        ("sem número", True, "Sem número por extenso minúsculo com acento"),
        ("123A", False, "Número com letra"),
        ("ABC", False, "Apenas letras"),
        ("12-34", False, "Número com hífen"),
        ("", False, "Vazio"),
        ("S N", False, "S N com espaço"),
        ("S/", False, "S/ incompleto"),
        ("/N", False, "/N incompleto"),
    ]
    
    print("📋 Testando validação HTML:\n")
    
    passed = 0
    failed = 0
    
    for valor, esperado, descricao in test_cases:
        # Testa com regex
        match = re.match(pattern, valor)
        valido = match is not None
        
        status = "✓" if valido == esperado else "✗"
        resultado = "VÁLIDO" if valido else "INVÁLIDO"
        
        if valido == esperado:
            passed += 1
            print(f"  {status} '{valor:20}' → {resultado:8} | {descricao}")
        else:
            failed += 1
            print(f"  {status} '{valor:20}' → {resultado:8} | {descricao} [ERRO]")
    
    print("\n" + "=" * 70)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ Todos os testes passaram!")
        print("\nO pattern HTML aceita:")
        print("  • Números: 123, 456, 1, 9999, 12345")
        print("  • S/N (qualquer combinação de maiúsculas/minúsculas)")
        print("  • SN (sem barra)")
        print("  • S.N. (com pontos)")
        print("  • SEM NUMERO ou SEM NÚMERO (por extenso)")
        print("\nE rejeita:")
        print("  • Números com letras: 123A")
        print("  • Apenas letras: ABC")
        print("  • Números com caracteres especiais: 12-34")
        print("  • Formatos incorretos: S N, S/, /N")
    else:
        print(f"\n⚠ {failed} teste(s) falharam")
    
    return failed == 0

if __name__ == '__main__':
    import sys
    success = test_html_pattern()
    sys.exit(0 if success else 1)
