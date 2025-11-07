# Testes de Integração Formulário → Banco de Dados

## Resumo dos Testes Realizados

Este documento descreve os testes realizados para validar a integração entre o formulário web e a tabela `servicos_mei` no banco de dados MySQL.

## Scripts de Teste Criados

### 1. `test_form_to_database.py`
**Objetivo**: Testar conexão básica e estrutura do banco de dados

**O que testa**:
- ✅ Conexão com banco de dados MySQL
- ✅ Existência da tabela `servicos_mei`
- ✅ Estrutura da tabela (campos e tipos)
- ✅ Inserção de registro de teste
- ✅ Verificação de dados inseridos
- ✅ Contagem de serviços

**Como executar**:
```bash
conda activate ciclo
python scripts/test_form_to_database.py
```

**Resultado esperado**: Todos os 5 testes devem passar

---

### 2. `test_manual_form_insert.py`
**Objetivo**: Simular inserção de múltiplos serviços como se viessem do formulário

**O que testa**:
- ✅ Inserção de 3 serviços diferentes
- ✅ Listagem de todos os serviços cadastrados
- ✅ Estatísticas (total, por forma de pagamento, por bairro)
- ✅ Validação de campos obrigatórios
- ✅ Formatação de datas

**Como executar**:
```bash
conda activate ciclo
python scripts/test_manual_form_insert.py
```

**Resultado esperado**: 3 novos serviços inseridos + listagem completa + estatísticas

---

### 3. `test_web_form_integration.py`
**Objetivo**: Testar integração completa do formulário web Flask

**O que testa**:
- ✅ Submissão de formulário via Flask test client
- ✅ Processamento da rota `/create_service`
- ✅ Criação de arquivo CSV
- ⚠️ Verificação de salvamento no banco (pendente de implementação)

**Como executar**:
```bash
conda activate ciclo
python scripts/test_web_form_integration.py
```

**Status atual**: Formulário funciona e salva em CSV, mas ainda não salva no MySQL

---

## Resultados dos Testes

### ✅ Testes que Passaram

1. **Conexão com Banco de Dados**: OK
   - Banco: `servicosmei`
   - Host: configurado via `.env`

2. **Estrutura da Tabela**: OK
   - 18 campos criados corretamente
   - Tipos de dados adequados
   - Índices configurados

3. **Inserção de Dados**: OK
   - 4 serviços de teste inseridos com sucesso
   - IDs gerados automaticamente
   - Timestamps automáticos funcionando

4. **Consultas e Listagens**: OK
   - Busca por ID
   - Listagem completa
   - Filtros por status, bairro, forma de pagamento

### ⚠️ Pendente de Implementação

**Integração do Formulário Web com MySQL**

Atualmente o formulário:
- ✅ Coleta dados do usuário
- ✅ Valida campos obrigatórios
- ✅ Salva em arquivo CSV
- ❌ **NÃO salva no banco de dados MySQL**

---

## Como Integrar o Formulário com o Banco

### Passo 1: Adicionar método no DatabaseManager

Edite `database.py` e adicione:

```python
def insert_servico(self, data):
    """
    Insere um novo serviço na tabela servicos_mei
    
    Args:
        data (dict): Dicionário com os dados do serviço
        
    Returns:
        int: ID do serviço inserido ou None em caso de erro
    """
    try:
        connection = self.get_connection()
        
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO servicos_mei (
                    orgao_demandante, titulo_servico, tipo_atividade, 
                    especificacao_atividade, descricao_servico, outras_informacoes,
                    endereco, numero, bairro, forma_pagamento, prazo_pagamento,
                    prazo_expiracao, data_limite_execucao, arquivo_csv
                ) VALUES (
                    %(orgao_demandante)s, %(titulo_servico)s, %(tipo_atividade)s,
                    %(especificacao_atividade)s, %(descricao_servico)s, %(outras_informacoes)s,
                    %(endereco)s, %(numero)s, %(bairro)s, %(forma_pagamento)s, %(prazo_pagamento)s,
                    %(prazo_expiracao)s, %(data_limite_execucao)s, %(arquivo_csv)s
                )
            """
            
            cursor.execute(sql, data)
            connection.commit()
            
            return cursor.lastrowid
            
    except Exception as e:
        print(f"Erro ao inserir serviço: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()
```

### Passo 2: Modificar a rota /create_service

Edite `app.py` na rota `/create_service`, após salvar o CSV:

