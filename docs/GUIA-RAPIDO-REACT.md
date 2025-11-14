# 🚀 Guia Rápido - Portal Empreendedor React

## Início Rápido

### Opção 1: Script Automático (Recomendado)

```bash
conda activate ciclo
./scripts/start-react-dev.sh
```

Este script inicia automaticamente o backend e frontend.

### Opção 2: Manual

**Terminal 1 - Backend:**
```bash
conda activate ciclo
cd backend
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Acessar a Aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5010

## Estrutura do Projeto

```
Portal Empreendedor/
│
├── backend/              # API Flask
│   ├── api.py           # Servidor REST
│   ├── database.py      # MySQL
│   ├── CSV/             # Armazenamento
│   └── refs/            # Dados de referência
│
└── frontend/            # React SPA
    ├── src/
    │   ├── pages/       # Páginas
    │   │   ├── Home.jsx              # Cadastro
    │   │   ├── Vagas.jsx             # Listagem
    │   │   ├── VagaDetalhes.jsx      # Detalhes
    │   │   ├── AdminLogin.jsx        # Login
    │   │   └── AdminDashboard.jsx    # Admin
    │   └── services/
    │       └── api.js   # Cliente API
    └── package.json
```

## Fluxo de Uso

### 1. Cadastrar Serviço
1. Acesse http://localhost:5173
2. Preencha o formulário
3. Clique em "Cadastrar Serviço"
4. Serviço salvo em CSV e MySQL

### 2. Ver Vagas Públicas
1. Clique em "Ver Vagas" no menu
2. Navegue pelas oportunidades
3. Clique em "Ver Detalhes" para mais informações
4. Baixe o CSV se necessário

### 3. Administração
1. Acesse http://localhost:5173/admin/login
2. Login: `admin` / Senha: `admin` (padrão)
3. Gerencie vagas no dashboard
4. Exclua vagas se necessário

## Endpoints da API

### Públicos
```
GET  /api/config                    # Configurações
GET  /api/servicos                  # Lista serviços
GET  /api/servicos/<filename>       # Detalhes
POST /api/servicos                  # Criar serviço
GET  /api/download/<filename>       # Download CSV
```

### Autenticação
```
POST /api/auth/login                # Login
POST /api/auth/logout               # Logout
GET  /api/auth/check                # Verificar auth
```

### Admin
```
DELETE /api/admin/servicos/<filename>  # Deletar
```

## Exemplo de Requisição

### Criar Serviço
```javascript
POST /api/servicos
Content-Type: application/json

{
  "orgao_demandante": "Prefeitura",
  "titulo_servico": "Pintor",
  "tipo_atividade": "Construção",
  "especificacao_atividade": "Pintura residencial",
  "descricao_servico": "Pintura de casa",
  "endereco": "Rua A",
  "numero": "123",
  "bairro": "Centro",
  "forma_pagamento": "Dinheiro",
  "prazo_pagamento": "30 dias",
  "prazo_expiracao": "2024-12-31",
  "data_limite_execucao": "2024-12-15"
}
```

## Tecnologias

### Backend
- Flask 2.3.3 (API REST)
- Flask-CORS (CORS)
- PyMySQL (MySQL)
- bcrypt (Autenticação)

### Frontend
- React 18 (UI)
- React Router 6 (Roteamento)
- Axios (HTTP)
- Vite (Build)

## Desenvolvimento

### Adicionar Nova Página

1. Criar componente em `frontend/src/pages/`
2. Adicionar rota em `frontend/src/App.jsx`
3. Criar endpoint correspondente em `backend/api.py`

### Adicionar Novo Endpoint

1. Adicionar rota em `backend/api.py`
2. Adicionar método em `frontend/src/services/api.js`
3. Usar no componente React

## Troubleshooting

### Backend não inicia
```bash
# Verificar ambiente conda
conda activate ciclo

# Reinstalar dependências
cd backend
pip install -r requirements.txt
```

### Frontend não inicia
```bash
# Reinstalar dependências
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro de CORS
Verifique se o backend está rodando em `localhost:5010` e o frontend em `localhost:5173`.

### Erro de autenticação
Verifique as credenciais no arquivo `.env`:
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

## Build para Produção

### Backend
```bash
cd backend
# Configurar variáveis de ambiente
# Usar servidor WSGI (gunicorn, uwsgi)
gunicorn -w 4 -b 0.0.0.0:5010 api:app
```

### Frontend
```bash
cd frontend
npm run build
# Arquivos em frontend/dist/
# Servir com nginx ou outro servidor
```

## Próximos Passos

- [ ] Adicionar testes automatizados
- [ ] Implementar paginação
- [ ] Adicionar filtros de busca
- [ ] Melhorar validações
- [ ] Adicionar upload de arquivos
- [ ] Implementar notificações
- [ ] Deploy em produção

## Suporte

Para dúvidas ou problemas, consulte:
- `README-REACT.md` - Documentação completa
- `backend/README.md` - Documentação do backend
- `frontend/README.md` - Documentação do frontend
