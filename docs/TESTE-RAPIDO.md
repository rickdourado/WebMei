# 🧪 Teste Rápido - Portal Empreendedor React

## Checklist de Testes

### ✅ Preparação

```bash
# 1. Ativar ambiente
conda activate ciclo

# 2. Verificar dependências backend
cd backend
pip install -r requirements.txt

# 3. Verificar dependências frontend
cd ../frontend
npm install

# 4. Voltar para raiz
cd ..
```

### 🚀 Iniciar Aplicação

```bash
# Opção 1: Script automático
./scripts/start-react-dev.sh

# Opção 2: Manual (2 terminais)
# Terminal 1:
cd backend && python api.py

# Terminal 2:
cd frontend && npm run dev
```

### 📋 Testes Funcionais

#### 1. Teste de Configuração Inicial

**URL**: http://localhost:5173

**Verificar**:
- [ ] Página carrega sem erros
- [ ] Título "Portal Empreendedor Unificado" aparece
- [ ] Formulário está visível
- [ ] Dropdowns estão populados

**Console do navegador**:
```
Não deve ter erros em vermelho
```

#### 2. Teste de Cadastro de Serviço

**Passos**:
1. Preencher todos os campos obrigatórios:
   - Órgão Demandante: `Prefeitura Municipal`
   - Título: `Teste Pintor Residencial`
   - Tipo de Atividade: Selecionar qualquer
   - Especificação: Selecionar qualquer
   - Descrição: `Serviço de pintura para teste`
   - Endereço: `Rua Teste`
   - Número: `123`
   - Bairro: `Centro`
   - Forma de Pagamento: `Dinheiro`
   - Prazo de Pagamento: `30 dias`
   - Prazo de Expiração: Data futura
   - Data Limite: Data futura

2. Clicar em "Cadastrar Serviço"

**Resultado Esperado**:
- [ ] Mensagem de sucesso aparece
- [ ] Redirecionamento para /vagas após 2 segundos
- [ ] Novo serviço aparece na listagem

**Backend (Terminal)**:
```
✓ Serviço inserido no banco de dados com ID: X
```

**Arquivo CSV criado**:
```bash
ls backend/CSV/
# Deve ter: Teste_Pintor_Residencial_YYYYMMDD_HHMMSS.csv
```

#### 3. Teste de Listagem de Vagas

**URL**: http://localhost:5173/vagas

**Verificar**:
- [ ] Lista de vagas aparece
- [ ] Cards mostram informações corretas
- [ ] Botão "Ver Detalhes" funciona
- [ ] Navegação para detalhes funciona

#### 4. Teste de Detalhes da Vaga

**Passos**:
1. Clicar em "Ver Detalhes" de qualquer vaga

**Verificar**:
- [ ] Todas as informações aparecem
- [ ] Botão "Baixar CSV" funciona
- [ ] Download do CSV acontece
- [ ] Botão "Voltar" funciona

#### 5. Teste de Login Admin

**URL**: http://localhost:5173/admin/login

**Credenciais**:
- Usuário: `admin`
- Senha: `admin`

**Verificar**:
- [ ] Login com credenciais corretas funciona
- [ ] Mensagem de sucesso aparece
- [ ] Redirecionamento para /admin
- [ ] Login com credenciais erradas falha
- [ ] Mensagem de erro aparece

#### 6. Teste de Dashboard Admin

**URL**: http://localhost:5173/admin (após login)

**Verificar**:
- [ ] Tabela de vagas aparece
- [ ] Nome do usuário aparece no header
- [ ] Botão "Ver" funciona
- [ ] Botão "Excluir" funciona
- [ ] Confirmação de exclusão aparece
- [ ] Vaga é removida após confirmação
- [ ] Botão "Sair" funciona

#### 7. Teste de Proteção de Rotas

**Passos**:
1. Fazer logout
2. Tentar acessar: http://localhost:5173/admin

**Resultado Esperado**:
- [ ] Redirecionamento para /admin/login
- [ ] Mensagem pedindo login

#### 8. Teste de API Direta

**Teste 1: Listar Serviços**
```bash
curl http://localhost:5010/api/servicos
```
**Esperado**: JSON array com serviços

**Teste 2: Configurações**
```bash
curl http://localhost:5010/api/config
```
**Esperado**: JSON com órgãos, tipos, etc

**Teste 3: Criar Serviço**
```bash
curl -X POST http://localhost:5010/api/servicos \
  -H "Content-Type: application/json" \
  -d '{
    "orgao_demandante": "Teste API",
    "titulo_servico": "Teste via CURL",
    "especificacao_atividade": "Teste",
    "descricao_servico": "Teste",
    "endereco": "Rua Teste",
    "numero": "1",
    "bairro": "Centro",
    "forma_pagamento": "Dinheiro",
    "prazo_pagamento": "30 dias",
    "prazo_expiracao": "2024-12-31",
    "data_limite_execucao": "2024-12-31"
  }'
```
**Esperado**: JSON com sucesso

