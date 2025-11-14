# 📁 Estrutura do Projeto - Portal Empreendedor

## Visão Geral

```
WebMei/
│
├── 📂 VERSÃO ORIGINAL (Flask Templates)
│   ├── app.py                    # Aplicação Flask original
│   ├── database.py               # Gerenciador MySQL
│   ├── templates/                # Templates Jinja2
│   │   ├── index.html
│   │   ├── vagas_public.html
│   │   ├── vaga_view.html
│   │   ├── admin_login.html
│   │   └── admin_dashboard.html
│   ├── static/                   # CSS/JS estáticos
│   ├── CSV/                      # Armazenamento de serviços
│   ├── refs/                     # Dados de referência
│   └── requirements.txt
│
├── 📂 VERSÃO REACT (SPA + API)
│   ├── backend/                  # API REST Flask
│   │   ├── api.py               # Servidor API REST
│   │   ├── database.py          # Gerenciador MySQL
│   │   ├── CSV/                 # Armazenamento
│   │   ├── refs/                # Dados de referência
│   │   ├── requirements.txt     # Dependências Python
│   │   └── README.md
│   │
│   └── frontend/                 # Aplicação React
│       ├── src/
│       │   ├── pages/           # Páginas da aplicação
│       │   │   ├── Home.jsx              # Cadastro de serviços
│       │   │   ├── Vagas.jsx             # Listagem pública
│       │   │   ├── VagaDetalhes.jsx      # Detalhes da vaga
│       │   │   ├── AdminLogin.jsx        # Login admin
│       │   │   └── AdminDashboard.jsx    # Dashboard admin
│       │   │
│       │   ├── services/        # Serviços de API
│       │   │   └── api.js       # Cliente Axios
│       │   │
│       │   ├── App.jsx          # Componente raiz + rotas
│       │   ├── App.css          # Estilos globais
│       │   ├── main.jsx         # Entry point
│       │   └── index.css
│       │
│       ├── public/              # Arquivos públicos
│       ├── package.json         # Dependências Node
│       ├── vite.config.js       # Configuração Vite
│       └── README.md
│
├── 📂 scripts/                   # Scripts utilitários
│   └── start-react-dev.sh       # Inicia backend + frontend
│
├── 📂 docs/                      # Documentação
│
├── 📄 .env                       # Variáveis de ambiente
├── 📄 .gitignore
├── 📄 README.md                  # README principal
├── 📄 README-REACT.md            # Documentação React
├── 📄 GUIA-RAPIDO-REACT.md       # Guia rápido
└── 📄 COMPARACAO-VERSOES.md      # Comparação versões
```

## Detalhamento

### 🔵 Backend API (Flask)

```
backend/
├── api.py                        # Servidor REST API
│   ├── /api/config              # GET - Configurações
│   ├── /api/servicos            # GET/POST - Serviços
│   ├── /api/servicos/<file>     # GET - Detalhes
│   ├── /api/download/<file>     # GET - Download CSV
│   ├── /api/auth/login          # POST - Login
│   ├── /api/auth/logout         # POST - Logout
│   ├── /api/auth/check          # GET - Verificar auth
│   └── /api/admin/servicos/<f>  # DELETE - Deletar
│
├── database.py                   # Gerenciador MySQL
│   ├── DatabaseManager
│   ├── insert_servico()
│   └── authenticate_user()
│
├── CSV/                          # Armazenamento
│   └── {titulo}_{timestamp}.csv
│
└── refs/                         # Dados de referência
    ├── ServicosConsolidados.csv
    ├── lista_orgaos.csv
    └── PortalEmpreendedorUnificado.csv
```

### ⚛️ Frontend React

```
frontend/src/
├── pages/                        # Páginas (Rotas)
│   ├── Home.jsx                 # / - Cadastro
│   ├── Vagas.jsx                # /vagas - Listagem
│   ├── VagaDetalhes.jsx         # /vaga/:filename
│   ├── AdminLogin.jsx           # /admin/login
│   └── AdminDashboard.jsx       # /admin
│
├── services/
│   └── api.js                   # Cliente API
│       ├── getConfig()
│       ├── getServicos()
│       ├── createServico()
│       ├── deleteServico()
│       ├── login()
│       └── logout()
│
├── App.jsx                       # Router + Rotas
├── App.css                       # Estilos
└── main.jsx                      # Entry point
```

## Fluxo de Dados

### Cadastro de Serviço

