/* =========================================================================
   Portfólio Pessoal - Marcelo Prates
   script.js | JavaScript puro (sem frameworks)
   Funcionalidades:
     1. Alternância de tema claro/escuro (com persistência via localStorage)
     2. Menu responsivo (hamburguer)
     3. Validação do formulário de contato
     4. Simulação de envio + modal de confirmação
     5. Ano automático no rodapé
   ========================================================================= */

// Executa só depois que todo o HTML estiver carregado
document.addEventListener('DOMContentLoaded', function () {

  /* ------------------------------------------------------------------
     1. TEMA CLARO / ESCURO
     ------------------------------------------------------------------ */
  const botaoTema = document.getElementById('botaoTema');
  const iconeTema = document.getElementById('iconeTema');
  const html = document.documentElement;

  // Recupera o tema salvo anteriormente pelo usuário (se houver)
  const temaSalvo = localStorage.getItem('tema');
  if (temaSalvo === 'dark') {
    html.setAttribute('data-theme', 'dark');
    iconeTema.textContent = '☀';
  }

  botaoTema.addEventListener('click', function () {
    const ehEscuro = html.getAttribute('data-theme') === 'dark';
    if (ehEscuro) {
      html.removeAttribute('data-theme');   // volta ao tema claro
      iconeTema.textContent = '◐';
      localStorage.setItem('tema', 'light');
    } else {
      html.setAttribute('data-theme', 'dark');  // ativa tema escuro
      iconeTema.textContent = '☀';
      localStorage.setItem('tema', 'dark');
    }
  });

  /* ------------------------------------------------------------------
     2. MENU RESPONSIVO (HAMBURGUER)
     ------------------------------------------------------------------ */
  const navToggle = document.getElementById('navToggle');
  const navLista = document.getElementById('navLista');

  navToggle.addEventListener('click', function () {
    const aberto = navLista.classList.toggle('aberto');
    navToggle.classList.toggle('ativo');
    // Atualiza acessibilidade
    navToggle.setAttribute('aria-expanded', aberto);
    navToggle.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
  });

  // Fecha o menu ao clicar em qualquer link (melhora a experiência no mobile)
  document.querySelectorAll('.nav__link').forEach(function (link) {
    link.addEventListener('click', function () {
      navLista.classList.remove('aberto');
      navToggle.classList.remove('ativo');
      navToggle.setAttribute('aria-expanded', false);
    });
  });

  /* ------------------------------------------------------------------
     3. VALIDAÇÃO DO FORMULÁRIO DE CONTATO
     ------------------------------------------------------------------ */
  const form = document.getElementById('formContato');
  const campoNome = document.getElementById('nome');
  const campoEmail = document.getElementById('email');
  const campoMensagem = document.getElementById('mensagem');

  // Função auxiliar: exibe mensagem de erro em um campo
  function mostrarErro(campo, idErro, mensagem) {
    document.getElementById(idErro).textContent = mensagem;
    campo.parentElement.classList.add('invalido');
  }

  // Função auxiliar: limpa o erro de um campo
  function limparErro(campo, idErro) {
    document.getElementById(idErro).textContent = '';
    campo.parentElement.classList.remove('invalido');
  }

  // Valida o formato do e-mail usando expressão regular
  function emailValido(email) {
    const padrao = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return padrao.test(email);
  }

  form.addEventListener('submit', function (evento) {
    evento.preventDefault();   // impede o envio padrão do navegador
    let valido = true;

    // Validação do nome
    if (campoNome.value.trim() === '') {
      mostrarErro(campoNome, 'erroNome', 'Por favor, informe seu nome.');
      valido = false;
    } else {
      limparErro(campoNome, 'erroNome');
    }

    // Validação do e-mail
    if (campoEmail.value.trim() === '') {
      mostrarErro(campoEmail, 'erroEmail', 'Por favor, informe seu e-mail.');
      valido = false;
    } else if (!emailValido(campoEmail.value.trim())) {
      mostrarErro(campoEmail, 'erroEmail', 'Digite um e-mail válido (ex: voce@dominio.com).');
      valido = false;
    } else {
      limparErro(campoEmail, 'erroEmail');
    }

    // Validação da mensagem
    if (campoMensagem.value.trim() === '') {
      mostrarErro(campoMensagem, 'erroMensagem', 'Por favor, escreva uma mensagem.');
      valido = false;
    } else {
      limparErro(campoMensagem, 'erroMensagem');
    }

    /* --------------------------------------------------------------
       4. ENVIO REAL (Formspree) + MODAL DE CONFIRMAÇÃO

       ATENÇÃO: antes daqui existia uma SIMULAÇÃO de envio — o modal de
       sucesso aparecia sem nada ser enviado. Agora o envio é de verdade,
       e o modal só aparece se o Formspree confirmar o recebimento.
       -------------------------------------------------------------- */
    if (!valido) return;

    enviarFormulario();
  });

  /**
   * Envia o formulário pro endpoint definido no atributo action do <form>.
   * Usa fetch com Accept: application/json — sem isso o Formspree responde
   * com uma página HTML de redirect em vez de JSON.
   */
  async function enviarFormulario() {
    const botao = document.getElementById('botaoEnviar');
    const status = document.getElementById('formStatus');
    const textoOriginal = botao.textContent;

    // Estado de carregando: evita clique duplo e dá retorno visual
    botao.disabled = true;
    botao.textContent = 'Enviando...';
    status.textContent = '';
    status.classList.remove('form__status--erro');

    try {
      const resposta = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      });

      if (resposta.ok) {
        form.reset();               // só limpa DEPOIS de confirmar o envio
        abrirModal();
      } else {
        // O Formspree devolve o motivo em JSON quando recusa o envio
        const dados = await resposta.json().catch(function () { return {}; });
        const motivo = dados.errors
          ? dados.errors.map(function (e) { return e.message; }).join(', ')
          : 'Não foi possível enviar agora.';
        mostrarFalha(status, motivo);
      }
    } catch (erro) {
      // Cai aqui em falha de rede / offline
      mostrarFalha(status, 'Sem conexão com o servidor.');
    } finally {
      botao.disabled = false;
      botao.textContent = textoOriginal;
    }
  }

  /**
   * Mostra o erro e oferece o e-mail direto como saída —
   * um contato perdido custa muito mais que uma mensagem de erro feia.
   */
  function mostrarFalha(status, motivo) {
    status.innerHTML = motivo +
      ' Escreva direto para <a href="mailto:marcelomprates@gmail.com">' +
      'marcelomprates@gmail.com</a>.';
    status.classList.add('form__status--erro');
  }

  /* ------------------------------------------------------------------
     MODAL DE SUCESSO
     ------------------------------------------------------------------ */
  const modal = document.getElementById('modal');
  const fecharModalBtn = document.getElementById('fecharModal');

  function abrirModal() {
    modal.classList.add('ativo');
    modal.setAttribute('aria-hidden', 'false');
  }
  function fecharModal() {
    modal.classList.remove('ativo');
    modal.setAttribute('aria-hidden', 'true');
  }

  fecharModalBtn.addEventListener('click', fecharModal);
  // Fecha ao clicar fora da caixa do modal
  modal.addEventListener('click', function (e) {
    if (e.target === modal) fecharModal();
  });
  // Fecha com a tecla ESC (acessibilidade)
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') fecharModal();
  });

  /* ------------------------------------------------------------------
     5. ANO AUTOMÁTICO NO RODAPÉ
     ------------------------------------------------------------------ */
  document.getElementById('ano').textContent = new Date().getFullYear();

});
