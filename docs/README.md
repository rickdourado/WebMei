# 📚 Documentação - Portal Empreendedor Unificado

**Versão Atual**: 2.0  
**Última Atualização**: 14/11/2025

---

## 🎯 Início Rápido

### Para Desenvolvedores Novos

1. **[ESTRUTURA-PROJETO.md](ESTRUTURA-PROJETO.md)** - Entenda a estrutura do projeto
2. **[estrutura-mysql.md](estrutura-mysql.md)** - Estrutura do banco de dados
3. **[TESTE-RAPIDO-V2.md](TESTE-RAPIDO-V2.md)** - Teste o sistema rapidamente

### Para Migração v1.x → v2.0

1. **[analise-duplicacao-csv-banco.md](analise-duplicacao-csv-banco.md)** - Entenda o problema
2. **[CHANGELOG-v2.0.md](CHANGELOG-v2.0.md)** - Veja todas as mudanças
3. **[INSTRUCOES-MIGRACAO.md](INSTRUCOES-MIGRACAO.md)** - Guia passo a passo
4. **[RESUMO-MUDANCAS.md](RESUMO-MUDANCAS.md)** - Resumo visual

---

## 📖 Índice Completo

### 🏗️ Arquitetura e Estrutura

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [ESTRUTURA-PROJETO.md](ESTRUTURA-PROJETO.md) | Estrutura completa do projeto | Todos |
| [estrutura-mysql.md](estrutura-mysql.md) | Schema do banco de dados MySQL | Desenvolvedores |
| [deploy-pythonanywhere.md](deploy-pythonanywhere.md) | Guia de deploy no PythonAnywhere | DevOps |

### 🔄 Migração v2.0

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [analise-duplicacao-csv-banco.md](analise-duplicacao-csv-banco.md) | Análise do problema de duplicação | Todos |
| [CHANGELOG-v2.0.md](CHANGELOG-v2.0.md) | Changelog completo da v2.0 | Desenvolvedores |
| [INSTRUCOES-MIGRACAO.md](INSTRUCOES-MIGRACAO.md) | Instruções de migração | DevOps |
| [RESUMO-MUDANCAS.md](RESUMO-MUDANCAS.md) | Resumo visual das mudanças | Todos |

### 🧪 Testes

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [TESTE-RAPIDO.md](TESTE-RAPIDO.md) | Testes rápidos v1.x (legado) | Referência |
| [TESTE-RAPIDO-V2.md](TESTE-RAPIDO-V2.md) | Testes rápidos v2.0 | Desenvolvedores |

### ✨ Features e Implementações

| Documento | Descrição | Público |
|-----------|-----------|---------|
| [dropdown-orgaos-demandantes.md](dropdown-orgaos-demandantes.md) | Implementação do dropdown de órgãos | Desenvolvedores |

---

## 🚀 Guias por Cenário

### Cenário 1: Novo Desenvolvedor

**Objetivo**: Entender e rodar o projeto

```
1. Leia: ESTRUTURA-PROJETO.md
2. Leia: estrutura-mysql.md
3. Configure o ambiente (veja .env.example)
4. Execute: python scripts/migrar_csv_para_banco.py
5. Teste: TESTE-RAPIDO-V2.md
```

### Cenário 2: Migração de v1.x para v2.0

**Objetivo**: Atualizar sistema existente

```
1. Leia: analise-duplicacao-csv-banco.md
2. Leia: CHANGELOG-v2.0.md
3. Leia: RESUMO-MUDANCAS.md
4. Siga: INSTRUCOES-MIGRACAO.md
5. Teste: TESTE-RAPIDO-V2.md
```

### Cenário 3: Deploy em Produção

**Objetivo**: Colocar sistema no ar

```
1. Leia: deploy-pythonanywhere.md
2. Configure banco de dados
3. Execute migração de dados
4. Configure variáveis de ambiente
5. Teste todas as funcionalidades
```

### Cenário 4: Adicionar Nova Feature

**Objetivo**: Implementar funcionalidade

```
1. Revise: ESTRUTURA-PROJETO.md
2. Revise: estrutura-mysql.md
3. Implemente no backend (database.py + api.py)
4. Implemente no frontend
5. Documente a mudança
6. Adicione testes
```

---

## 📊 Versões

### v2.0 (Atual) - 14/11/2025

**Mudanças principais**:
- ✅ Banco de dados como fonte única
- ✅ Eliminação de redundância CSV
- ✅ IDs numéricos ao invés de filenames
- ✅ Export CSV sob demanda
- ⚠️ Breaking changes na API

