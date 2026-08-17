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
├── index.html            # home: sobre, formação, portfólio, serviços, contato
├── caso-pcp.html         # estudo de caso — PCP Embalagem
├── caso-b2b.html         # estudo de caso — Plataforma B2B
├── caso-financeiro.html  # estudo de caso — Controle Financeiro com IA
├── estilo.css            # variáveis, temas claro/escuro, responsividade
├── script.js             # menu, tema, validação e envio do formulário
└── README.md
```

O mesmo `script.js` roda em todas as páginas. Como as páginas de caso não têm
formulário nem menu hambúrguer, cada bloco é protegido por guarda de null —
sem isso, o primeiro `getElementById` vazio derrubaria o arquivo inteiro.

## ▶️ Rodar local

Sem build:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Ou abrir `index.html` direto no navegador / Live Server no VS Code.

## 📌 Changelog

### 2026-08-17 · Fase 3 — marca Digital Droids
- **Marca própria em SVG**: um droid cuja face é um terminal (barra de título,
  prompt `>`, cursor `_`) — amarra na assinatura `~/marcelo_` que já existia.
  Inline, ~500 bytes, `currentColor`, nítido de 16px a qualquer tamanho.
- Aplicada em: favicon (todas as páginas), header ao lado do `~/marcelo_`,
  assinatura da marca abrindo a seção Digital Droids, e rodapé.
- O cursor do droid pisca no mesmo ritmo do cursor do logo, e respeita
  `prefers-reduced-motion`.
- **Ícones dos serviços trocados de emoji para SVG inline** — emoji vinham
  coloridos e com desenho diferente em cada sistema operacional, competindo com
  a marca. Agora são 4 ícones no mesmo traço do droid (viewBox 32, stroke 2,
  cantos redondos) usando `currentColor`. Classe `.servico__icone` → `.ico`.
  Nenhum deles usa "janela com barra de título" — essa forma é exclusiva da marca.
- **O site passou a respeitar o tema do sistema operacional.** Antes o escuro só
  aparecia clicando no botão: quem usa o SO em dark recebia o site claro na
  primeira visita. Agora `@media (prefers-color-scheme: dark)` define o padrão,
  e `:not([data-theme="light"])` preserva a escolha manual — **sistema decide,
  usuário explícito ganha**. Script inline no `<head>` aplica o tema salvo antes
  da primeira pintura, evitando flash. O botão inverte a partir do tema
  *efetivo*, não do atributo, senão o primeiro clique não faria nada.


### 2026-08-17 · Fase 2 — conteúdo e posicionamento
- **Links mortos eliminados.** Os três cards apontavam para o perfil genérico do
  GitHub; nenhum dos projetos tem repo público. Agora levam a estudos de caso.
- **Três páginas de estudo de caso** com a seção "o que eu precisei saber para
  construir isso" — o log de aprendizado nascendo dentro do portfólio.
- **Posicionamento em camadas:** hero com o cargo buscável (Desenvolvedor Full
  Stack), liderança de TI na prosa, Vibe Coding explicado como método.
- **Seção de serviços Digital Droids** (PJ) com CTA comercial.
- **Stack agrupada por finalidade** — linguagens, web, IA/automação, integração,
  infra, ferramentas.
- `script.js` com guardas de null para rodar nas páginas de caso.
- `scroll-margin-top` nas seções: a âncora deixava só 3px de folga sob o header.
- OpenGraph, canonical e favicon.

### 2026-08-17 · Fase 1
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
