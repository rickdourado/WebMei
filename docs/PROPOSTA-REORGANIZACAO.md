# Proposta de Reorganização da Documentação

## Problema Atual
A pasta `docs/` contém 23 arquivos markdown sem uma estrutura clara, dificultando a navegação e manutenção.

## Estrutura Proposta

```
docs/
├── README.md                          # Índice principal
│
├── 01-inicio/                         # Documentação inicial
│   ├── INSTALACAO-RAPIDA.md
│   ├── GUIA-RAPIDO-REACT.md
│   └── ESTRUTURA-PROJETO.md
│
├── 02-desenvolvimento/                # Guias de desenvolvimento
│   ├── IDENTIDADE-VISUAL.md
│   ├── TEMPLATES-ESTRUTURA.md
│   └── estrutura-mysql.md
│
├── 03-features/                       # Documentação de funcionalidades
│   ├── dropdown-orgaos-demandantes.md
│   ├── campo-numero-corrigido.md
│   ├── campo-prazo-expiracao-calendario.md
│   ├── integracao-formulario-mysql.md
│   └── hash-senhas/
│       ├── como-funciona-hash-bcrypt.md
│       ├── hash-senhas-explicacao.md
│       └── migracao-senhas-hash.md
│
├── 04-migracao/                       # Documentação de migração
│   ├── RESUMO-MIGRACAO.md
│   ├── INSTRUCOES-MIGRACAO.md
│   ├── COMPARACAO-VERSOES.md
│   ├── analise-duplicacao-csv-banco.md
│   └── README-REACT.md
│
├── 05-versoes/                        # Changelogs e versões
│   ├── CHANGELOG-v2.0.md
│   ├── IMPLEMENTACAO-COMPLETA.md
│   └── changelogs/
│       ├── 2025-11-14.md
│       └── 2025-11-15.md
│
├── 06-deploy/                         # Documentação de deploy
│   └── deploy-pythonanywhere.md
│
└── 07-atual/                          # Estado atual do projeto
    └── RESUMO-MUDANCAS.md             # Sempre o mais recente
```

## Benefícios

1. **Navegação Intuitiva**: Estrutura numerada facilita encontrar documentos
2. **Separação por Contexto**: Cada pasta agrupa documentos relacionados
3. **Histórico Preservado**: Changelogs mantidos em subpasta dedicada
4. **Fácil Manutenção**: Novos documentos têm local claro
5. **Onboarding Simplificado**: Novos desenvolvedores seguem ordem numérica

## Mapeamento de Arquivos

### 01-inicio/ (3 arquivos)
- INSTALACAO-RAPIDA.md
- GUIA-RAPIDO-REACT.md
- ESTRUTURA-PROJETO.md

### 02-desenvolvimento/ (3 arquivos)
- IDENTIDADE-VISUAL.md
- TEMPLATES-ESTRUTURA.md
- estrutura-mysql.md

### 03-features/ (7 arquivos)
- dropdown-orgaos-demandantes.md
- campo-numero-corrigido.md
- campo-prazo-expiracao-calendario.md
- integracao-formulario-mysql.md
- hash-senhas/
  - como-funciona-hash-bcrypt.md
  - hash-senhas-explicacao.md
  - migracao-senhas-hash.md

### 04-migracao/ (5 arquivos)
- RESUMO-MIGRACAO.md
- INSTRUCOES-MIGRACAO.md
- COMPARACAO-VERSOES.md
- analise-duplicacao-csv-banco.md
- README-REACT.md

### 05-versoes/ (4 arquivos)
- CHANGELOG-v2.0.md
- IMPLEMENTACAO-COMPLETA.md
- changelogs/
  - 2025-11-14.md
  - 2025-11-15.md

### 06-deploy/ (1 arquivo)
- deploy-pythonanywhere.md

### 07-atual/ (1 arquivo)
- RESUMO-MUDANCAS.md

## Novo README.md Principal

Criar um índice visual com links diretos para cada seção, facilitando navegação.

## Implementação

Executar script de reorganização que:
1. Cria estrutura de pastas
2. Move arquivos para locais apropriados
3. Atualiza links internos
4. Cria novo README.md
5. Mantém histórico git
