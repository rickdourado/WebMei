# Estrutura de Banco de Dados MySQL - Portal Empreendedor

## Visão Geral

Este documento especifica a estrutura de banco de dados MySQL para migração do sistema atual (baseado em CSV) para um banco de dados relacional. A estrutura foi baseada na análise do formulário `templates/index.html`.

## Tabela Principal: `servicos_mei`

### Descrição
Tabela principal para armazenar todas as oportunidades de serviços para MEI cadastradas no sistema.

### Estrutura SQL

```sql
CREATE TABLE servicos_mei (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orgao_demandante VARCHAR(255) NOT NULL COMMENT 'Órgão que está demandando o serviço',
    titulo_servico VARCHAR(255) NOT NULL COMMENT 'Título/nome do serviço',
    tipo_atividade VARCHAR(100) NULL COMMENT 'Categoria/tipo da atividade',
    especificacao_atividade VARCHAR(255) NOT NULL COMMENT 'Especificação detalhada da atividade',
    descricao_servico TEXT NOT NULL COMMENT 'Descrição completa do serviço',
    outras_informacoes TEXT NULL COMMENT 'Informações adicionais opcionais',
    endereco VARCHAR(255) NOT NULL COMMENT 'Endereço onde o serviço será executado',
    numero VARCHAR(20) NOT NULL COMMENT 'Número do endereço',
    bairro VARCHAR(100) NOT NULL COMMENT 'Bairro do endereço',
    forma_pagamento ENUM('Cheque', 'Dinheiro', 'Cartão', 'Transferência') NOT NULL COMMENT 'Forma de pagamento',
    prazo_pagamento VARCHAR(100) NOT NULL COMMENT 'Prazo para pagamento (ex: 30 dias)',
    prazo_expiracao DATE NOT NULL COMMENT 'Data de expiração da oportunidade',
    data_limite_execucao DATE NOT NULL COMMENT 'Data limite para execução do serviço',
    arquivo_csv VARCHAR(255) NULL COMMENT 'Nome do arquivo CSV original (para compatibilidade)',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação do registro',
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data da última atualização',
    ativo BOOLEAN DEFAULT TRUE COMMENT 'Indica se o serviço está ativo/disponível',
    
    -- Índices para melhor performance
    INDEX idx_orgao_demandante (orgao_demandante),
    INDEX idx_tipo_atividade (tipo_atividade),
    INDEX idx_bairro (bairro),
    INDEX idx_prazo_expiracao (prazo_expiracao),
    INDEX idx_data_limite_execucao (data_limite_execucao),
    INDEX idx_ativo (ativo),
    INDEX idx_data_criacao (data_criacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela para armazenar oportunidades de serviços para MEI';
```

### Campos Detalhados

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | INT AUTO_INCREMENT | Sim | Chave primária única |
| `orgao_demandante` | VARCHAR(255) | Sim | Nome do órgão que demanda o serviço |
| `titulo_servico` | VARCHAR(255) | Sim | Título/nome do serviço oferecido |
| `tipo_atividade` | VARCHAR(100) | Não | Categoria geral da atividade |
| `especificacao_atividade` | VARCHAR(255) | Sim | Especificação detalhada da atividade |
| `descricao_servico` | TEXT | Sim | Descrição completa do serviço |
| `outras_informacoes` | TEXT | Não | Informações adicionais opcionais |
| `endereco` | VARCHAR(255) | Sim | Endereço de execução do serviço |
| `numero` | VARCHAR(20) | Sim | Número do endereço |
| `bairro` | VARCHAR(100) | Sim | Bairro do endereço |
| `forma_pagamento` | ENUM | Sim | Forma de pagamento (Cheque, Dinheiro, Cartão, Transferência) |
| `prazo_pagamento` | VARCHAR(100) | Sim | Prazo para pagamento |
| `prazo_expiracao` | DATE | Sim | Data de expiração da oportunidade |
| `data_limite_execucao` | DATE | Sim | Data limite para execução |
| `arquivo_csv` | VARCHAR(255) | Não | Nome do arquivo CSV original (compatibilidade) |
| `data_criacao` | TIMESTAMP | Automático | Data de criação do registro |
| `data_atualizacao` | TIMESTAMP | Automático | Data da última atualização |
| `ativo` | BOOLEAN | Padrão: TRUE | Status ativo/inativo do serviço |