```
1. Usuário preenche formulário (Home.jsx)
   ↓
2. handleSubmit() → apiService.createServico()
   ↓
3. POST /api/servicos (api.js)
   ↓
4. Flask recebe JSON (api.py)
   ↓
5. Valida dados
   ↓
6. Salva CSV + MySQL
   ↓
7. Retorna JSON success
   ↓
8. React atualiza UI
```

### Listagem de Vagas

```
1. Componente monta (Vagas.jsx)
   ↓
2. useEffect() → apiService.getServicos()
   ↓
3. GET /api/servicos
   ↓
4. Flask lê CSVs
   ↓
5. Retorna JSON array
   ↓
6. React renderiza cards
```

### Autenticação Admin

```
1. Login form (AdminLogin.jsx)
   ↓
2. POST /api/auth/login
   ↓
3. Flask verifica credenciais
   ↓
4. Cria sessão
   ↓
5. Retorna user data
   ↓
6. React navega para /admin
   ↓
7. AdminDashboard verifica auth
   ↓
8. GET /api/auth/check
```

## Tecnologias por Camada

### Backend
```
Flask 2.3.3          → Framework web
Flask-CORS 4.0.0     → CORS para React
PyMySQL 1.1.0        → Conexão MySQL
bcrypt 4.1.2         → Hash de senhas
python-dotenv 1.0.1  → Variáveis de ambiente
```

### Frontend
```
React 18             → UI Library
React Router 6       → Roteamento
Axios 1.6            → HTTP Client
Vite 5               → Build tool
```

## Portas e URLs

### Desenvolvimento
```
Backend API:  http://localhost:5010
Frontend:     http://localhost:5173
MySQL:        localhost:3306
```

### Produção (exemplo)
```
Backend API:  https://api.portalempreendedor.com
Frontend:     https://portalempreendedor.com
MySQL:        servidor-db:3306
```

## Arquivos de Configuração

### Backend
```
.env                  # Variáveis de ambiente
  ├── SECRET_KEY
  ├── ADMIN_USERNAME
  ├── ADMIN_PASSWORD
  ├── DB_HOST
  ├── DB_USER
  ├── DB_PASSWORD
  └── DB_NAME

requirements.txt      # Dependências Python
```

### Frontend
```
package.json          # Dependências Node
vite.config.js        # Config Vite
eslint.config.js      # Config ESLint

src/services/api.js   # Config API URL
  └── API_BASE_URL = 'http://localhost:5010/api'
```

## Comandos Úteis

### Desenvolvimento
```bash
# Iniciar tudo
./scripts/start-react-dev.sh

# Apenas backend
conda activate ciclo
cd backend && python api.py

# Apenas frontend
cd frontend && npm run dev
```

### Build
```bash
# Backend (produção)
cd backend
pip install -r requirements.txt
gunicorn -w 4 api:app

# Frontend (build)
cd frontend
npm run build
# Arquivos em: frontend/dist/
```

### Testes
```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

## Dependências

### Backend precisa de:
- Python 3.8+
- Conda (ambiente ciclo)
- MySQL 5.7+

### Frontend precisa de:
- Node.js 18+
- npm 9+

## Próximos Passos

1. ✅ Estrutura básica criada
2. ✅ Backend API funcionando
3. ✅ Frontend React funcionando
4. ⏳ Testes automatizados
5. ⏳ CI/CD
6. ⏳ Deploy produção
7. ⏳ Monitoramento
8. ⏳ Documentação API (Swagger)

## Manutenção

### Adicionar nova funcionalidade:

1. **Backend**: Criar endpoint em `backend/api.py`
2. **Frontend**: Adicionar método em `frontend/src/services/api.js`
3. **UI**: Criar/atualizar componente em `frontend/src/pages/`
4. **Rota**: Adicionar em `frontend/src/App.jsx`

### Atualizar dependências:

```bash
# Backend
cd backend
pip list --outdated
pip install -U <package>

# Frontend
cd frontend
npm outdated
npm update
```

## Backup

### Dados importantes:
```
CSV/                  # Serviços cadastrados
refs/                 # Dados de referência
.env                  # Configurações
MySQL database        # Dados persistentes
```

### Script de backup:
```bash
# Backup CSVs
tar -czf backup-csv-$(date +%Y%m%d).tar.gz backend/CSV/

# Backup MySQL
mysqldump -u user -p database > backup-$(date +%Y%m%d).sql
```