**Documentos**:
- [CHANGELOG-v2.0.md](CHANGELOG-v2.0.md)
- [INSTRUCOES-MIGRACAO.md](INSTRUCOES-MIGRACAO.md)
- [RESUMO-MUDANCAS.md](RESUMO-MUDANCAS.md)

### v1.x (Legado)

**Características**:
- Salvamento em CSV + Banco
- Leitura apenas de CSV
- Filenames como identificadores

**Documentos**:
- [TESTE-RAPIDO.md](TESTE-RAPIDO.md) (referência)

---

## 🔧 Tecnologias

### Backend
- **Flask** - Framework web Python
- **MySQL** - Banco de dados
- **PyMySQL** - Driver MySQL
- **bcrypt** - Hash de senhas
- **python-dotenv** - Variáveis de ambiente

### Frontend
- **React** - Biblioteca UI
- **Vite** - Build tool
- **React Router** - Roteamento
- **Axios** - Cliente HTTP

### DevOps
- **Conda** - Gerenciador de ambientes
- **Git** - Controle de versão
- **PythonAnywhere** - Hospedagem (opcional)

---

## 📁 Estrutura de Arquivos

```
docs/
├── README.md                              ← Você está aqui
├── ESTRUTURA-PROJETO.md                   ← Estrutura do projeto
├── estrutura-mysql.md                     ← Schema do banco
├── deploy-pythonanywhere.md               ← Deploy
├── analise-duplicacao-csv-banco.md        ← Análise v2.0
├── CHANGELOG-v2.0.md                      ← Changelog v2.0
├── INSTRUCOES-MIGRACAO.md                 ← Migração v2.0
├── RESUMO-MUDANCAS.md                     ← Resumo v2.0
├── TESTE-RAPIDO.md                        ← Testes v1.x
├── TESTE-RAPIDO-V2.md                     ← Testes v2.0
└── dropdown-orgaos-demandantes.md         ← Feature dropdown
```

---

## 🎯 Roadmap

### Concluído ✅
- [x] Sistema básico de cadastro
- [x] Autenticação admin
- [x] Dropdown de órgãos
- [x] Integração com MySQL
- [x] Migração para banco como fonte única
- [x] Export CSV sob demanda

### Em Desenvolvimento 🚧
- [ ] Atualização do frontend React
- [ ] Atualização dos templates HTML
- [ ] Testes automatizados

### Planejado 📋
- [ ] Paginação
- [ ] Filtros e busca
- [ ] Edição de serviços
- [ ] Histórico de alterações
- [ ] Dashboard com estatísticas
- [ ] API de notificações
- [ ] Sistema de permissões

---

## 🤝 Contribuindo

### Padrões de Código

1. **Python**: PEP 8
2. **JavaScript**: ESLint
3. **Commits**: Conventional Commits
4. **Branches**: GitFlow

### Processo

1. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
2. Implemente a funcionalidade
3. Adicione testes
4. Atualize a documentação
5. Faça commit: `git commit -m "feat: adiciona nova funcionalidade"`
6. Push: `git push origin feature/nova-funcionalidade`
7. Abra um Pull Request

### Documentação

Ao adicionar features:
1. Atualize `ESTRUTURA-PROJETO.md` se necessário
2. Crie documento específico em `docs/`
3. Atualize este README.md
4. Adicione exemplos de uso

---

## 📞 Suporte

### Problemas Comuns

1. **Banco não conecta**: Verifique `.env` e MySQL
2. **API não responde**: Verifique se o backend está rodando
3. **Frontend não carrega**: Verifique se o Vite está rodando
4. **Erro 401**: Faça login primeiro

### Recursos

- **Documentação**: `docs/`
- **Issues**: GitHub Issues
- **Logs**: Console do servidor

---

## 📜 Licença

[Adicionar informações de licença]

---

## 👥 Equipe

[Adicionar informações da equipe]

---

## 📝 Notas de Versão

### v2.0.0 - 14/11/2025

**Breaking Changes**:
- Sistema agora requer MySQL
- Endpoints usam IDs ao invés de filenames
- CSVs gerados sob demanda

**Melhorias**:
- Performance 3x melhor
- Consistência de dados garantida
- Código mais limpo e manutenível

**Migração**:
- Siga `INSTRUCOES-MIGRACAO.md`
- Execute `scripts/migrar_csv_para_banco.py`
- Atualize frontend conforme `CHANGELOG-v2.0.md`

---

**Última atualização**: 14/11/2025  
**Versão da documentação**: 2.0
