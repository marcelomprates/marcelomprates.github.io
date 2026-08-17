# marcelomprates.github.io

Site pessoal e portfólio — **HTML5, CSS3 e JavaScript puro**, sem frameworks
e sem etapa de build. Deploy é `git push` (GitHub Pages, branch `main`, raiz).

## 🔗 Acesso

- **Site:** https://marcelomprates.github.io
- **Origem:** evoluído de
  [`portfolio-marcelo-prates`](https://github.com/marcelomprates/portfolio-marcelo-prates),
  Atividade Prática de *Fundamentos da Programação Web* (Engenharia de
  Software · UNINTER). Aquele repo fica intacto como o artefato entregue e
  avaliado; este continua a história.

## ✨ Funcionalidades

- Quatro seções (Sobre, Formação, Portfólio, Contato) em página única com
  menu fixo e rolagem suave
- Tema claro/escuro com persistência via `localStorage`
- Menu hambúrguer no mobile
- Formulário de contato com validação em JS **e envio real via Formspree**,
  com estado de carregando, tratamento de falha e fallback pro e-mail direto
- Layout responsivo mobile-first

## 🛠️ Estrutura

```
.
├── index.html      # estrutura e conteúdo das seções
├── estilo.css      # variáveis, temas claro/escuro, responsividade
├── script.js       # menu, tema, validação e envio do formulário
└── README.md
```

## ▶️ Rodar local

Sem build:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Ou abrir `index.html` direto no navegador / Live Server no VS Code.

## 📌 Changelog

### 2026-08-17
- 🚨 **Correção crítica:** o formulário de contato exibia o modal de sucesso
  sem enviar nada. O `action` do Formspree estava no HTML, mas o `script.js`
  ainda rodava a *simulação* de envio da versão acadêmica — toda mensagem
  enviada desde 02/07/2026 foi silenciosamente descartada. Agora o envio é
  um `fetch` real e o modal só aparece com confirmação do servidor.
- Adicionado estado de carregando no botão (evita clique duplo)
- Falha de envio agora mostra o motivo e oferece o e-mail direto, em vez de
  fingir sucesso. Os campos preenchidos são preservados.

## 👤 Autor

**Marcelo de Morais Prates** — Guarulhos, SP

- LinkedIn: [marcelo-de-morais-prates](https://www.linkedin.com/in/marcelo-de-morais-prates)
- GitHub: [@marcelomprates](https://github.com/marcelomprates)
- E-mail: marcelomprates@gmail.com
