# Migração de Senhas para Hash bcrypt - Guia Completo

## 🎯 Objetivo

Converter senhas armazenadas em texto plano na tabela `authuser` para hash bcrypt seguro, eliminando a exposição de credenciais no banco de dados.

## ⚠️ Situação Anterior (INSEGURA)

```sql
-- Senhas em texto plano (PERIGOSO!)
SELECT login, senha FROM authuser;
+----------------------------------+----------+
| login                            | senha    |
+----------------------------------+----------+
| admin                            | admin123 |
| oportunidades.cariocas@prefeitura.rio | GPCE#2025# |
+----------------------------------+----------+
```

## ✅ Situação Atual (SEGURA)

```sql
-- Senhas em hash bcrypt (SEGURO!)
SELECT login, senha FROM authuser;
+----------------------------------+--------------------------------------------------------------+
| login                            | senha                                                        |
+----------------------------------+--------------------------------------------------------------+
| admin                            | $2b$12$aT530K4dhk6qiQZTohSQLu8YvK2J3mXzFqGH7wN9... |
| oportunidades.cariocas@prefeitura.rio | $2b$12$ZkcDCUlLH0IvdAM.dozgOOdR5K8mN2pLxQvH6... |
+----------------------------------+--------------------------------------------------------------+
```

## 🛠️ Scripts Disponíveis

### 1. 🚀 Migração Rápida (Recomendado)

**Script**: `scripts/quick_hash_migration.py`

```bash
python scripts/quick_hash_migration.py
```

**O que faz**:
- ✅ Migra automaticamente senhas conhecidas
- ✅ Mantém as credenciais funcionais
- ✅ Testa autenticação após migração
- ✅ Processo seguro e rápido

### 2. 🔧 Migração Interativa (Avançado)

**Script**: `scripts/migrate_passwords_to_hash.py`

```bash
python scripts/migrate_passwords_to_hash.py
```

**Funcionalidades**:
- 👀 Visualizar estado das senhas
- 🚀 Migração em lote
- 🔧 Atualização individual
- 🧪 Testes de autenticação

### 3. 🔍 Verificação de Status

**Script**: `scripts/check_passwords.py`

```bash
python scripts/check_passwords.py
```

**Mostra**:
- Formato atual das senhas (texto plano vs hash)
- Tamanho e tipo de cada senha
- Status de segurança

## 🔐 Como Funciona o Hash bcrypt

### Antes da Migração
```python
# Senha armazenada em texto plano
senha_banco = "admin123"

# Verificação insegura
if senha_digitada == senha_banco:
    login_ok = True
```

### Após a Migração
```python
# Senha armazenada como hash
senha_banco = "$2b$12$aT530K4dhk6qiQZTohSQLu8YvK2J3mXzFqGH7wN9..."

# Verificação segura
if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_banco.encode('utf-8')):
    login_ok = True
```

## 🛡️ Vantagens da Migração

### ✅ Segurança Aprimorada
- **Senhas irreversíveis**: Impossível recuperar senha original
- **Salt único**: Cada hash é diferente, mesmo para senhas iguais
- **Resistente a ataques**: Força bruta torna-se impraticável

### ✅ Conformidade
- **Boas práticas**: Padrão da indústria para armazenamento de senhas
- **LGPD/GDPR**: Proteção adequada de dados pessoais
- **Auditoria**: Demonstra cuidado com segurança

### ✅ Compatibilidade
- **Login mantido**: Usuários continuam usando as mesmas credenciais
- **Sistema híbrido**: Suporta hash e texto plano durante transição
- **Fallback seguro**: Migração gradual sem interrupção

## 📊 Processo de Migração Executado

### Passo 1: Verificação Inicial
```bash
$ python scripts/check_passwords.py

👤 Usuário: admin (ID: 1)
   Senha: admin123
   Formato: ⚠️  Texto plano (inseguro)

👤 Usuário: oportunidades.cariocas@prefeitura.rio (ID: 2)  
   Senha: GPCE#2025#
   Formato: ⚠️  Texto plano (inseguro)
```

