# Frontend React - Portal Empreendedor

Interface React para o Portal Empreendedor Unificado.

## Tecnologias

- React 18
- React Router DOM
- Axios
- Vite

## Instalação

```bash
npm install
```

## Desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`

## Build para Produção

```bash
npm run build
```

## Estrutura

```
src/
├── pages/              # Páginas da aplicação
│   ├── Home.jsx       # Formulário de cadastro
│   ├── Vagas.jsx      # Listagem de vagas
│   ├── VagaDetalhes.jsx
│   ├── AdminLogin.jsx
│   └── AdminDashboard.jsx
├── services/          # Serviços de API
│   └── api.js
├── App.jsx           # Componente principal
└── main.jsx          # Entry point
```

## Rotas

- `/` - Cadastro de serviços
- `/vagas` - Listagem pública
- `/vaga/:filename` - Detalhes da vaga
- `/admin/login` - Login administrativo
- `/admin` - Dashboard admin

## Configuração

A URL da API está configurada em `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:5010/api';
```

Ajuste conforme necessário para produção.
