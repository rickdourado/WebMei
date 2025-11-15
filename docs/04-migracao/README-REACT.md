# Portal Empreendedor - Versão React

Migração do Portal Empreendedor para arquitetura React + Flask API.

## Arquitetura

```
projeto/
├── backend/          # API REST Flask
│   ├── api.py       # Servidor API
│   ├── database.py  # Gerenciador de BD
│   ├── CSV/         # Armazenamento de serviços
│   └── refs/        # Dados de referência
└── frontend/        # SPA React
    ├── src/
    │   ├── pages/
    │   └── services/
    └── package.json
```

## Como Executar

### 1. Backend (API Flask)

```bash
# Ativar ambiente conda
conda activate ciclo

# Instalar dependências
cd backend
pip install -r requirements.txt

# Executar API
python api.py
```

API disponível em: `http://localhost:5010`

### 2. Frontend (React)

```bash
# Instalar dependências
cd frontend
npm install

# Executar em desenvolvimento
npm run dev
```

Frontend disponível em: `http://localhost:5173`

## Endpoints da API

### Públicos
- `GET /api/config` - Configurações (órgãos, tipos, etc)
- `GET /api/servicos` - Lista serviços
- `GET /api/servicos/<filename>` - Detalhes de serviço
- `POST /api/servicos` - Cria serviço
- `GET /api/download/<filename>` - Download CSV

### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Verifica autenticação

### Admin
- `DELETE /api/admin/servicos/<filename>` - Deleta serviço

## Funcionalidades

### Área Pública
- ✅ Cadastro de serviços com validação
- ✅ Listagem de vagas disponíveis
- ✅ Visualização detalhada de vagas
- ✅ Download de CSV

### Área Administrativa
- ✅ Login com autenticação
- ✅ Dashboard de gerenciamento
- ✅ Exclusão de vagas
- ✅ Proteção de rotas

## Diferenças da Versão Original

### Backend
- Rotas convertidas para API REST (JSON)
- CORS habilitado para React
- Mantém compatibilidade com CSV e MySQL
- Sessões Flask para autenticação

### Frontend
- SPA (Single Page Application)
- Roteamento client-side
- Estado gerenciado com React hooks
- Requisições assíncronas com Axios
- Interface responsiva

## Próximos Passos

1. **Deploy**: Configurar para produção
2. **Testes**: Adicionar testes unitários e E2E
3. **Melhorias**: 
   - Paginação na listagem
   - Filtros e busca
   - Upload de arquivos
   - Notificações em tempo real

## Migração do Código Antigo

O código original Flask com templates Jinja2 permanece em:
- `app.py` (versão original)
- `templates/` (templates HTML)
- `static/` (CSS/JS estáticos)

A nova versão React está em:
- `backend/api.py` (API REST)
- `frontend/` (aplicação React)

## Tecnologias

### Backend
- Flask 2.3.3
- Flask-CORS 4.0.0
- PyMySQL 1.1.0
- bcrypt 4.1.2

### Frontend
- React 18
- React Router DOM 6
- Axios 1.6
- Vite 5

## Desenvolvimento

Para desenvolvimento simultâneo:

```bash
# Terminal 1 - Backend
conda activate ciclo
cd backend
python api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Acesse: `http://localhost:5173`