### 🐛 Testes de Erro

#### 1. Validação de Campos Obrigatórios

**Passos**:
1. Tentar cadastrar serviço sem preencher campos
2. Clicar em "Cadastrar"

**Esperado**:
- [ ] Navegador mostra validação HTML5
- [ ] Formulário não é enviado

#### 2. Validação de Número

**Passos**:
1. Preencher campo "Número" com: `ABC123`
2. Tentar cadastrar

**Esperado**:
- [ ] Erro de validação
- [ ] Mensagem explicativa

**Valores válidos para testar**:
- `123` ✅
- `S/N` ✅
- `SN` ✅
- `ABC` ❌

#### 3. Teste de CORS

**Abrir console do navegador**:
```javascript
fetch('http://localhost:5010/api/config')
  .then(r => r.json())
  .then(console.log)
```

**Esperado**:
- [ ] Sem erro de CORS
- [ ] Dados retornados

### 📊 Testes de Performance

#### 1. Tempo de Carregamento

**Ferramentas**: DevTools → Network

**Verificar**:
- [ ] Primeira carga < 2s
- [ ] Navegação entre páginas < 500ms
- [ ] API responses < 200ms

#### 2. Tamanho dos Arquivos

**Verificar**:
- [ ] Bundle JS < 500KB
- [ ] CSS < 50KB
- [ ] Imagens otimizadas

### 🔒 Testes de Segurança

#### 1. Proteção de Rotas Admin

**Sem login, tentar**:
```bash
curl -X DELETE http://localhost:5010/api/admin/servicos/teste.csv
```

**Esperado**:
- [ ] Status 401 Unauthorized

#### 2. Validação de Entrada

**Tentar injeção SQL/XSS**:
- Título: `<script>alert('xss')</script>`
- Descrição: `'; DROP TABLE servicos; --`

**Esperado**:
- [ ] Dados são sanitizados
- [ ] Sem execução de código

### 📱 Testes de Responsividade

**Testar em**:
- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

**DevTools → Toggle Device Toolbar**

**Verificar**:
- [ ] Layout se adapta
- [ ] Formulário usável
- [ ] Tabelas scrollam horizontalmente
- [ ] Botões acessíveis

### 🌐 Testes de Navegadores

**Testar em**:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (se disponível)
- [ ] Edge

### 📝 Checklist Final

#### Backend
- [ ] API responde em http://localhost:5010
- [ ] Endpoints retornam JSON válido
- [ ] CORS configurado corretamente
- [ ] Sessões funcionando
- [ ] CSVs sendo criados
- [ ] MySQL salvando dados (se configurado)

#### Frontend
- [ ] App carrega em http://localhost:5173
- [ ] Todas as rotas funcionam
- [ ] Formulários validam
- [ ] API calls funcionam
- [ ] Autenticação funciona
- [ ] Navegação funciona
- [ ] Sem erros no console

#### Integração
- [ ] Frontend → Backend comunicação OK
- [ ] Dados persistem corretamente
- [ ] Download de CSV funciona
- [ ] Login/Logout funciona
- [ ] Proteção de rotas funciona

### 🚨 Problemas Comuns

#### Backend não inicia
```bash
# Verificar porta
lsof -i :5010

# Matar processo
kill -9 <PID>

# Verificar ambiente
conda activate ciclo
which python
```

#### Frontend não inicia
```bash
# Limpar cache
rm -rf node_modules package-lock.json
npm install

# Verificar porta
lsof -i :5173
```

#### Erro de CORS
```python
# Verificar em backend/api.py
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
```

#### Erro de autenticação
```bash
# Verificar .env
cat backend/.env | grep ADMIN
```

### ✅ Teste Completo Passou?

Se todos os testes acima passaram:
- ✅ Aplicação está funcionando corretamente
- ✅ Pronta para desenvolvimento adicional
- ✅ Pode começar a usar em produção (após deploy adequado)

### 📊 Relatório de Teste

```
Data: ___/___/___
Testador: _____________

Testes Funcionais:     [ ] Passou  [ ] Falhou
Testes de Erro:        [ ] Passou  [ ] Falhou
Testes de Performance: [ ] Passou  [ ] Falhou
Testes de Segurança:   [ ] Passou  [ ] Falhou
Testes de Responsiv.:  [ ] Passou  [ ] Falhou

Observações:
_________________________________
_________________________________
_________________________________
```

### 🎯 Próximos Passos Após Testes

1. [ ] Corrigir bugs encontrados
2. [ ] Adicionar testes automatizados
3. [ ] Configurar CI/CD
4. [ ] Preparar para deploy
5. [ ] Documentar API (Swagger)
6. [ ] Adicionar monitoramento