```python
@app.route('/create_service', methods=['POST'])
def create_service():
    # ... código existente de validação ...
    
    # Salva em CSV (código existente)
    # ... código do CSV ...
    
    # ADICIONAR: Salva no banco de dados MySQL
    try:
        # Converte prazo_expiracao de DD/MM/AAAA para YYYY-MM-DD
        prazo_exp_parts = data['prazo_expiracao'].split('/')
        if len(prazo_exp_parts) == 3:
            prazo_exp_mysql = f"{prazo_exp_parts[2]}-{prazo_exp_parts[1]}-{prazo_exp_parts[0]}"
        else:
            prazo_exp_mysql = data['prazo_expiracao']
        
        # Prepara dados para o banco
        db_data = data.copy()
        db_data['prazo_expiracao'] = prazo_exp_mysql
        db_data['arquivo_csv'] = filename
        
        # Insere no banco
        service_id = db_manager.insert_servico(db_data)
        
        if service_id:
            print(f"Serviço inserido no banco com ID: {service_id}")
        else:
            print("Aviso: Serviço não foi salvo no banco de dados")
            
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        # Não interrompe o fluxo - CSV já foi salvo
    
    flash('Serviço cadastrado com sucesso!', 'success')
    return render_template('service_success.html', data=data, csv_file=filename)
```

### Passo 3: Atualizar listagens para usar MySQL

Modifique as rotas de listagem (`/vagas`, `/admin`) para buscar do banco:

```python
@app.route('/vagas')
def vagas_public():
    try:
        conn = db_manager.get_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    id, titulo_servico, tipo_atividade, bairro, 
                    prazo_expiracao, arquivo_csv
                FROM servicos_mei 
                WHERE ativo = TRUE 
                ORDER BY data_criacao DESC
            """)
            vagas = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Erro ao buscar vagas: {e}")
        vagas = []
    
    return render_template('vagas_public.html', vagas=vagas)
```

---

## Verificação Final

Após implementar as mudanças:

1. **Teste o formulário web**:
   ```bash
   conda activate ciclo
   python app.py
   ```
   Acesse: http://localhost:5010

2. **Preencha o formulário** com dados de teste

3. **Verifique no banco**:
   ```bash
   python scripts/test_form_to_database.py
   ```

4. **Confirme que os dados aparecem** tanto em CSV quanto no MySQL

---

## Estrutura de Dados

### Campos do Formulário → Tabela MySQL

| Campo Formulário | Campo MySQL | Tipo | Observações |
|------------------|-------------|------|-------------|
| orgao_demandante | orgao_demandante | VARCHAR(255) | Obrigatório |
| titulo_servico | titulo_servico | VARCHAR(255) | Obrigatório |
| tipo_atividade | tipo_atividade | VARCHAR(100) | Opcional |
| especificacao_atividade | especificacao_atividade | VARCHAR(255) | Obrigatório |
| descricao_servico | descricao_servico | TEXT | Obrigatório |
| outras_informacoes | outras_informacoes | TEXT | Opcional |
| endereco | endereco | VARCHAR(255) | Obrigatório |
| numero | numero | VARCHAR(20) | Obrigatório |
| bairro | bairro | VARCHAR(100) | Obrigatório |
| forma_pagamento | forma_pagamento | ENUM | Obrigatório |
| prazo_pagamento | prazo_pagamento | VARCHAR(100) | Obrigatório |
| prazo_expiracao | prazo_expiracao | DATE | Converter DD/MM/AAAA → YYYY-MM-DD |
| data_limite_execucao | data_limite_execucao | DATE | Já vem em YYYY-MM-DD |
| - | arquivo_csv | VARCHAR(255) | Nome do CSV gerado |
| - | data_criacao | TIMESTAMP | Automático |
| - | data_atualizacao | TIMESTAMP | Automático |
| - | ativo | BOOLEAN | Padrão: TRUE |

---

## Comandos Úteis

### Verificar dados no banco via MySQL CLI
```bash
mysql -u root -p servicosmei
```

```sql
-- Ver todos os serviços
SELECT id, titulo_servico, bairro, data_criacao FROM servicos_mei;

-- Ver serviços ativos
SELECT * FROM servicos_mei WHERE ativo = TRUE;

-- Contar por bairro
SELECT bairro, COUNT(*) as total FROM servicos_mei GROUP BY bairro;

-- Limpar dados de teste
DELETE FROM servicos_mei WHERE titulo_servico LIKE '%Teste%';
```

### Executar todos os testes
```bash
conda activate ciclo
python scripts/test_form_to_database.py
python scripts/test_manual_form_insert.py
```

---

## Conclusão

✅ **Testes Realizados com Sucesso**:
- Conexão com banco de dados
- Estrutura da tabela validada
- Inserção de dados funcionando
- Consultas e listagens operacionais

⚠️ **Próximo Passo**:
- Integrar a rota `/create_service` para salvar no MySQL
- Atualizar rotas de listagem para buscar do banco
- Manter compatibilidade com CSV durante transição

📊 **Status Atual**:
- 4 serviços de teste inseridos no banco
- Tabela `servicos_mei` 100% funcional
- Scripts de teste prontos para validação contínua

---

**Data**: 07/11/2025  
**Ambiente**: conda ciclo  
**Banco**: servicosmei (MySQL)
