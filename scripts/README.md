# Scripts Utilitários - Portal Empreendedor

Esta pasta contém scripts auxiliares para desenvolvimento, testes e manutenção do sistema.

## 📋 Scripts Disponíveis

### 🔌 `test_db_connection.py`
**Função**: Testa a conexão com o banco de dados MySQL

**Uso**:
```bash
python scripts/test_db_connection.py
```

**O que faz**:
- Verifica conectividade com MySQL
- Mostra versão do banco
- Lista tabelas existentes
- Valida configurações do .env

---

### 🔐 `generate_admin_hash.py`
**Função**: Gera hash bcrypt para senha do administrador

**Uso**:
```bash
python scripts/generate_admin_hash.py
```

**O que faz**:
- Lê senha atual do .env ou solicita nova
- Gera hash bcrypt seguro
- Testa a verificação do hash
- Fornece string para adicionar ao .env

**Exemplo de saída**:
```
Hash: $2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i
Adicione ao .env: ADMIN_PASSWORD_HASH=...
```

---

### 🛡️ `test_security.py`
**Função**: Valida implementações de segurança do sistema

**Uso**:
```bash
python scripts/test_security.py
```

**O que faz**:
- Testa verificação de hash de senhas
- Valida importações de segurança
- Confirma configurações do .env
- Relatório de status das implementações

---

### 🔐 `migrate_passwords_to_hash.py`
**Função**: Migra senhas da tabela authuser de texto plano para hash bcrypt (interativo)

**Uso**:
```bash
python scripts/migrate_passwords_to_hash.py
```

**O que faz**:
- Menu interativo com múltiplas opções
- Visualiza estado atual das senhas
- Migra todas as senhas automaticamente
- Atualiza senhas individuais
- Testa autenticação após migração

**Funcionalidades**:
- Migração em lote segura
- Atualização individual de usuários
- Verificação de integridade
- Testes de autenticação

---

### ⚡ `quick_hash_migration.py`
**Função**: Migração rápida de senhas conhecidas para hash bcrypt

**Uso**:
```bash
python scripts/quick_hash_migration.py
```

**O que faz**:
- Migra automaticamente senhas conhecidas
- Converte admin/admin123 e oportunidades.cariocas@prefeitura.rio/GPCE#2025#
- Testa autenticação após migração
- Processo rápido e seguro

**Ideal para**:
- Primeira migração do sistema
- Conversão rápida de senhas conhecidas
- Preparação para produção

---

### 🚀 `prepare_migration.py`
**Função**: Prepara dados e arquivos para migração ao PythonAnywhere

**Uso**:
```bash
python scripts/prepare_migration.py
```

**O que faz**:
- Exporta dados da tabela authuser (mysqldump)
- Cria arquivo .env para produção
- Gera arquivo WSGI configurado
- Lista arquivos CSV existentes
- Fornece resumo da migração

**Arquivos gerados**:
- `migration/authuser_backup_*.sql`
- `migration/.env.production`
- `migration/wsgi.py`

---

## 🚀 Como Usar

### Primeira configuração:
```bash
# 1. Teste a conexão com banco
python scripts/test_db_connection.py

# 2. Gere hash da senha admin
python scripts/generate_admin_hash.py

# 3. Valide as implementações
python scripts/test_security.py
```

### Manutenção:
```bash
# Alterar senha do admin
python scripts/generate_admin_hash.py

# Verificar segurança após mudanças
python scripts/test_security.py
```

## 📁 Estrutura

```
scripts/
├── README.md                 # Este arquivo
├── test_db_connection.py     # Teste de conexão MySQL
├── generate_admin_hash.py    # Gerador de hash de senhas
└── test_security.py          # Validador de segurança
```

## 🔧 Dependências

Os scripts utilizam as mesmas dependências do projeto principal:
- `python-dotenv` - Carregamento de variáveis .env
- `PyMySQL` - Conexão com MySQL
- `bcrypt` - Hash de senhas
- `Flask-WTF` - Validação de segurança

## 📝 Notas

- Todos os scripts carregam configurações do arquivo `.env`
- Scripts são independentes e podem ser executados isoladamente
- Sempre execute a partir da raiz do projeto para manter paths corretos
- Em caso de erro, verifique se as dependências estão instaladas