# Portal Empreendedor Unificado - Diretrizes de Desenvolvimento

## Visão Geral do Projeto
Este é um sistema web Flask para cadastro e gerenciamento de oportunidades de serviços para empreendedores. O sistema permite que órgãos demandantes cadastrem serviços/vagas e que empreendedores visualizem essas oportunidades publicamente.

**SEMPRE** utilize o Ambiente de desenvolvimento : usando o comando conda activate ciclo, a cada prompt.
**SEMPRE** Armazene scripts na pasta scripts

## Arquitetura e Tecnologias
- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS/JavaScript com templates Jinja2
- **Armazenamento**: Arquivos CSV (sem banco de dados)
- **Autenticação**: Sessões Flask simples para área administrativa

## Estrutura de Dados
Os serviços são armazenados em arquivos CSV individuais na pasta `CSV/` com os seguintes campos:
- `orgao_demandante` (obrigatório)
- `titulo_servico` (obrigatório)
- `tipo_atividade` (dropdown)
- `especificacao_atividade` (obrigatório, dropdown)
- `descricao_servico` (obrigatório)
- `outras_informacoes` (opcional)
- `endereco` (obrigatório)
- `numero` (obrigatório, numérico)
- `bairro` (obrigatório)
- `forma_pagamento` (obrigatório, dropdown: Cheque, Dinheiro, Cartão, Transferência)
- `prazo_pagamento` (obrigatório)
- `prazo_expiracao` (obrigatório, formato DD/MM/AAAA)
- `data_limite_execucao` (obrigatório, formato YYYY-MM-DD)

## Padrões de Desenvolvimento

### Validação de Dados
- Sempre validar campos obrigatórios antes de salvar
- Validar formato de datas e números
- Usar flash messages para feedback ao usuário
- Sanitizar entrada de dados para evitar problemas de segurança

### Nomenclatura de Arquivos
- CSVs são nomeados como: `{slug_do_titulo}_{timestamp}.csv`
- Usar função `safe_slug()` para gerar nomes seguros
- Timestamp no formato: `YYYYMMDD_HHMMSS`

### Tratamento de Erros
- Sempre usar try/except ao ler arquivos CSV
- Fornecer valores padrão quando dados não estão disponíveis
- Logs de erro devem ser informativos mas não expor dados sensíveis

### Interface do Usuário
- Usar Bootstrap ou CSS similar para responsividade
- Flash messages para feedback (success, error, warning, info)
- Formulários devem ter validação client-side e server-side
- Dropdowns devem ser populados dinamicamente quando possível

### Segurança
- Usar variáveis de ambiente para credenciais (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD)
- Validar e sanitizar todas as entradas do usuário
- Implementar decorador `@login_required` para rotas administrativas
- Não expor informações sensíveis em logs ou mensagens de erro

### Organização de Código
- Separar lógica de negócio em funções auxiliares
- Manter rotas simples e focadas
- Usar nomes descritivos para variáveis e funções
- Comentar código complexo ou não óbvio

## Funcionalidades Principais

### Área Pública
- `/` - Formulário de cadastro de serviços
- `/vagas` - Listagem pública de vagas
- `/vaga/<filename>` - Visualização detalhada de vaga
- `/download/<filename>` - Download de CSV

### Área Administrativa
- `/admin/login` - Login administrativo
- `/admin` - Dashboard com listagem de vagas
- `/admin/delete/<filename>` - Exclusão de vagas
- `/admin/logout` - Logout

## Referências de Dados
- `refs/ServicosConsolidados.csv` - Fonte de dados para ocupações e serviços
- `refs/PortalEmpreendedorUnificado.csv` - Dados de referência do portal
- `refs/Campos` - Especificação dos campos do formulário

## Convenções de Commit
- Use mensagens em português
- Prefixos: `feat:`, `fix:`, `refactor:`, `docs:`
- Seja descritivo sobre as mudanças realizadas

## Testes e Qualidade
- Testar funcionalidades críticas manualmente
- Validar formulários com dados válidos e inválidos
- Verificar comportamento em diferentes navegadores
- Testar fluxo completo: cadastro → visualização → administração