## Tabelas Auxiliares (Opcionais)

### Tabela: `tipos_atividade`

Para normalização e controle dos tipos de atividade disponíveis.

```sql
CREATE TABLE tipos_atividade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Tabela: `especificacoes_atividade`

Para normalização das especificações de atividade vinculadas aos tipos.

```sql
CREATE TABLE especificacoes_atividade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_atividade_id INT,
    nome VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_atividade_id) REFERENCES tipos_atividade(id) ON DELETE SET NULL,
    INDEX idx_tipo_atividade (tipo_atividade_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Considerações Técnicas

### Charset e Collation
- **Charset**: `utf8mb4` - Suporte completo a caracteres Unicode
- **Collation**: `utf8mb4_unicode_ci` - Comparação case-insensitive com suporte a acentos

### Engine
- **InnoDB**: Escolhido por suportar transações, chaves estrangeiras e melhor performance para aplicações web

### Índices
Os índices foram criados nos campos mais utilizados para consultas:
- Órgão demandante (filtros administrativos)
- Tipo de atividade (filtros públicos)
- Bairro (filtros geográficos)
- Datas (filtros temporais)
- Status ativo (performance geral)

### Campos de Auditoria
- `data_criacao`: Timestamp automático na inserção
- `data_atualizacao`: Timestamp automático na atualização
- `ativo`: Para soft delete (não remove fisicamente os registros)

## Migração do Sistema Atual

### Estratégia de Migração
1. **Fase 1**: Criar estrutura do banco
2. **Fase 2**: Script de migração dos CSVs existentes
3. **Fase 3**: Atualizar aplicação Flask para usar MySQL
4. **Fase 4**: Manter compatibilidade temporária com CSVs

### Script de Migração (Sugestão)
```python
# Exemplo de script para migrar CSVs existentes
import csv
import mysql.connector
from datetime import datetime
import os

def migrar_csvs_para_mysql():
    # Conectar ao banco
    conn = mysql.connector.connect(
        host='localhost',
        user='seu_usuario',
        password='sua_senha',
        database='portal_empreendedor'
    )
    
    # Processar arquivos CSV da pasta CSV/
    csv_folder = 'CSV/'
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            # Lógica de migração aqui
            pass
```

## Consultas Úteis

### Listar serviços ativos por bairro
```sql
SELECT * FROM servicos_mei 
WHERE ativo = TRUE AND bairro = 'Centro' 
ORDER BY data_criacao DESC;
```

### Serviços próximos ao vencimento
```sql
SELECT * FROM servicos_mei 
WHERE ativo = TRUE 
AND prazo_expiracao BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY prazo_expiracao ASC;
```

### Estatísticas por órgão
```sql
SELECT orgao_demandante, COUNT(*) as total_servicos
FROM servicos_mei 
WHERE ativo = TRUE 
GROUP BY orgao_demandante 
ORDER BY total_servicos DESC;
```

## Próximos Passos

1. **Criar banco de dados**: `CREATE DATABASE portal_empreendedor;`
2. **Executar scripts de criação das tabelas**
3. **Desenvolver script de migração dos dados existentes**
4. **Atualizar código Flask para usar MySQL em vez de CSV**
5. **Implementar testes para validar a migração**
6. **Documentar novas procedures e queries**

---

**Data de criação**: {{ data_atual }}  
**Versão**: 1.0  
**Autor**: Sistema Portal Empreendedor