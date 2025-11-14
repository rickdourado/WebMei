# 🔧 Solução de Problemas - Portal Empreendedor React

## Diagnóstico Rápido

### 1. Execute o diagnóstico automático

```bash
conda activate ciclo
python scripts/diagnostico_api.py
```

Este script verifica:
- ✅ Imports necessários
- ✅ Arquivos de configuração
- ✅ Diretórios
- ✅ Conexão com banco de dados
- ✅ Carregamento de dados

---

## Problemas Comuns

### ❌ Problema: "No module named 'flask_cors'"

**Sintoma**: API não inicia, erro de import

**Solução**:
```bash
conda activate ciclo
pip install Flask-CORS
```

**Verificar**:
```bash
python -c "from flask_cors import CORS; print('OK')"
```

---

### ❌ Problema: "API retorna 404 Not Found"

**Sintomas**:
- Acessa `http://localhost:5010` → 404
- Acessa `http://localhost:5010/api/config` → 404

**Causas possíveis**:

#### 1. API não está rodando
```bash
# Verificar se está rodando
curl http://localhost:5010

# Se não responder, iniciar:
cd backend
python api.py
```

#### 2. Porta errada
```bash
# Verificar qual porta está rodando
lsof -i :5010

# Ou verificar no terminal onde iniciou a API:
# * Running on http://127.0.0.1:5010
```

#### 3. Rota incorreta
```bash
# ❌ Errado
curl http://localhost:5010/config

# ✅ Correto
curl http://localhost:5010/api/config
```

**Teste os endpoints corretos**:
```bash
# Rota raiz (informações da API)
curl http://localhost:5010/

# Configurações
curl http://localhost:5010/api/config

# Lista de serviços
curl http://localhost:5010/api/servicos
```

---

### ❌ Problema: "Connection refused" ao acessar API

**Sintoma**: Frontend não consegue conectar ao backend

**Solução**:

1. **Verificar se backend está rodando**:
```bash
curl http://localhost:5010/
```

2. **Verificar CORS**:
```javascript
// No navegador, console:
fetch('http://localhost:5010/api/config')
  .then(r => r.json())
  .then(console.log)
```

3. **Verificar URL no frontend**:
```javascript
// frontend/src/services/api.js
const API_BASE_URL = 'http://localhost:5010/api';
```

---

### ❌ Problema: Banco de dados não conecta

**Sintoma**: Aviso "Banco de dados não disponível"

**Solução**:

1. **Verificar MySQL está rodando**:
```bash
sudo systemctl status mysql
# ou
sudo service mysql status
```

2. **Verificar credenciais no .env**:
```bash
cat backend/.env | grep DB_
```

Deve ter:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=servicosmei
```

3. **Testar conexão**:
```bash
mysql -u seu_usuario -p -e "SHOW DATABASES;"
```

4. **Criar banco se não existir**:
```sql
CREATE DATABASE IF NOT EXISTS servicosmei;
```

**Nota**: A API funciona sem MySQL (apenas com CSV)

---

### ❌ Problema: Frontend não carrega

**Sintoma**: Página em branco ou erro no navegador

**Solução**:

1. **Verificar se está rodando**:
```bash
cd frontend
npm run dev
```

2. **Verificar console do navegador** (F12):
   - Erros em vermelho?
   - Erro de CORS?
   - Erro de conexão?

3. **Limpar cache e reinstalar**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

4. **Verificar porta**:
   - Frontend deve estar em: `http://localhost:5173`
   - Backend deve estar em: `http://localhost:5010`

---

### ❌ Problema: Erro de CORS

**Sintoma**: Console mostra "CORS policy blocked"

**Solução**:

1. **Verificar CORS no backend**:
```python
# backend/api.py
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
```

2. **Verificar se backend está rodando**:
```bash
curl http://localhost:5010/api/config
```

3. **Reiniciar backend**:
```bash
# Ctrl+C no terminal do backend
python api.py
```

---

### ❌ Problema: Formulário não envia

**Sintomas**:
- Clica em "Cadastrar" mas nada acontece
- Erro no console

**Solução**:

1. **Verificar console do navegador** (F12)

2. **Verificar campos obrigatórios**:
   - Todos os campos com * estão preenchidos?

3. **Verificar API está respondendo**:
```bash
curl -X POST http://localhost:5010/api/servicos \
  -H "Content-Type: application/json" \
  -d '{"orgao_demandante":"Teste",...}'
```

