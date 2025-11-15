# Como Funciona o Hash de Senhas - Explicação Técnica

## 🔐 O que é Hash de Senha?

Hash de senha é uma técnica de segurança que transforma uma senha em texto plano em uma string criptografada irreversível. É como criar uma "impressão digital" única da senha que não pode ser revertida para obter a senha original.

## 🧮 Algoritmo bcrypt

O **bcrypt** é um algoritmo de hash especificamente projetado para senhas, baseado no cipher Blowfish. Ele possui características importantes:

- **Lento por design**: Dificulta ataques de força bruta
- **Salt automático**: Cada hash é único, mesmo para senhas iguais
- **Custo adaptativo**: Pode ser ajustado conforme o poder computacional aumenta

## 🔄 Processo de Hash no Sistema

### 1. Geração do Hash (Cadastro/Alteração)

```python
import bcrypt

# Senha original
senha = "admin"

# Gera salt aleatório (fator de custo 12)
salt = bcrypt.gensalt()  # Exemplo: $2b$12$N6t8R6Fl5hhEAD7Sw6EgEu

# Cria o hash
hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
# Resultado: $2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i
```

### 2. Verificação do Hash (Login)

```python
# Senha digitada pelo usuário
senha_digitada = "admin"

# Hash armazenado no banco/arquivo
hash_armazenado = "$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i"

# Verifica se a senha está correta
is_valid = bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_armazenado.encode('utf-8'))
# Retorna: True ou False
```

## 🔍 Anatomia do Hash bcrypt

Um hash bcrypt tem a seguinte estrutura:

```
$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i
│ │  │  │                    │
│ │  │  │                    └── Hash da senha (31 chars)
│ │  │  └────────────────────── Salt (22 chars)
│ │  └───────────────────────── Custo/Rounds (12 = 2^12 = 4096 iterações)
│ └──────────────────────────── Versão do algoritmo (2b)
└─────────────────────────────── Identificador bcrypt ($)
```

## 🛡️ Implementação no Sistema

### Arquivo: `app.py`

```python
def verify_admin_password(password):
    """Verifica a senha do admin usando hash ou texto plano (fallback)"""
    if ADMIN_PASSWORD_HASH:
        # Usa hash se disponível (SEGURO)
        try:
            return bcrypt_lib.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8'))
        except Exception:
            return False
    else:
        # Fallback para senha em texto plano (INSEGURO - apenas desenvolvimento)
        return password == ADMIN_PASSWORD
```

### Fluxo de Login

1. **Usuário digita senha** → `"admin"`
2. **Sistema pega hash do .env** → `$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu...`
3. **bcrypt.checkpw() faz a mágica**:
   - Extrai o salt do hash armazenado
   - Aplica o mesmo salt na senha digitada
   - Compara os hashes resultantes
4. **Retorna True/False** → Login aprovado/negado

## 🔒 Vantagens de Segurança

### ✅ Proteção contra Vazamentos
- Se o banco for comprometido, as senhas reais não são expostas
- Apenas hashes inúteis para atacantes

### ✅ Proteção contra Rainbow Tables
- Salt único torna cada hash diferente
- Mesmo senhas iguais geram hashes diferentes

### ✅ Proteção contra Força Bruta
- Custo computacional alto (2^12 iterações)
- Cada tentativa demora ~100ms

## 📊 Exemplo Prático

### Mesma senha, hashes diferentes:

```bash
# Primeira execução
Senha: "admin" → Hash: $2b$12$ABC123.../xyz789
                        ↑ Salt diferente

# Segunda execução  
Senha: "admin" → Hash: $2b$12$DEF456.../uvw012
                        ↑ Salt diferente
```

### Verificação sempre funciona:

```python
# Ambos retornam True
bcrypt.checkpw("admin", "$2b$12$ABC123.../xyz789")  # True
bcrypt.checkpw("admin", "$2b$12$DEF456.../uvw012")  # True
```

## 🛠️ Ferramentas do Sistema

### `generate_admin_hash.py`
- Gera hash para nova senha
- Testa a verificação
- Fornece string para o .env

### `test_security.py`
- Valida implementação
- Testa verificação de hash
- Confirma importações

## 🚨 Boas Práticas

### ✅ Fazer
- Sempre usar hash para senhas
- Usar custo adequado (12+ para bcrypt)
- Validar entrada antes do hash
- Usar HTTPS em produção

### ❌ Evitar
- Senhas em texto plano
- MD5 ou SHA1 para senhas
- Salt fixo ou previsível
- Logs com senhas

## 🔄 Migração de Texto Plano para Hash

O sistema atual suporta ambos:

1. **Desenvolvimento**: Senha em texto plano (fallback)
2. **Produção**: Hash bcrypt (recomendado)

Para migrar:
```bash
python generate_admin_hash.py
# Adiciona ADMIN_PASSWORD_HASH ao .env
# Remove ADMIN_PASSWORD (opcional)
```

## 📈 Performance

- **Geração**: ~100ms (uma vez por alteração de senha)
- **Verificação**: ~100ms (a cada login)
- **Custo 12**: Bom equilíbrio segurança/performance
- **Escalabilidade**: Pode aumentar custo conforme hardware melhora

---

*Este documento explica a implementação de hash de senhas no Portal Empreendedor Unificado usando bcrypt para máxima segurança.*
## 🔄 
Autenticação via Banco de Dados

O sistema agora suporta autenticação através da tabela `authuser` do MySQL:

### Estrutura da tabela authuser:
```sql
- id: int (PK)
- login: varchar(50)
- senha: varchar(255)
```

### Fluxo de autenticação:
1. **Usuário faz login** → Sistema consulta tabela `authuser`
2. **Verifica formato da senha**:
   - Se começa com `$2b$` → Usa bcrypt para verificar
   - Caso contrário → Comparação direta (texto plano)
3. **Fallback para .env** → Se não encontrar no banco, tenta .env
4. **Sessão criada** → Armazena dados do usuário na sessão

### Vantagens:
- ✅ Múltiplos usuários administrativos
- ✅ Senhas centralizadas no banco
- ✅ Suporte a hash bcrypt e texto plano
- ✅ Fallback para configuração .env

### Scripts disponíveis:
- `scripts/inspect_authuser_table.py` - Inspeciona estrutura da tabela
- `scripts/check_passwords.py` - Verifica formato das senhas
- `scripts/test_auth_system.py` - Teste interativo de autenticação
- `scripts/test_known_credentials.py` - Teste com credenciais conhecidas