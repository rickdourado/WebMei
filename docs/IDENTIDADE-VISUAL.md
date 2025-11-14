# 🎨 Identidade Visual - Portal Empreendedor React

## Visão Geral

A identidade visual do React foi alinhada com os templates originais do Flask, mantendo a consistência da marca "Oportunidades Cariocas — Ciclo Carioca".

---

## 🎨 Paleta de Cores

### Cores Principais
```css
/* Gradiente de fundo */
background: linear-gradient(135deg, #003399 0%, #0066cc 100%);

/* Gradiente dos botões */
background: linear-gradient(135deg, #667eea, #764ba2);

/* Texto principal */
color: #2d3748;

/* Bordas */
border-color: #e2e8f0;
```

### Cores de Estado
```css
/* Sucesso */
background: #f0fff4;
color: #22543d;
border: #9ae6b4;

/* Erro */
background: #fed7d7;
color: #742a2a;
border: #e53e3e;

/* Info */
background: #e6f7ff;
color: #003a8c;
border: #91d5ff;
```

---

## 🖼️ Componentes Visuais

### Header
```
┌─────────────────────────────────────────────────────┐
│ [Logo] Oportunidades Cariocas — Título    [🏠][Vagas][Admin] │
└─────────────────────────────────────────────────────┘
```

**Características:**
- Fundo branco translúcido com blur
- Logo do Ciclo Carioca (75px altura)
- Título em negrito (1.6rem)
- Botões com gradiente roxo/azul
- Ícone de home com Font Awesome

### Cards de Vagas
```
┌──────────────────────────┐
│ Título da Vaga           │
│                          │
│ Tipo: Construção         │
│ Bairro: Centro           │
│ Expira: 31/12/2024       │
│                          │
│ [Ver Detalhes]           │
└──────────────────────────┘
```

**Características:**
- Borda 2px sólida
- Border-radius 12px
- Hover: elevação e borda colorida
- Botão com gradiente

### Formulários
```
┌─────────────────────────────────┐
│ Label *                         │
│ ┌─────────────────────────────┐ │
│ │ Input field                 │ │
│ └─────────────────────────────┘ │
│ Texto de ajuda                  │
└─────────────────────────────────┘
```

**Características:**
- Inputs com padding 12px 16px
- Border 2px sólida
- Focus: borda roxa + shadow
- Border-radius 8px

---

## 📐 Tipografia

### Fonte
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Tamanhos
- **Título principal**: 1.6rem (logo-title)
- **Subtítulos**: 1.2rem (h2)
- **Texto normal**: 1rem
- **Texto pequeno**: 0.85em
- **Botões**: 0.9rem

### Pesos
- **Normal**: 400
- **Médio**: 500
- **Semibold**: 600
- **Bold**: 700

---

## 🎭 Efeitos Visuais

### Glassmorphism
```css
background: rgba(255, 255, 255, 0.95);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.2);
```

Aplicado em:
- Header
- Main content
- Cards

### Hover Effects
```css
/* Botões */
transform: translateY(-1px);
box-shadow: 0 6px 18px rgba(102, 126, 234, 0.25);

/* Cards */
transform: translateY(-2px);
box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
border-color: #667eea;
```

