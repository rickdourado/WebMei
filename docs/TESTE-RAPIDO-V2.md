# 🧪 Teste Rápido - Versão 2.0

**Objetivo**: Validar que o sistema está funcionando corretamente após a migração

---

## 🚀 Preparação

### 1. Ative o ambiente

```bash
conda activate ciclo
```

### 2. Verifique o banco de dados

```bash
mysql -u root -p -e "USE servicosmei; SELECT COUNT(*) as total FROM servicos_mei;"
```

---

## 📝 Testes Backend

### Teste 1: Verificar API está online

```bash
curl http://localhost:5010/
```

**Esperado**:
```json
{
  "name": "Portal Empreendedor API",
  "version": "2.0.0",
  "status": "online",
  "database": "MySQL"
}
```

### Teste 2: Listar serviços

```bash
curl http://localhost:5010/api/servicos
```

**Esperado**: Array de serviços com IDs numéricos

```json
[
  {
    "id": 1,
    "titulo_servico": "...",
    "orgao_demandante": "...",
    ...
  }
]
```

### Teste 3: Criar novo serviço

```bash
curl -X POST http://localhost:5010/api/servicos \
  -H "Content-Type: application/json" \
  -d '{
    "orgao_demandante": "Secretaria de Teste",
    "titulo_servico": "Teste API v2.0",
    "tipo_atividade": "Pintor",
    "especificacao_atividade": "Pintura de Interiores",
    "descricao_servico": "Serviço de teste para validar API v2.0",
    "outras_informacoes": "Teste",
    "endereco": "Rua Teste",
    "numero": "123",
    "bairro": "Centro",
    "forma_pagamento": "Dinheiro",
    "prazo_pagamento": "30 dias",
    "prazo_expiracao": "2025-12-31",
    "data_limite_execucao": "2025-11-30"
  }'
```

**Esperado**:
```json
{
  "message": "Serviço cadastrado com sucesso",
  "id": 123,
  "data": {...}
}
```

**✅ Anote o ID retornado para os próximos testes!**

### Teste 4: Buscar serviço por ID

```bash
# Substitua 123 pelo ID retornado no teste anterior
curl http://localhost:5010/api/servicos/123
```

**Esperado**: Dados completos do serviço

### Teste 5: Exportar CSV

```bash
# Substitua 123 pelo ID do serviço
curl http://localhost:5010/api/servicos/123/export -o teste.csv

# Verificar conteúdo
cat teste.csv
```

**Esperado**: Arquivo CSV com os dados do serviço

### Teste 6: Login admin

```bash
curl -X POST http://localhost:5010/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt
```

**Esperado**:
```json
{
  "message": "Login realizado com sucesso",
  "user": {
    "id": 0,
    "username": "admin"
  }
}
```

### Teste 7: Verificar autenticação

```bash
curl http://localhost:5010/api/auth/check -b cookies.txt
```

**Esperado**:
```json
{
  "authenticated": true,
  "user": {
    "id": 0,
    "username": "admin"
  }
}
```

### Teste 8: Deletar serviço (autenticado)

```bash
# Substitua 123 pelo ID do serviço de teste
curl -X DELETE http://localhost:5010/api/admin/servicos/123 -b cookies.txt
```

**Esperado**:
```json
{
  "message": "Serviço excluído com sucesso"
}
```

### Teste 9: Verificar deleção

```bash
# Tentar buscar o serviço deletado
curl http://localhost:5010/api/servicos/123
```

**Esperado**:
```json
{
  "error": "Serviço não encontrado"
}
```

---

## 🎨 Testes Frontend (Após Atualização)

### Teste 1: Página inicial

1. Acesse `http://localhost:5173`
2. Preencha o formulário
3. Submeta
4. Verifique se retorna ID ao invés de filename

### Teste 2: Listagem de vagas

1. Acesse `http://localhost:5173/vagas`
2. Verifique se as vagas aparecem
3. Clique em uma vaga
4. Verifique se a URL usa ID: `/vaga/123`

### Teste 3: Visualização de vaga

1. Na página de detalhes da vaga
2. Verifique se todos os dados aparecem
3. Teste o botão de download CSV
4. Verifique se o CSV é gerado corretamente

### Teste 4: Admin dashboard

1. Acesse `http://localhost:5173/admin/login`
2. Faça login (admin/admin)
3. Verifique se a listagem aparece
4. Teste deletar uma vaga
5. Verifique se foi removida

