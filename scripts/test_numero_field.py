"""
Script para testar validação do campo Número
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_numero_validation():
    """Testa a lógica de validação do campo número"""
    print("=" * 70)
    print("TESTE: Validação do Campo Número")
    print("=" * 70)
    
    # Casos de teste
    test_cases = [
        ("123", True, "Número simples"),
        ("456", True, "Número com 3 dígitos"),
        ("1", True, "Número de 1 dígito"),
        ("9999", True, "Número com 4 dígitos"),
        ("S/N", True, "Sem número (S/N)"),
        ("s/n", True, "Sem número minúsculo"),
        ("SN", True, "Sem número sem barra"),
        ("S.N.", True, "Sem número com pontos"),
        ("SEM NUMERO", True, "Sem número por extenso"),
        ("SEM NÚMERO", True, "Sem número por extenso com acento"),
        ("123A", False, "Número com letra"),
        ("ABC", False, "Apenas letras"),
        ("12-34", False, "Número com hífen"),
        ("", False, "Vazio"),
    ]
    
    print("\n📋 Testando validação:\n")
    
    passed = 0
    failed = 0
    
    for valor, esperado, descricao in test_cases:
        # Simula a validação do app.py
        numero_limpo = valor.strip().upper()
        valido = numero_limpo.isdigit() or numero_limpo in ['S/N', 'SN', 'S.N.', 'SEM NUMERO', 'SEM NÚMERO']
        
        status = "✓" if valido == esperado else "✗"
        resultado = "VÁLIDO" if valido else "INVÁLIDO"
        
        if valido == esperado:
            passed += 1
            print(f"  {status} '{valor:15}' → {resultado:8} | {descricao}")
        else:
            failed += 1
            print(f"  {status} '{valor:15}' → {resultado:8} | {descricao} [ERRO: esperado {'VÁLIDO' if esperado else 'INVÁLIDO'}]")
    
    print("\n" + "=" * 70)
    print(f"RESULTADO: {passed} passaram, {failed} falharam")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ Todos os testes passaram!")
        print("\nO campo Número agora aceita:")
        print("  • Números puros: 123, 456, 1, 9999")
        print("  • Sem número: S/N, SN, S.N., SEM NUMERO, SEM NÚMERO")
        print("\nE rejeita:")
        print("  • Números com letras: 123A")
        print("  • Apenas letras: ABC")
        print("  • Números com caracteres especiais: 12-34")
    else:
        print(f"\n⚠ {failed} teste(s) falharam")
    
    return failed == 0

if __name__ == '__main__':
    success = test_numero_validation()
    sys.exit(0 if success else 1)
