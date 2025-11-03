# Portal Empreendedor Unificado

Sistema web Flask para cadastro e gerenciamento de oportunidades de serviços para empreendedores MEI (Microempreendedor Individual).

## 🎯 Visão Geral

O Portal Empreendedor Unificado permite que órgãos demandantes cadastrem serviços/vagas e que empreendedores visualizem essas oportunidades publicamente. O sistema oferece uma interface administrativa para gerenciamento das oportunidades cadastradas.

## ✨ Funcionalidades

### 🌐 Área Pública
- **Cadastro de Serviços**: Formulário completo para órgãos demandantes
- **Listagem de Vagas**: Visualização pública das oportunidades
- **Detalhes da Vaga**: Visualização completa de cada oportunidade
- **Download CSV**: Exportação dos dados cadastrados

### 🔐 Área Administrativa
- **Login Seguro**: Autenticação via banco de dados MySQL
- **Dashboard**: Listagem e gerenciamento de vagas
- **Exclusão de Vagas**: Remoção segura de oportunidades
- **Múltiplos Usuários**: Suporte a vários administradores

## 🛠️ Tecnologias

- **Backend**: Flask (Python 3.10+)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: MySQL
- **Segurança**: bcrypt, Flask-WTF (CSRF Protection)
- **Templates**: Jinja2
- **Estilo**: CSS customizado com design responsivo

## 📋 Estrutura de Dados

### Campos do Formulário de Serviços
- Órgão Demandante (obrigatório)
- Título do serviço (obrigatório)
- Tipo de atividade (dropdown)
- Especificação da Atividade (obrigatório, dropdown)
- Descrição do Serviço (obrigatório)
- Outras informações (opcional)
- Endereço completo (obrigatório)
- Forma de pagamento (Cheque, Dinheiro, Cartão, Transferência)
- Prazos de pagamento e execução (obrigatórios)

### Tabela de Usuários (authuser)
```sql
CREATE TABLE authuser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.10+
- MySQL 8.0+
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd portal-empreendedor
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o banco de dados
```bash
# Crie o banco de dados
mysql -u root -p
CREATE DATABASE servicosmei CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Crie a tabela de usuários
CREATE TABLE authuser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas configurações
nano .env
```

**Exemplo de .env:**
```env
# Configurações Flask
SECRET_KEY=sua_chave_secreta_super_forte
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Configurações MySQL
DB_HOST=localhost
DB_PORT=3306
DB_NAME=servicosmei
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_CHARSET=utf8mb4
```

### 5. Teste a conexão
```bash
python scripts/test_db_connection.py
```

### 6. Configure usuários administrativos
```bash
# Inserir usuário inicial
INSERT INTO authuser (login, senha) VALUES ('admin', 'admin123');

# Migrar senhas para hash bcrypt (recomendado)
python scripts/quick_hash_migration.py
```

### 7. Inicie o servidor
```bash
python app.py
# ou
python scripts/start_server.py
```

Acesse: http://localhost:5010

## 🔐 Segurança

### Implementações de Segurança
- ✅ **Hash bcrypt** para senhas de usuários
- ✅ **Proteção CSRF** em todos os formulários
- ✅ **Validação de entrada** em campos obrigatórios
- ✅ **Sessões seguras** com Flask
- ✅ **Sanitização de dados** para nomes de arquivos

### Credenciais Padrão
- **Usuário**: admin
- **Senha**: admin123

⚠️ **IMPORTANTE**: Altere as credenciais padrão em produção!

## 📁 Estrutura do Projeto

```
portal-empreendedor/
├── app.py                 # Aplicação Flask principal
├── database.py            # Gerenciador de banco de dados
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Este arquivo
├── templates/            # Templates HTML
│   ├── index.html        # Formulário de cadastro
│   ├── admin_login.html  # Login administrativo
│   ├── admin_dashboard.html # Dashboard admin
│   ├── vagas_public.html # Listagem pública
│   └── vaga_view.html    # Visualização de vaga
├── static/               # Arquivos estáticos
│   ├── css/             # Estilos CSS
│   ├── js/              # JavaScript
│   └── images/          # Imagens
├── CSV/                  # Arquivos CSV gerados
├── scripts/              # Scripts utilitários
│   ├── README.md        # Documentação dos scripts
│   ├── test_db_connection.py
│   ├── quick_hash_migration.py
│   └── ...
└── docs/                 # Documentação técnica
    ├── hash-senhas-explicacao.md
    ├── deploy-pythonanywhere.md
    └── ...
```

## 🛠️ Scripts Utilitários

### Testes e Validação
```bash
# Testar conexão com banco
python scripts/test_db_connection.py

# Testar autenticação
python scripts/test_known_credentials.py

# Validar segurança
python scripts/test_security.py
```

### Migração de Senhas
```bash
# Migração rápida (senhas conhecidas)
python scripts/quick_hash_migration.py

# Migração interativa
python scripts/migrate_passwords_to_hash.py
```

### Preparação para Deploy
```bash
# Preparar migração para PythonAnywhere
python scripts/prepare_migration.py
```

## 🌐 Deploy

### PythonAnywhere
Consulte o guia completo: [`docs/deploy-pythonanywhere.md`](docs/deploy-pythonanywhere.md)

### Configurações de Produção
- Desabilitar DEBUG
- Usar HTTPS
- Configurar backup automático
- Monitorar logs de acesso

## 📚 Documentação

- [`docs/hash-senhas-explicacao.md`](docs/hash-senhas-explicacao.md) - Sistema de hash bcrypt
- [`docs/deploy-pythonanywhere.md`](docs/deploy-pythonanywhere.md) - Guia de deploy
- [`docs/migracao-senhas-hash.md`](docs/migracao-senhas-hash.md) - Migração de senhas
- [`scripts/README.md`](scripts/README.md) - Documentação dos scripts

## 🤝 Contribuição

### Padrões de Desenvolvimento
- Usar mensagens de commit em português
- Prefixos: `feat:`, `fix:`, `docs:`, `refactor:`
- Validar formulários client-side e server-side
- Sempre usar hash bcrypt para senhas
- Implementar testes para funcionalidades críticas

### Fluxo de Desenvolvimento
1. Criar branch para feature
2. Implementar funcionalidade
3. Testar com scripts utilitários
4. Documentar mudanças
5. Fazer commit seguindo padrões
6. Criar pull request

## 📞 Suporte

### Problemas Comuns
- **Erro CSRF**: Verificar tokens nos templates
- **Erro MySQL**: Validar configurações no .env
- **Login falha**: Verificar hash das senhas

### Logs e Debug
```bash
# Logs de erro (desenvolvimento)
tail -f logs/error.log

# Debug de autenticação
python scripts/test_auth_system.py
```

## 📄 Licença

Este projeto está sob licença MIT. Consulte o arquivo LICENSE para mais detalhes.

## 🏷️ Versão

**v1.0.0** - Sistema completo com autenticação MySQL e segurança bcrypt

---

**Desenvolvido para facilitar a conexão entre órgãos demandantes e empreendedores MEI, promovendo oportunidades de negócio e desenvolvimento econômico local.**