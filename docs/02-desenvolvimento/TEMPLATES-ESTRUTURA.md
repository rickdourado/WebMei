# Estrutura dos Templates - Portal Empreendedor

## Visão Geral

O sistema utiliza templates Jinja2 para renderizar as páginas HTML. Todos os templates estão na pasta `templates/`.

## Templates Disponíveis

### 1. index.html
**Rota:** `GET /`  
**Descrição:** Formulário de cadastro de novos serviços/vagas

**Dados recebidos:**
- `today_iso` - Data atual no formato YYYY-MM-DD
- `orgaos_opcoes` - Lista de órgãos demandantes
- `tipo_atividade_opcoes` - Lista de tipos de atividade (ocupações)
- `especificacao_atividade_opcoes` - Lista inicial de especificações
- `forma_pagamento_opcoes` - Lista de formas de pagamento
- `ocupacao_to_servicos` - Mapeamento de ocupações para serviços

**Campos do formulário:**
- Órgão Demandante (dropdown)
- Título do Serviço (texto)
- Tipo de Atividade (dropdown dinâmico)
- Especificação da Atividade (dropdown dinâmico)
- Descrição do Serviço (textarea)
- Outras Informações (textarea, opcional)
- Endereço (texto)
- Número (texto)
- Bairro (texto)
- Forma de Pagamento (dropdown)
- Prazo de Pagamento (texto)
- Prazo de Expiração (data)
- Data Limite de Execução (data)

---

### 2. service_success.html
**Rota:** Renderizado após `POST /create_service`  
**Descrição:** Página de confirmação após cadastro bem-sucedido

**Dados recebidos:**
- `data` - Dicionário com todos os dados do serviço cadastrado
- `service_id` - ID do serviço no banco de dados

**Ações disponíveis:**
- Baixar CSV do serviço
- Ver todas as vagas
- Cadastrar outro serviço

---

### 3. vagas_public.html
**Rota:** `GET /vagas`  
**Descrição:** Listagem pública de todas as vagas cadastradas

**Dados recebidos:**
- `vagas` - Lista de dicionários com dados das vagas

**Estrutura da listagem:**
```
Título | Tipo | Bairro | Ações
```

**Ações por vaga:**
- Ver detalhes
- Baixar CSV

**Campos exibidos de cada vaga:**
- `id` - ID do serviço (usado nas URLs)
- `titulo_servico` - Título da vaga
- `tipo_atividade` - Tipo de atividade
- `bairro` - Bairro onde será executado

---

### 4. vaga_view.html
**Rota:** `GET /vaga/<servico_id>`  
**Descrição:** Visualização detalhada de uma vaga específica

**Dados recebidos:**
- `data` - Dicionário com todos os dados da vaga
- `servico_id` - ID do serviço

**Campos exibidos:**
- Órgão Demandante
- Tipo de atividade
- Especificação da Atividade
- Descrição do Serviço
- Outras informações (ou "—" se vazio)
- Endereço completo (rua, número, bairro)
- Forma de pagamento
- Prazo de pagamento
- Prazo de expiração
- Data limite de execução

**Ações disponíveis:**
- Baixar CSV
- Voltar para listagem

---

### 5. admin_login.html
**Rota:** `GET /admin/login`  
**Descrição:** Página de login administrativo

**Campos:**
- Username
- Password

**Ação:** `POST /admin/login`

---

### 6. admin_dashboard.html
**Rota:** `GET /admin` (requer autenticação)  
**Descrição:** Painel administrativo com listagem de vagas

**Dados recebidos:**
- `vagas` - Lista de dicionários com dados das vagas
- `total` - Total de vagas cadastradas

**Estrutura da listagem:**
```
Título | Tipo | Bairro | Ações
```

**Ações por vaga:**
- Ver detalhes
- Baixar CSV
- Excluir (com confirmação)

---

## Estrutura de Dados das Vagas

Todos os templates que exibem vagas recebem dicionários com a seguinte estrutura:

```python
{
    'id': int,                          # ID único no banco
    'orgao_demandante': str,            # Nome do órgão
    'titulo_servico': str,              # Título da vaga
    'tipo_atividade': str,              # Tipo de atividade/ocupação
    'especificacao_atividade': str,     # Especificação detalhada
    'descricao_servico': str,           # Descrição completa
    'outras_informacoes': str,          # Informações adicionais (opcional)
    'endereco': str,                    # Endereço
    'numero': str,                      # Número do endereço
    'bairro': str,                      # Bairro
    'forma_pagamento': str,             # Forma de pagamento
    'prazo_pagamento': str,             # Prazo de pagamento
    'prazo_expiracao': date,            # Data de expiração
    'data_limite_execucao': date,       # Data limite para execução
    'data_criacao': timestamp           # Data de cadastro
}
```

## URLs e Parâmetros

### URLs que usam servico_id:
- `/vaga/<servico_id>` - Visualizar vaga
- `/download/<servico_id>` - Baixar CSV
- `/admin/delete/<servico_id>` - Excluir vaga (POST)

### Exemplo de uso no template:
```jinja2
<a href="{{ url_for('vaga_view', servico_id=v.id) }}">Ver</a>
<a href="{{ url_for('download_file', servico_id=v.id) }}">CSV</a>
```

## Componentes Comuns

### Header
Todos os templates incluem um header com:
- Logo do Ciclo Carioca
- Título da página
- Navegação (Home, Vagas, Admin/Sair)

### Flash Messages
Sistema de mensagens flash para feedback:
- `success` - Verde (operação bem-sucedida)
- `error` - Vermelho (erro)
- `warning` - Amarelo (aviso)
- `info` - Azul (informação)

### Estilos
- CSS principal: `/static/css/style.css`
- Fonte: Inter (Google Fonts)
- Ícones: Font Awesome 6.0.0

## Migração CSV → Banco de Dados

### Antes (CSV):
```jinja2
url_for('vaga_view', filename=v.arquivo)
url_for('download_file', filename=v.arquivo)
```

### Depois (MySQL):
```jinja2
url_for('vaga_view', servico_id=v.id)
url_for('download_file', servico_id=v.id)
```

## Validação e Segurança

- CSRF Protection habilitado em todos os formulários
- Campos obrigatórios validados no backend
- Sanitização de entrada de dados
- Sessões Flask para autenticação admin
- Decorador `@login_required` para rotas administrativas