4. **Verificar validação de número**:
   - Aceita: `123`, `S/N`, `SN`
   - Não aceita: `ABC123`, `#45`

---

### ❌ Problema: Login admin não funciona

**Sintomas**:
- Credenciais corretas mas não loga
- Erro "Credenciais inválidas"

**Solução**:

1. **Verificar credenciais no .env**:
```bash
cat backend/.env | grep ADMIN
```

Padrão:
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```

2. **Testar via API**:
```bash
curl -X POST http://localhost:5010/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

3. **Verificar sessões**:
```python
# backend/api.py
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
```

---

### ❌ Problema: CSV não é criado

**Sintomas**:
- Formulário envia com sucesso
- Mas arquivo CSV não aparece em `backend/CSV/`

**Solução**:

1. **Verificar permissões**:
```bash
ls -la backend/CSV/
chmod 755 backend/CSV/
```

2. **Verificar se diretório existe**:
```bash
mkdir -p backend/CSV
```

3. **Verificar logs do backend**:
   - Terminal onde rodou `python api.py`
   - Deve mostrar: "✓ Serviço inserido..."

---

## Scripts de Teste

### Teste completo da API
```bash
python scripts/test_api_simple.py
```

### Diagnóstico completo
```bash
python scripts/diagnostico_api.py
```

### Teste via bash
```bash
./scripts/test-api.sh
```

---

## Verificação Passo a Passo

### 1. Ambiente Python
```bash
conda activate ciclo
python --version  # Deve ser 3.8+
```

### 2. Dependências Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Dependências Frontend
```bash
cd frontend
npm install
```

### 4. Iniciar Backend
```bash
cd backend
python api.py
```

Deve mostrar:
```
* Running on http://127.0.0.1:5010
```

### 5. Testar Backend
```bash
# Em outro terminal
curl http://localhost:5010/
curl http://localhost:5010/api/config
```

### 6. Iniciar Frontend
```bash
cd frontend
npm run dev
```

Deve mostrar:
```
Local: http://localhost:5173/
```

### 7. Testar Frontend
Abrir navegador em: `http://localhost:5173`

---

## Logs e Debug

### Backend (Flask)
```python
# backend/api.py já tem debug=True
app.run(host='0.0.0.0', port=5010, debug=True)
```

Logs aparecem no terminal onde rodou `python api.py`

### Frontend (React)
```javascript
// Console do navegador (F12)
// Adicionar logs:
console.log('API Response:', response);
```

### Verificar requisições
- Abrir DevTools (F12)
- Aba "Network"
- Fazer ação no frontend
- Ver requisições para `localhost:5010`

---

## Reinstalação Completa

Se nada funcionar, reinstale tudo:

### Backend
```bash
cd backend
rm -rf __pycache__
pip uninstall -y Flask Flask-CORS PyMySQL bcrypt python-dotenv
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
rm -rf node_modules package-lock.json dist
npm install
```

---

## Portas em Uso

### Verificar portas
```bash
# Backend (5010)
lsof -i :5010

# Frontend (5173)
lsof -i :5173

# MySQL (3306)
lsof -i :3306
```

### Matar processo
```bash
# Encontrar PID
lsof -i :5010

# Matar
kill -9 <PID>
```

---

## Checklist Final

Antes de reportar problema, verificar:

- [ ] Ambiente conda ativado (`conda activate ciclo`)
- [ ] Flask-CORS instalado (`pip list | grep Flask-CORS`)
- [ ] Backend rodando (`curl http://localhost:5010/`)
- [ ] Frontend rodando (`curl http://localhost:5173/`)
- [ ] Sem erros no console do navegador (F12)
- [ ] Sem erros no terminal do backend
- [ ] Arquivos .env configurados
- [ ] Diretórios CSV/ e refs/ existem
- [ ] Permissões corretas nos diretórios

---

## Contato e Suporte

Se o problema persistir:

1. Execute o diagnóstico:
```bash
python scripts/diagnostico_api.py > diagnostico.txt
```

2. Capture logs do backend:
```bash
cd backend
python api.py 2>&1 | tee backend.log
```

3. Capture erros do frontend:
   - F12 → Console → Copiar erros

4. Verifique a documentação:
   - `README-REACT.md`
   - `GUIA-RAPIDO-REACT.md`
   - `ESTRUTURA-PROJETO.md`
