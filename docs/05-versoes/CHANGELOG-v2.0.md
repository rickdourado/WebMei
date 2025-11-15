# Changelog - Versão 2.0

**Data**: 14/11/2025  
**Tipo**: Refatoração Major - Breaking Changes

---

## 🎯 Objetivo

Migrar o sistema de armazenamento baseado em arquivos CSV para banco de dados MySQL como fonte principal de dados, eliminando redundância e inconsistências.

---

## ✨ Mudanças Implementadas

### 1. Backend - Database Manager (`backend/database.py`)

**Novas funções adicionadas**:

- ✅ `list_servicos(limit, offset)` - Lista serviços do banco com paginação
- ✅ `get_servico_by_id(servico_id)` - Busca serviço específico por ID
- ✅ `delete_servico(servico_id)` - Deleta serviço do banco
- ✅ `update_servico(servico_id, data)` - Atualiza serviço existente
- ✅ `count_servicos()` - Conta total de serviços cadastrados

### 2. Backend API (`backend/api.py`)

**Rotas modificadas**:

| Rota Antiga | Rota Nova | Mudança |
|------------|-----------|---------|
| `GET /api/servicos` | `GET /api/servicos` | Agora lê do banco, não de CSVs |
| `GET /api/servicos/<filename>` | `GET /api/servicos/<id>` | Usa ID numérico ao invés de filename |
| `POST /api/servicos` | `POST /api/servicos` | Salva apenas no banco, não gera CSV |
| `GET /api/download/<filename>` | `GET /api/servicos/<id>/export` | Gera CSV sob demanda |
| `DELETE /api/admin/servicos/<filename>` | `DELETE /api/admin/servicos/<id>` | Deleta do banco, não arquivo |

**Mudanças de comportamento**:

- ❌ **Removido**: Salvamento automático em CSV
- ✅ **Adicionado**: Export de CSV sob demanda
- ✅ **Adicionado**: Validação de banco disponível
- ✅ **Adicionado**: Formatação de datas em respostas JSON

### 3. App Principal (`app.py`)

**Rotas modificadas**:

| Rota | Mudança |
|------|---------|
| `POST /create_service` | Salva apenas no banco, retorna `service_id` |
| `GET /vagas` | Lista vagas do banco |
| `GET /vaga/<id>` | Busca vaga por ID no banco |
| `GET /download/<id>` | Gera CSV sob demanda |
| `GET /admin` | Lista vagas do banco + contador |
| `POST /admin/delete/<id>` | Deleta do banco |

**Mudanças nos templates**:

- Variável `csv_file` substituída por `service_id`
- Variável `arquivo` substituída por `id`
- Links agora usam IDs numéricos

### 4. Script de Migração (`scripts/migrar_csv_para_banco.py`)

**Novo script criado**:

- ✅ Migra todos os CSVs existentes para o banco
- ✅ Mostra progresso e estatísticas
- ✅ Oferece opção de backup dos CSVs
- ✅ Tratamento de erros robusto

---

## 🔄 Breaking Changes

### Para o Frontend React

**Mudanças necessárias**:

1. **Listagem de serviços**:
   ```javascript
   // ANTES
   servico.arquivo  // "titulo_20241114_123456.csv"
   
   // AGORA
   servico.id  // 123
   ```

2. **Visualização de serviço**:
   ```javascript
   // ANTES
   GET /api/servicos/titulo_20241114_123456.csv
   
   // AGORA
   GET /api/servicos/123
   ```

3. **Download de CSV**:
   ```javascript
   // ANTES
   GET /api/download/titulo_20241114_123456.csv
   
   // AGORA
   GET /api/servicos/123/export
   ```

4. **Exclusão de serviço**:
   ```javascript
   // ANTES
   DELETE /api/admin/servicos/titulo_20241114_123456.csv
   
   // AGORA
   DELETE /api/admin/servicos/123
   ```

5. **Resposta de criação**:
   ```javascript
   // ANTES
   { message: "...", filename: "...", data: {...} }
   
   // AGORA
   { message: "...", id: 123, data: {...} }
   ```

### Para Templates HTML

**Mudanças necessárias**:

1. **service_success.html**:
   ```html
   <!-- ANTES -->
   {{ csv_file }}
   
   <!-- AGORA -->
   {{ service_id }}
   ```