### Animações
```css
/* Fade in ao carregar */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 🔘 Botões

### Primário (Gradiente)
```css
background: linear-gradient(135deg, #667eea, #764ba2);
color: #fff;
padding: 12px 20px;
border-radius: 8px;
font-weight: 600;
```

**Uso**: Ações principais (Cadastrar, Entrar, Ver Detalhes)

### Secundário (Verde)
```css
background: linear-gradient(135deg, #48bb78, #38a169);
```

**Uso**: Download de CSV

### Perigo (Vermelho)
```css
background: linear-gradient(135deg, #fc8181, #f56565);
```

**Uso**: Excluir vaga

---

## 📱 Responsividade

### Breakpoints
```css
@media (max-width: 768px) {
  /* Mobile */
  .form-grid { grid-template-columns: 1fr; }
  .header-content { flex-direction: column; }
  .logo-title { font-size: 1.2rem; }
}
```

### Ajustes Mobile
- Grid de formulário: 1 coluna
- Header: layout vertical
- Logo: tamanho reduzido
- Navegação: centralizada
- Tabelas: scroll horizontal

---

## 🎯 Componentes Criados

### Header Component
```jsx
<Header 
  title="Título da Página"
  showAdmin={true}
  showLogout={false}
  onLogout={handleLogout}
/>
```

**Props:**
- `title`: Texto após "Oportunidades Cariocas —"
- `showAdmin`: Mostrar botão Admin
- `showLogout`: Mostrar botão Sair
- `onLogout`: Função de logout

---

## 🖼️ Assets

### Logo
**Localização**: `frontend/public/logo_ciclocarioca.png`

**Especificações**:
- Altura máxima: 75px
- Formato: PNG com transparência
- Fallback: Oculta automaticamente se não encontrado

### Ícones
**Font Awesome 6.0.0**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

**Ícones usados**:
- `fa-home` - Página inicial
- `fa-sign-out-alt` - Logout

---

## 📋 Checklist de Consistência Visual

Ao criar novos componentes, verificar:

- [ ] Usa fonte Inter
- [ ] Fundo com gradiente azul
- [ ] Cards com glassmorphism
- [ ] Botões com gradiente
- [ ] Border-radius 8px ou 12px
- [ ] Hover effects com transform
- [ ] Focus com outline roxa
- [ ] Responsivo (mobile-first)
- [ ] Animação fadeIn
- [ ] Cores da paleta oficial

---

## 🎨 Comparação Visual

### Antes (Estilo Genérico)
```
┌─────────────────────────┐
│ Header (branco sólido)  │
└─────────────────────────┘
  Fundo cinza (#f5f5f5)
┌─────────────────────────┐
│ Card (branco sólido)    │
│ Borda fina              │
│ [Botão azul simples]    │
└─────────────────────────┘
```

### Depois (Ciclo Carioca)
```
╔═════════════════════════╗
║ Header (glass effect)   ║
╚═════════════════════════╝
  Gradiente azul (#003399 → #0066cc)
╔═════════════════════════╗
║ Card (glass effect)     ║
║ Borda 2px colorida      ║
║ [Botão gradiente]       ║
╚═════════════════════════╝
```

---

## 🔧 Customização

### Alterar Cores Principais
```css
/* frontend/src/App.css */

/* Gradiente de fundo */
body {
  background: linear-gradient(135deg, #SUA_COR_1, #SUA_COR_2);
}

/* Gradiente dos botões */
nav a, button[type="submit"] {
  background: linear-gradient(135deg, #SUA_COR_3, #SUA_COR_4);
}
```

### Alterar Logo
1. Substituir `frontend/public/logo_ciclocarioca.png`
2. Ajustar altura em `Header.jsx` se necessário

### Alterar Fonte
```html
<!-- frontend/index.html -->
<link href="https://fonts.googleapis.com/css2?family=SUA_FONTE:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

```css
/* frontend/src/App.css */
body {
  font-family: 'SUA_FONTE', sans-serif;
}
```

---

## 📚 Referências

### Templates Originais
- `templates/index.html` - Formulário de cadastro
- `templates/vagas_public.html` - Listagem de vagas
- `templates/admin_login.html` - Login admin
- `static/css/style.css` - Estilos originais

### Documentação
- [Inter Font](https://fonts.google.com/specimen/Inter)
- [Font Awesome](https://fontawesome.com/)
- [CSS Gradients](https://cssgradient.io/)
- [Glassmorphism](https://glassmorphism.com/)

---

## ✅ Resultado

A identidade visual do React agora está **100% alinhada** com os templates originais:

✅ Gradiente azul de fundo (Ciclo Carioca)
✅ Header com logo e glassmorphism
✅ Botões com gradiente roxo/azul
✅ Cards com efeito glass
✅ Tipografia Inter
✅ Ícones Font Awesome
✅ Animações suaves
✅ Responsivo
✅ Acessível

**A experiência visual é consistente entre Flask e React!** 🎉