---

## 🔍 Verificações no Banco

### Verificar serviços cadastrados

```sql
USE servicosmei;

-- Contar total
SELECT COUNT(*) as total FROM servicos_mei;

-- Listar últimos 5
SELECT id, titulo_servico, orgao_demandante, data_cadastro 
FROM servicos_mei 
ORDER BY data_cadastro DESC 
LIMIT 5;

-- Buscar por ID
SELECT * FROM servicos_mei WHERE id = 123;

-- Verificar serviços por órgão
SELECT orgao_demandante, COUNT(*) as total 
FROM servicos_mei 
GROUP BY orgao_demandante 
ORDER BY total DESC;
```

---

## ✅ Checklist de Validação

### Backend
- [ ] API responde na porta 5010
- [ ] Endpoint raiz retorna versão 2.0.0
- [ ] Listagem retorna dados do banco
- [ ] Criação salva no banco e retorna ID
- [ ] Busca por ID funciona
- [ ] Export CSV funciona
- [ ] Login funciona
- [ ] Deleção funciona (autenticado)
- [ ] Deleção falha sem autenticação

### Banco de Dados
- [ ] Tabela servicos_mei existe
- [ ] Dados são inseridos corretamente
- [ ] Dados são listados corretamente
- [ ] Dados são deletados corretamente
- [ ] Datas são armazenadas corretamente

### Frontend (Após Atualização)
- [ ] Formulário de cadastro funciona
- [ ] Listagem de vagas funciona
- [ ] Visualização de vaga funciona
- [ ] Download de CSV funciona
- [ ] Login admin funciona
- [ ] Dashboard admin funciona
- [ ] Deleção de vaga funciona

---

## 🐛 Problemas Comuns

### Erro: "Banco de dados não disponível"

```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Iniciar MySQL se necessário
sudo systemctl start mysql

# Verificar credenciais no .env
cat backend/.env | grep DB_
```

### Erro: "Connection refused"

```bash
# Verificar se o backend está rodando
ps aux | grep "python.*api.py"

# Iniciar backend se necessário
cd backend
python api.py
```

### Erro: "Serviço não encontrado"

- Certifique-se de usar IDs numéricos
- Verifique se o serviço existe no banco
- Não use filenames (arquivo.csv)

### Erro 401: "Não autorizado"

```bash
# Fazer login primeiro
curl -X POST http://localhost:5010/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt

# Usar cookies nas requisições seguintes
curl ... -b cookies.txt
```

---

## 📊 Resultados Esperados

### ✅ Sucesso

```
✓ API online (versão 2.0.0)
✓ Banco de dados conectado
✓ Criação de serviços funciona
✓ Listagem retorna IDs numéricos
✓ Busca por ID funciona
✓ Export CSV funciona
✓ Autenticação funciona
✓ Deleção funciona
```

### ❌ Falha

Se algum teste falhar:

1. Verifique os logs do servidor
2. Verifique a conexão com o banco
3. Verifique as credenciais
4. Consulte `docs/INSTRUCOES-MIGRACAO.md`
5. Revise o código modificado

---

## 🔄 Teste de Migração

### Migrar CSVs existentes

```bash
# Execute o script de migração
python scripts/migrar_csv_para_banco.py

# Verifique os resultados
mysql -u root -p servicosmei -e "SELECT COUNT(*) FROM servicos_mei;"
```

**Esperado**:
- Todos os CSVs migrados com sucesso
- Nenhum erro
- Dados preservados

---

## 📈 Métricas de Performance

### Teste de carga (opcional)

```bash
# Instalar apache bench se necessário
sudo apt-get install apache2-utils

# Testar listagem (100 requisições, 10 concorrentes)
ab -n 100 -c 10 http://localhost:5010/api/servicos

# Verificar tempo de resposta
# Esperado: < 100ms por requisição
```

---

## 🎉 Conclusão

Se todos os testes passaram:

✅ **Sistema v2.0 funcionando corretamente!**

Próximos passos:
1. Atualizar frontend React
2. Atualizar templates HTML
3. Fazer testes de integração completos
4. Deploy em produção

---

## 📞 Suporte

Em caso de problemas:

1. Consulte `docs/INSTRUCOES-MIGRACAO.md`
2. Revise `docs/CHANGELOG-v2.0.md`
3. Verifique `docs/analise-duplicacao-csv-banco.md`
4. Analise os logs do servidor
