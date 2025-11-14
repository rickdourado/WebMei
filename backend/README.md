# Backend API - Portal Empreendedor

API REST em Flask para o Portal Empreendedor.

## Instalação

```bash
conda activate ciclo
pip install -r requirements.txt
```

## Executar

```bash
python api.py
```

A API estará disponível em `http://localhost:5010`

## Endpoints

### Públicos
- `GET /api/config` - Configurações iniciais (órgãos, tipos de atividade, etc)
- `GET /api/servicos` - Lista todos os serviços
- `GET /api/servicos/<filename>` - Detalhes de um serviço
- `POST /api/servicos` - Cria novo serviço
- `GET /api/download/<filename>` - Download do CSV

### Autenticação
- `POST /api/auth/login` - Login admin
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Verifica autenticação

### Admin (requer autenticação)
- `DELETE /api/admin/servicos/<filename>` - Deleta serviço
