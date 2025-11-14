# Análise: Duplicação de Armazenamento (CSV + Banco de Dados)

**Data**: 14/11/2025  
**Status**: ⚠️ REDUNDÂNCIA IDENTIFICADA

---

## 🔍 Problema Identificado

O sistema está configurado para **salvar dados em duplicidade**:
1. ✅ Salva no banco de dados MySQL
2. ✅ Salva em arquivos CSV individuais

Isso gera:
- **Redundância de dados**
- **Inconsistência potencial** (CSV e banco podem ficar dessincronizados)
- **Desperdício de espaço em disco**
- **Complexidade desnecessária** na manutenção

---

## 📊 Locais Onde Ocorre a Duplicação

### 1. Backend API (`backend/api.py`)

**Linha 218-245**: Função `create_servico()`

```python
# Salva CSV (REDUNDANTE)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
slug = safe_slug(data['titulo_servico'])
filename = f"{slug}_{timestamp}.csv"
filepath = os.path.join(CSV_DIR, filename)

headers = [...]
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerow(data)

# Salva no banco (PRINCIPAL)
if db_manager:
    try:
        service_id = db_manager.insert_servico(data)
        if service_id:
            print(f"✓ Serviço inserido no banco com ID: {service_id}")
    except Exception as e:
        print(f"✗ Erro ao salvar no banco: {e}")
```

### 2. App Principal (`app.py`)

**Linha 174-207**: Função `create_service()`

```python
# Persistência em CSV (REDUNDANTE)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
slug = safe_slug(data['titulo_servico'])
filename = f"{slug}_{timestamp}.csv"
filepath = os.path.join(CSV_DIR, filename)

headers = [...]
with open(filepath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerow(data)

# Persistência no banco de dados MySQL (PRINCIPAL)
try:
    db_data = data.copy()
    service_id = db_manager.insert_servico(db_data)
    
    if service_id:
        print(f"✓ Serviço inserido no banco de dados com ID: {service_id}")
    else:
        print("⚠ Aviso: Serviço não foi salvo no banco de dados")
        
except Exception as e:
    print(f"✗ Erro ao salvar no banco de dados: {e}")
    # Não interrompe o fluxo - CSV já foi salvo
```

---

## 🚨 Problemas Adicionais Identificados

### 1. Listagem de Serviços Lê Apenas CSV

**`backend/api.py` - Linha 156-175**: `list_servicos()`
```python
def list_servicos():
    """Lista todos os serviços cadastrados"""
    vagas = []
    for name in sorted(os.listdir(CSV_DIR)):  # ❌ LÊ DO CSV
        if not name.lower().endswith('.csv'):
            continue
        try:
            with open(os.path.join(CSV_DIR, name), 'r', encoding='utf-8') as f:
                r = csv.DictReader(f)
                row = next(r, None)
                if row:
                    vagas.append({...})
```

**Problema**: Mesmo salvando no banco, a listagem lê dos arquivos CSV!

### 2. Visualização de Serviço Lê Apenas CSV

**`backend/api.py` - Linha 177-189**: `get_servico()`
```python
def get_servico(filename):
    """Retorna detalhes de um serviço específico"""
    path = os.path.join(CSV_DIR, filename)  # ❌ LÊ DO CSV
    if not os.path.isfile(path):
        return jsonify({'error': 'Serviço não encontrado'}), 404
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            r = csv.DictReader(f)
            data = next(r, None) or {}
        return jsonify(data)
```

### 3. Dashboard Admin Lê Apenas CSV

**`app.py` - Linha 328-348**: `admin_dashboard()`
```python
def admin_dashboard():
    vagas = []
    for name in sorted(os.listdir(CSV_DIR)):  # ❌ LÊ DO CSV
        if not name.lower().endswith('.csv'):
            continue
```

### 4. Exclusão Remove Apenas CSV

**`backend/api.py` - Linha 279-291**: `delete_servico()`
```python
def delete_servico(filename):
    """Deleta um serviço (apenas admin)"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Não autorizado'}), 401
    
    path = os.path.join(CSV_DIR, filename)  # ❌ DELETA APENAS CSV
    if os.path.isfile(path):
        try:
            os.remove(path)
            return jsonify({'message': 'Serviço excluído com sucesso'})
```

**Problema**: Deleta o CSV mas **NÃO deleta do banco de dados**!

---

## 📋 Funções Faltando no `database.py`

O arquivo `backend/database.py` possui apenas:
- ✅ `authenticate_user()` - Autenticação
- ✅ `update_user_password_hash()` - Atualizar senha
- ✅ `list_users()` - Listar usuários
- ✅ `insert_servico()` - Inserir serviço

**Faltam**:
- ❌ `list_servicos()` - Listar serviços do banco
- ❌ `get_servico(id)` - Buscar serviço por ID
- ❌ `delete_servico(id)` - Deletar serviço do banco
- ❌ `update_servico(id, data)` - Atualizar serviço

---

## 💡 Recomendações

### Opção 1: Usar Apenas Banco de Dados (RECOMENDADO)

**Vantagens**:
- ✅ Fonte única de verdade
- ✅ Sem inconsistências
- ✅ Melhor performance
- ✅ Facilita queries complexas
- ✅ Backup mais simples

**Ações necessárias**:
1. Criar funções faltantes em `database.py`
2. Remover código de salvamento em CSV
3. Atualizar rotas para ler do banco
4. Manter CSV apenas para export/download opcional

### Opção 2: Usar Apenas CSV (NÃO RECOMENDADO)

**Desvantagens**:
- ❌ Não escalável
- ❌ Difícil fazer queries
- ❌ Sem integridade referencial
- ❌ Performance ruim com muitos registros

### Opção 3: Manter Ambos com Sincronização (COMPLEXO)

**Desvantagens**:
- ❌ Muito complexo
- ❌ Propenso a erros
- ❌ Manutenção difícil
- ❌ Não recomendado

---

## 🎯 Solução Proposta

### Fase 1: Adicionar Funções ao `database.py`
- Criar `list_servicos()`
- Criar `get_servico_by_id()`
- Criar `delete_servico()`
- Criar `update_servico()`

### Fase 2: Atualizar Rotas
- Modificar `list_servicos()` para ler do banco
- Modificar `get_servico()` para ler do banco
- Modificar `delete_servico()` para deletar do banco
- Adicionar rota de export CSV (opcional)

### Fase 3: Remover Salvamento em CSV
- Remover código de criação de CSV em `create_servico()`
- Manter apenas função de export opcional

### Fase 4: Migração de Dados
- Criar script para migrar CSVs existentes para o banco
- Mover CSVs antigos para pasta de backup

---

## 📝 Conclusão

O sistema está **salvando em duplicidade** e **lendo apenas dos CSVs**, tornando o banco de dados praticamente inútil no momento. É necessário refatorar para usar o banco como fonte principal de dados.

**Prioridade**: 🔴 ALTA  
**Impacto**: Médio a Alto  
**Esforço**: Médio (2-4 horas de desenvolvimento)