### Passo 2: Migração Automática
```bash
$ python scripts/quick_hash_migration.py

🚀 Migração Rápida - Senhas para Hash bcrypt
============================================================
👥 Encontrados 2 usuários na tabela authuser

👤 Processando: admin
   🔄 Convertendo senha para hash...
   ✅ Hash gerado: $2b$12$aT530K4dhk6qi...
   ✅ Verificação: OK

👤 Processando: oportunidades.cariocas@prefeitura.rio
   🔄 Convertendo senha para hash...
   ✅ Hash gerado: $2b$12$ZkcDCUlLH0Ivd...
   ✅ Verificação: OK

📊 Resultado:
   ✅ Usuários migrados: 2
   📋 Total de usuários: 2

🎉 Migração concluída com sucesso!
```

### Passo 3: Verificação Final
```bash
$ python scripts/check_passwords.py

👤 Usuário: admin (ID: 1)
   Senha: $2b$12$aT530K4dhk6qi...
   Formato: ✅ Hash bcrypt

👤 Usuário: oportunidades.cariocas@prefeitura.rio (ID: 2)
   Senha: $2b$12$ZkcDCUlLH0Ivd...
   Formato: ✅ Hash bcrypt
```

### Passo 4: Teste de Autenticação
```bash
$ python scripts/test_known_credentials.py

🔍 Testando: admin
   ✅ Autenticação bem-sucedida!

🔍 Testando: oportunidades.cariocas@prefeitura.rio
   ✅ Autenticação bem-sucedida!
```

## 🔄 Adicionando Novos Usuários

### Com Hash (Recomendado)
```python
# Gerar hash para nova senha
import bcrypt
password = "nova_senha_123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

# Inserir no banco
INSERT INTO authuser (login, senha) VALUES ('novo_usuario', hashed.decode('utf-8'));
```

### Script Auxiliar
```bash
# Usar o gerador de hash
python scripts/generate_admin_hash.py
```

## 🚨 Troubleshooting

### Problema: Login não funciona após migração
**Causa**: Senha incorreta ou erro na migração
**Solução**:
```bash
# Verificar formato da senha
python scripts/check_passwords.py

# Testar autenticação
python scripts/test_known_credentials.py

# Resetar senha se necessário
python scripts/migrate_passwords_to_hash.py
# Escolha opção 3 (atualização individual)
```

### Problema: Erro "bcrypt not found"
**Causa**: Biblioteca não instalada
**Solução**:
```bash
pip install bcrypt
```

### Problema: Erro de conexão MySQL
**Causa**: Configurações incorretas no .env
**Solução**:
```bash
# Testar conexão
python scripts/test_db_connection.py

# Verificar .env
cat .env | grep DB_
```

## 📋 Checklist de Segurança

### ✅ Antes do Deploy
- [x] Todas as senhas migradas para hash bcrypt
- [x] Testes de autenticação passando
- [x] Backup do banco de dados criado
- [x] Scripts de migração testados
- [x] Documentação atualizada

### ✅ Após o Deploy
- [ ] Testar login em produção
- [ ] Monitorar logs de erro
- [ ] Verificar performance de autenticação
- [ ] Documentar credenciais de produção
- [ ] Configurar backup automático

## 🎯 Próximos Passos

### 1. Deploy Seguro
- Usar senhas em hash no PythonAnywhere
- Configurar .env de produção
- Testar autenticação em produção

### 2. Melhorias Futuras
- Interface web para gerenciar usuários
- Política de senhas (complexidade, expiração)
- Log de tentativas de login
- Autenticação de dois fatores (2FA)

### 3. Monitoramento
- Alertas para tentativas de login falhadas
- Relatórios de acesso
- Backup automático de usuários

---

**✅ Migração concluída com sucesso! O sistema agora armazena senhas de forma segura usando hash bcrypt, eliminando a exposição de credenciais em texto plano.**