2. **vagas_public.html**:
   ```html
   <!-- ANTES -->
   <a href="/vaga/{{ vaga.arquivo }}">
   
   <!-- AGORA -->
   <a href="/vaga/{{ vaga.id }}">
   ```

3. **admin_dashboard.html**:
   ```html
   <!-- ANTES -->
   <form action="/admin/delete/{{ vaga.arquivo }}" method="POST">
   
   <!-- AGORA -->
   <form action="/admin/delete/{{ vaga.id }}" method="POST">
   ```

4. **vaga_view.html**:
   ```html
   <!-- ANTES -->
   <a href="/download/{{ csv_file }}">
   
   <!-- AGORA -->
   <a href="/download/{{ servico_id }}">
   ```

---

## 📋 Checklist de Migração

### Backend
- [x] Adicionar funções ao `database.py`
- [x] Atualizar rotas em `backend/api.py`
- [x] Atualizar rotas em `app.py`
- [x] Criar script de migração
- [x] Atualizar documentação

### Frontend (A FAZER)
- [ ] Atualizar componente de listagem
- [ ] Atualizar componente de visualização
- [ ] Atualizar função de exclusão
- [ ] Atualizar links de download
- [ ] Testar todas as funcionalidades

### Templates HTML (A FAZER)
- [ ] Atualizar `service_success.html`
- [ ] Atualizar `vagas_public.html`
- [ ] Atualizar `vaga_view.html`
- [ ] Atualizar `admin_dashboard.html`

### Testes
- [ ] Testar criação de serviço
- [ ] Testar listagem de serviços
- [ ] Testar visualização de serviço
- [ ] Testar exclusão de serviço
- [ ] Testar export de CSV
- [ ] Testar autenticação admin

---

## 🚀 Como Migrar

### 1. Backup dos Dados

```bash
# Faça backup da pasta CSV
cp -r CSV CSV_backup_$(date +%Y%m%d)

# Faça backup do banco de dados
mysqldump -u root -p servicosmei > backup_$(date +%Y%m%d).sql
```

### 2. Execute o Script de Migração

```bash
# Ative o ambiente conda
conda activate ciclo

# Execute o script
python scripts/migrar_csv_para_banco.py
```

### 3. Atualize o Frontend

Atualize o código do frontend React conforme as mudanças listadas acima.

### 4. Atualize os Templates

Atualize os templates HTML conforme as mudanças listadas acima.

### 5. Teste Tudo

Execute testes completos de todas as funcionalidades.

---

## 📊 Benefícios

### Performance
- ✅ Queries mais rápidas
- ✅ Paginação eficiente
- ✅ Índices otimizados

### Manutenção
- ✅ Código mais limpo
- ✅ Menos redundância
- ✅ Mais fácil de debugar

### Escalabilidade
- ✅ Suporta mais registros
- ✅ Queries complexas possíveis
- ✅ Relacionamentos futuros facilitados

### Consistência
- ✅ Fonte única de verdade
- ✅ Sem dessincronia
- ✅ Integridade referencial

---

## ⚠️ Avisos Importantes

1. **Banco de dados obrigatório**: O sistema agora **requer** conexão com MySQL
2. **CSVs são opcionais**: Gerados apenas sob demanda para export
3. **IDs numéricos**: Todos os endpoints agora usam IDs ao invés de filenames
4. **Breaking changes**: Frontend precisa ser atualizado

---

## 🔙 Rollback

Se necessário reverter:

1. Restaure o backup do banco:
   ```bash
   mysql -u root -p servicosmei < backup_YYYYMMDD.sql
   ```

2. Restaure os CSVs:
   ```bash
   cp -r CSV_backup_YYYYMMDD/* CSV/
   ```

3. Faça checkout do commit anterior:
   ```bash
   git checkout <commit_anterior>
   ```

---

## 📝 Próximos Passos

1. Atualizar frontend React
2. Atualizar templates HTML
3. Adicionar testes automatizados
4. Implementar paginação no frontend
5. Adicionar filtros e busca
6. Implementar edição de serviços

---

## 👥 Suporte

Em caso de dúvidas ou problemas:
1. Verifique a documentação em `docs/`
2. Consulte o arquivo `docs/analise-duplicacao-csv-banco.md`
3. Revise os logs do servidor
