# Registros anteriores à convenção `Aprendi:`

Este arquivo existe só para os aprendizados que aconteceram **antes** de
começarmos a registrar direto no commit. Daqui pra frente não precisa mexer
nele: basta escrever `Aprendi:` na mensagem do commit e a página se atualiza
sozinha.

Formato de cada entrada:

```
## título curto
data: AAAA-MM-DD
origem: contexto de uma linha
Texto explicando o que aconteceu e o que ficou.
```

Pode apagar, editar ou reescrever qualquer entrada abaixo — o script só lê
o que estiver aqui.

---

## Interface que mente sucesso é pior que interface que falha
data: 2026-08-17
origem: correção do formulário de contato
O formulário chamava preventDefault e depois só abria o modal de sucesso, sem
enviar nada. O endpoint estava no HTML, mas o JavaScript ainda rodava a
simulação de envio da versão acadêmica. Resultado: seis semanas exibindo
"mensagem enviada com sucesso" enquanto descartava tudo em silêncio. A lição
não é sobre fetch: é que testar o caminho feliz não prova nada quando o
caminho feliz é justamente o que foi simulado. Verificar o efeito, não a
resposta.

## Regex não entende estrutura aninhada
data: 2026-08-17
origem: troca do favicon nas quatro páginas
Usei `<link rel="icon"[^>]*>` para substituir o favicon. O problema é que o
valor era um data-URI com SVG dentro, e SVG tem `>` no meio. O padrão cortou
no primeiro `>` que encontrou e deixou lixo em todos os arquivos. Regex casa
padrão de texto, não hierarquia — quando o conteúdo pode conter o próprio
delimitador, ou se usa um parser, ou se aceita conferir o resultado depois.

## Inverter estado a partir do atributo, não do que está valendo
data: 2026-08-17
origem: suporte a prefers-color-scheme
O botão de tema lia o atributo data-theme para decidir se invertia para claro
ou escuro. Quando o tema vinha da preferência do sistema, esse atributo estava
vazio — o código concluía "está claro" e tentava ir para o escuro, que já era
o estado atual. Clique morto. Passei a calcular o tema efetivo antes de
inverter. Estado derivado de duas fontes precisa de uma função que resolva as
duas, nunca da leitura de uma só.

## Texto dentro de SVG não é texto
data: 2026-08-17
origem: geração da imagem de compartilhamento
O wordmark da marca usava `<text>` num SVG. Na primeira renderização saiu em
fonte serifada, porque texto em SVG depende da fonte existir na máquina de
quem abre. Num favicon isso não importa; num og:image ou num cartão, a marca
simplesmente vira outra coisa. Tipografia de identidade tem que ir
rasterizada ou convertida em curvas.

## Erro em dado estruturado falha em silêncio
data: 2026-08-17
origem: JSON-LD nas quatro páginas
Uma vírgula fora do lugar no JSON-LD faz o Google descartar o bloco inteiro,
sem aviso e sem erro visível em lugar nenhum. Diferente de HTML, que o
navegador tenta consertar, aqui não existe degradação graciosa: ou vale tudo,
ou não vale nada. Passei a validar em três níveis — o JSON puro, o parse
dentro do navegador e o resultado no inspetor externo.
