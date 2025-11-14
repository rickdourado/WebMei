# ⚡ Instalação Rápida - Portal Empreendedor React

## 🚀 Setup em 5 Minutos

### 1. Ativar Ambiente
```bash
conda activate ciclo
```

### 2. Instalar Dependências Backend
```bash
cd backend
pip install Flask-CORS
# Outras dependências já devem estar instaladas
```

### 3. Instalar Dependências Frontend
```bash
cd ../frontend
npm install
```

### 4. Iniciar Aplicação

**Opção A: Script Automático (Recomendado)**
```bash
cd ..
./scripts/start-react-dev.sh
```

**Opção B: Manual (2 terminais)**

Terminal 1 - Backend:
```bash
cd backend
python api.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 5. Acessar
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5010

---

## ✅ Verificação Rápida

### Testar Backend
```bash
curl http://localhost:5010/
curl http://localhost:5010/api/config
```

### Testar Frontend
Abrir navegador em: http://localhost:5173

### Diagnóstico Completo
```bash
python scripts/diagnostico_api.py
```

---

## 🔧 Solução de Problemas

### Erro: "No module named 'flask_cors'"
```bash
conda activate ciclo
pip install Flask-CORS
```

### Erro: "Connection refused"
Certifique-se que o backend está rodando:
```bash
cd backend
python api.py
```

### Erro: Frontend não carrega
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📚 Documentação Completa

- `RESUMO-MIGRACAO.md` - Resumo completo
- `GUIA-RAPIDO-REACT.md` - Guia de uso
- `SOLUCAO-PROBLEMAS.md` - Troubleshooting detalhado

---

## 🎯 Pronto!

Agora você pode:
- ✅ Cadastrar serviços
- ✅ Ver vagas públicas
- ✅ Fazer login admin (admin/admin)
- ✅ Gerenciar vagas

**Divirta-se! 🎉**
