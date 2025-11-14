# 🚀 Instruções de Migração - CSV para Banco de Dados

**Versão**: 2.0  
**Data**: 14/11/2025

---

## ⚡ Início Rápido

### 1. Ative o ambiente

```bash
conda activate ciclo
```

### 2. Execute a migração

```bash
python scripts/migrar_csv_para_banco.py
```

### 3. Teste o sistema

```bash
# Inicie o backend
cd backend
python api.py

# Em outro terminal, teste a API
curl http://localhost:5010/api/servicos
```

---

## 📝 O Que Mudou?

### ✅ Antes (v1.x)
- Salvava em CSV + Banco (duplicado)
- Lia apenas dos CSVs
- Deletava apenas CSVs
- Usava filenames como identificadores

### ✅ Agora (v2.0)
- Salva apenas no banco
- Lê do banco
- Deleta do banco
- Usa IDs numéricos
- CSV gerado sob demanda

---

## 🔧 Mudanças na API

### Endpoints Atualizados

```bash
# Listar serviços (sem mudança na URL, mas retorna IDs)
GET /api/servicos

# Buscar serviço (agora usa ID)
GET /api/servicos/123  # antes: /api/servicos/arquivo.csv

# Criar serviço (retorna ID ao invés de filename)
POST /api/servicos

# Exportar CSV (novo endpoint)
GET /api/servicos/123/export

# Deletar serviço (agora usa ID)
DELETE /api/admin/servicos/123  # antes: /api/admin/servicos/arquivo.csv
```

---

## 🎨 Atualizações Necessárias no Frontend

### 1. Componente de Listagem

```javascript
// ANTES
{servicos.map(servico => (
  <Link to={`/vaga/${servico.arquivo}`}>
    {servico.titulo_servico}
  </Link>
))}

// AGORA
{servicos.map(servico => (
  <Link to={`/vaga/${servico.id}`}>
    {servico.titulo_servico}
  </Link>
))}
```

### 2. Visualização de Serviço

```javascript
// ANTES
const { filename } = useParams();
fetch(`/api/servicos/${filename}`)

// AGORA
const { id } = useParams();
fetch(`/api/servicos/${id}`)
```

### 3. Download de CSV

```javascript
// ANTES
<a href={`/api/download/${servico.arquivo}`}>Download CSV</a>

// AGORA
<a href={`/api/servicos/${servico.id}/export`}>Download CSV</a>
```

### 4. Exclusão de Serviço

```javascript
// ANTES
fetch(`/api/admin/servicos/${servico.arquivo}`, { method: 'DELETE' })

// AGORA
fetch(`/api/admin/servicos/${servico.id}`, { method: 'DELETE' })
```

### 5. Resposta de Criação

```javascript
// ANTES
const response = await fetch('/api/servicos', {...});
const { filename } = await response.json();

// AGORA
const response = await fetch('/api/servicos', {...});
const { id } = await response.json();
```

---

## 📄 Estrutura de Dados

### Resposta de Listagem

```json
[
  {
    "id": 1,
    "orgao_demandante": "Secretaria de Obras",
    "titulo_servico": "Pintura Residencial",
    "tipo_atividade": "Pintor",
    "especificacao_atividade": "Pintura de Interiores",
    "descricao_servico": "...",
    "outras_informacoes": "...",
    "endereco": "Rua das Flores",
    "numero": "123",
    "bairro": "Centro",
    "forma_pagamento": "Transferência",
    "prazo_pagamento": "30 dias",
    "prazo_expiracao": "2025-12-31",
    "data_limite_execucao": "2025-11-30",
    "data_cadastro": "2025-11-14 10:30:00"
  }
]
```

---

## 🧪 Testes

### Teste 1: Criar Serviço

```bash
curl -X POST http://localhost:5010/api/servicos \
  -H "Content-Type: application/json" \
  -d '{
    "orgao_demandante": "Teste",
    "titulo_servico": "Serviço Teste",
    "especificacao_atividade": "Teste",
    "descricao_servico": "Descrição teste",
    "endereco": "Rua Teste",
    "numero": "123",
    "bairro": "Centro",
    "forma_pagamento": "Dinheiro",
    "prazo_pagamento": "30 dias",
    "prazo_expiracao": "2025-12-31",
    "data_limite_execucao": "2025-11-30"
  }'
```

### Teste 2: Listar Serviços

```bash
curl http://localhost:5010/api/servicos
```

### Teste 3: Buscar Serviço

```bash
curl http://localhost:5010/api/servicos/1
```

### Teste 4: Exportar CSV

```bash
curl http://localhost:5010/api/servicos/1/export -o servico.csv
```

### Teste 5: Deletar Serviço (requer autenticação)

```bash
# Primeiro faça login
curl -X POST http://localhost:5010/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt

# Depois delete
curl -X DELETE http://localhost:5010/api/admin/servicos/1 \
  -b cookies.txt
```

---

## ⚠️ Problemas Comuns

### Erro: "Banco de dados não disponível"

**Solução**:
1. Verifique se o MySQL está rodando
2. Verifique as credenciais no `.env`
3. Verifique se o banco `servicosmei` existe

```bash
# Verificar MySQL
sudo systemctl status mysql

# Criar banco se não existir
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS servicosmei;"
```

### Erro: "Serviço não encontrado"

**Solução**:
- Certifique-se de usar IDs numéricos, não filenames
- Verifique se o serviço existe no banco

```bash
# Verificar serviços no banco
mysql -u root -p servicosmei -e "SELECT id, titulo_servico FROM servicos_mei;"
```

### Frontend não carrega serviços

**Solução**:
1. Verifique se o backend está rodando
2. Verifique o console do navegador
3. Atualize o código do frontend conforme instruções acima

---

## 📦 Backup e Rollback

### Fazer Backup

```bash
# Backup do banco
mysqldump -u root -p servicosmei > backup_$(date +%Y%m%d).sql

# Backup dos CSVs (se ainda existirem)
tar -czf csv_backup_$(date +%Y%m%d).tar.gz CSV/
```

### Restaurar Backup

```bash
# Restaurar banco
mysql -u root -p servicosmei < backup_YYYYMMDD.sql

# Restaurar CSVs
tar -xzf csv_backup_YYYYMMDD.tar.gz
```

---

## 📚 Documentação Adicional

- `docs/CHANGELOG-v2.0.md` - Changelog completo
- `docs/analise-duplicacao-csv-banco.md` - Análise do problema
- `docs/estrutura-mysql.md` - Estrutura do banco

---

## ✅ Checklist Final

Antes de colocar em produção:

- [ ] Migração executada com sucesso
- [ ] Backup do banco realizado
- [ ] Frontend atualizado
- [ ] Templates HTML atualizados
- [ ] Testes de criação funcionando
- [ ] Testes de listagem funcionando
- [ ] Testes de visualização funcionando
- [ ] Testes de exclusão funcionando
- [ ] Testes de export funcionando
- [ ] Autenticação funcionando
- [ ] Logs verificados
- [ ] Performance testada

---

## 🆘 Suporte

Em caso de problemas:

1. Verifique os logs do servidor
2. Consulte a documentação em `docs/`
3. Revise as mudanças no código
4. Teste os endpoints individualmente
