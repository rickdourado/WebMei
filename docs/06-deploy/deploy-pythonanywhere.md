# Deploy no PythonAnywhere - Guia Completo

## 📋 Visão Geral

O PythonAnywhere é uma plataforma de hospedagem Python que oferece MySQL gratuito e suporte completo ao Flask. Este guia detalha como migrar o Portal Empreendedor Unificado para lá.

## 🎯 Pré-requisitos

### Conta PythonAnywhere
- ✅ Conta gratuita ou paga no [PythonAnywhere](https://www.pythonanywhere.com)
- ✅ Acesso ao dashboard e console
- ✅ Banco MySQL disponível (incluído no plano gratuito)

### Dados Locais
- ✅ Código fonte do projeto
- ✅ Dados da tabela `authuser` (usuários)
- ✅ Arquivos CSV existentes (se houver)

## 🚀 Processo de Migração

### 1. Preparação Local

#### 1.1 Exportar dados do MySQL local
```bash
# Exportar estrutura e dados da tabela authuser
mysqldump -u root -p servicosmei authuser > authuser_backup.sql

# Ou exportar apenas os dados
mysqldump -u root -p --no-create-info servicosmei authuser > authuser_data.sql
```

#### 1.2 Criar arquivo de requirements
```bash
# Gerar requirements.txt atualizado
pip freeze > requirements.txt
```

#### 1.3 Preparar arquivos de configuração
```bash
# Criar .env para produção (sem senhas reais)
cp .env .env.production.example
```

### 2. Configuração no PythonAnywhere

#### 2.1 Upload do código
```bash
# Opção 1: Via Git (recomendado)
git clone https://github.com/seu-usuario/portal-empreendedor.git

# Opção 2: Via upload de arquivos
# Use o file manager do PythonAnywhere
```

#### 2.2 Configurar ambiente virtual
```bash
# No console do PythonAnywhere
mkvirtualenv --python=/usr/bin/python3.10 portal-empreendedor

# Ativar ambiente
workon portal-empreendedor

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração do MySQL

#### 3.1 Acessar MySQL no PythonAnywhere
```bash
# No console do PythonAnywhere
mysql -u seu_usuario -p'sua_senha' seu_usuario$servicosmei
```

#### 3.2 Criar estrutura do banco
```sql
-- Criar tabela authuser
CREATE TABLE authuser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserir usuários (com senhas em hash)
INSERT INTO authuser (login, senha) VALUES 
('admin', '$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i'),
('oportunidades.cariocas@prefeitura.rio', 'GPCE#2025#');
```

#### 3.3 Importar dados existentes
```bash
# Se você tem backup local
mysql -u seu_usuario -p'sua_senha' seu_usuario$servicosmei < authuser_backup.sql
```

### 4. Configuração da Aplicação

#### 4.1 Arquivo .env para produção
```bash
# No PythonAnywhere, criar /home/seu_usuario/portal-empreendedor/.env
SECRET_KEY=sua_chave_secreta_super_forte_aqui
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_PASSWORD_HASH=$2b$12$N6t8R6Fl5hhEAD7Sw6EgEu/yRx27sj366qnXeElwePcgP6uWRFN3i

# Configurações MySQL do PythonAnywhere
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
DB_NAME=seu_usuario$servicosmei
DB_USER=seu_usuario
DB_PASSWORD=sua_senha_mysql
DB_CHARSET=utf8mb4
```

#### 4.2 Configurar WSGI
```python
# /var/www/seu_usuario_pythonanywhere_com_wsgi.py

import sys
import os

# Adicionar o diretório do projeto ao path
project_home = '/home/seu_usuario/portal-empreendedor'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar variáveis de ambiente
os.environ['FLASK_ENV'] = 'production'

# Importar a aplicação
from app import app as application

if __name__ == "__main__":
    application.run()
```

### 5. Configuração Web

#### 5.1 Configurar Web App no Dashboard
1. **Acesse** "Web" no dashboard
2. **Clique** "Add a new web app"
3. **Escolha** "Manual configuration"
4. **Selecione** Python 3.10
5. **Configure** o WSGI file path

#### 5.2 Configurações importantes
```
Source code: /home/seu_usuario/portal-empreendedor
Working directory: /home/seu_usuario/portal-empreendedor
WSGI configuration file: /var/www/seu_usuario_pythonanywhere_com_wsgi.py
Virtualenv: /home/seu_usuario/.virtualenvs/portal-empreendedor
```

#### 5.3 Arquivos estáticos
```
URL: /static/
Directory: /home/seu_usuario/portal-empreendedor/static/
```

### 6. Testes e Validação

#### 6.1 Testar conexão com banco
```bash
# No console do PythonAnywhere
cd /home/seu_usuario/portal-empreendedor
python scripts/test_db_connection.py
```

#### 6.2 Testar autenticação
```bash
python scripts/test_known_credentials.py
```

#### 6.3 Testar aplicação web
- Acesse: `https://seu_usuario.pythonanywhere.com`
- Teste login: `https://seu_usuario.pythonanywhere.com/admin/login`

## 🔧 Configurações Específicas

### Diferenças do Ambiente Local

#### Paths e Diretórios
```python
# Local
CSV_DIR = os.path.join(BASE_DIR, 'CSV')

# PythonAnywhere (mesmo código funciona)
CSV_DIR = os.path.join(BASE_DIR, 'CSV')
```

#### Configurações de Banco
```python
# Local
DB_HOST = 'localhost'

# PythonAnywhere
DB_HOST = 'seu_usuario.mysql.pythonanywhere-services.com'
```

### Logs e Debug
```python
# Para produção, desabilitar debug
if __name__ == '__main__':
    app.run(debug=False)  # Importante!
```

## 🛡️ Segurança em Produção

### Variáveis de Ambiente
- ✅ Usar senhas fortes e únicas
- ✅ Não commitar .env no Git
- ✅ Usar HTTPS (automático no PythonAnywhere)

### Banco de Dados
- ✅ Migrar senhas para hash bcrypt
- ✅ Usar usuário MySQL específico
- ✅ Backup regular dos dados

### Aplicação
- ✅ DEBUG=False em produção
- ✅ SECRET_KEY forte e única
- ✅ CSRF protection ativo

## 📊 Monitoramento

### Logs de Erro
```bash
# Acessar logs no PythonAnywhere
tail -f /var/log/seu_usuario.pythonanywhere.com.error.log
```

### Logs de Acesso
```bash
tail -f /var/log/seu_usuario.pythonanywhere.com.access.log
```

### Performance
- Monitor CPU/RAM no dashboard
- Otimizar queries MySQL se necessário

## 🔄 Manutenção

### Atualizações de Código
```bash
# Via Git
cd /home/seu_usuario/portal-empreendedor
git pull origin main

# Reiniciar aplicação
# Clique "Reload" no dashboard Web
```

### Backup de Dados
```bash
# Backup automático semanal
mysqldump -u seu_usuario -p'sua_senha' seu_usuario$servicosmei > backup_$(date +%Y%m%d).sql
```

### Atualizações de Dependências
```bash
workon portal-empreendedor
pip install -r requirements.txt --upgrade
```

## 🚨 Troubleshooting

### Problemas Comuns

#### Erro de Importação
```
ImportError: No module named 'flask'
```
**Solução**: Verificar se o virtualenv está configurado corretamente

#### Erro de Conexão MySQL
```
Access denied for user
```
**Solução**: Verificar credenciais no .env e permissões MySQL

#### Erro 500 Internal Server Error
**Solução**: Verificar logs de erro e configuração WSGI

#### CSRF Token Missing
**Solução**: Verificar se todos os templates têm tokens CSRF

### Comandos Úteis
```bash
# Reiniciar aplicação
# Dashboard > Web > Reload

# Ver logs em tempo real
tail -f /var/log/seu_usuario.pythonanywhere.com.error.log

# Testar configuração
python -c "from app import app; print('OK')"

# Verificar variáveis de ambiente
python -c "import os; print(os.getenv('DB_HOST'))"
```

## 📞 Suporte

### Recursos PythonAnywhere
- [Documentação oficial](https://help.pythonanywhere.com/)
- [Fórum de suporte](https://www.pythonanywhere.com/forums/)
- [Guias Flask](https://help.pythonanywhere.com/pages/Flask/)

### Recursos do Projeto
- Scripts de teste em `scripts/`
- Documentação em `docs/`
- Configurações em `.kiro/steering/`

---

**✅ Com este guia, você conseguirá migrar completamente o Portal Empreendedor Unificado para o PythonAnywhere, mantendo todas as funcionalidades e melhorando a segurança e disponibilidade do sistema.**