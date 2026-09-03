# OMXTerm Web — materiais do vídeo

Este **não é o repositório do OMXTerm Web**. Ele reúne somente os arquivos, exemplos, diagramas e demais recursos mencionados ou utilizados no vídeo sobre o projeto.

O código-fonte e a documentação do OMXTerm Web estão no repositório principal:

🔗 **[github.com/luizomf/omxterm-web](https://github.com/luizomf/omxterm-web)**

## Tutorial em vídeo (PT-BR)

🎥 **[OMXTerm Web: explicação aprofundada e demonstração prática](https://youtu.be/up0im04clS8)**

## Scripts utilizados no vídeo

A pasta [`scripts/`](./scripts/) contém versões sanitizadas dos scripts auxiliares e do arquivo de configuração de exemplo utilizados durante a demonstração. Nomes de máquinas, usuários, credenciais e outros valores específicos do ambiente de gravação foram removidos ou substituídos por exemplos genéricos.

> [!WARNING]
> `first_deploy` e `reset_vps` são **destrutivos**. O primeiro redefine o checkout Git remoto e chama o segundo; `reset_vps` interrompe todos os containers e remove containers, imagens, volumes, cache e redes Docker do host. Não execute esses arquivos sem lê-los, adaptá-los e entender completamente seus efeitos — especialmente em servidores compartilhados ou com dados importantes.

`setup_omxterm_web` também altera firewall, redes Docker e arquivos de implantação. Todos os scripts foram feitos para o cenário específico apresentado no vídeo, não como ferramentas genéricas de produção. Arquivos locais com credenciais ou valores reais não fazem parte deste repositório.

### Manutenção mensal da imagem do Traefik

Uma vez por mês, um mantenedor deve revisar manualmente a imagem do proxy:

1. Consulte os [releases oficiais do Traefik](https://github.com/traefik/traefik/releases) e os [avisos de segurança oficiais](https://github.com/traefik/traefik/security/advisories). Escolha uma versão estável que inclua todas as correções aplicáveis; não use apenas uma tag mutável como `latest`.
2. Resolva o digest do índice multiplataforma da Docker Official Image com `docker buildx imagetools inspect traefik:vX.Y.Z`. Confirme que o campo `Digest` do índice, e não o digest de uma imagem de plataforma individual, tem o formato `sha256:` seguido por 64 caracteres hexadecimais.
3. Forme a referência legível e imutável `traefik:vX.Y.Z@sha256:<digest>` e atualize juntos o padrão de `scripts/setup_omxterm_web` e o valor público de `scripts/setup_omxterm_web.env.example`.
4. Na raiz do repositório, execute o teste focado com `bash tests/traefik_image_pin_test.sh`, verifique a sintaxe com `bash -n tests/traefik_image_pin_test.sh scripts/first_deploy scripts/reset_vps scripts/setup_omxterm_web scripts/setup_omxterm_web.env.example` e finalize com `git diff --check`. Revise o diff para confirmar que somente a atualização pretendida e sua documentação entraram na mudança.
5. Somente em um ambiente descartável e explicitamente autorizado, registre a referência atual para rollback e atualize apenas o serviço Traefik existente. Preserve o container da aplicação, a rede Docker, o armazenamento ACME, certificados, firewall e demais recursos do host.
6. Verifique de fora e de dentro do host: redirecionamento HTTP para HTTPS e certificado público válido; resposta do controle de acesso e da aplicação; sessão WSS no navegador até o SSH, incluindo confirmação da chave do host e um comando sentinela interativo; endereço real do cliente no caminho de proxy confiável e rejeição de `X-Forwarded-For` forjado; e versão e digest esperados no container em execução.
7. Se qualquer verificação falhar, restaure somente o serviço Traefik com a referência registrada no passo anterior e repita as verificações. Não faça limpeza ampla nem altere outros recursos para corrigir a atualização.

## Diagramas

O arquivo [`diagrams/omxterm-web-video-diagrams.excalidraw`](./diagrams/omxterm-web-video-diagrams.excalidraw) contém, em um único documento editável do Excalidraw, todos os diagramas apresentados ao longo do vídeo.

## Demonstração de pseudoterminal

O arquivo [`demos/meu-terminal-pty.py`](./demos/meu-terminal-pty.py) é o exemplo didático utilizado no vídeo para mostrar a criação de um PTY, o processo de `fork`/`exec`, a conexão do shell ao lado *slave* e o papel básico exercido pelo lado *master*.

A demonstração requer Python 3, Tkinter, Bash e um sistema compatível com as APIs Unix utilizadas. Ela é propositalmente mínima e **não implementa um emulador de terminal completo**.

## Fontes e referências

1. [How the teleprinter works (1940) \[Dufaycolor\]](https://youtu.be/Mi2Sx-ZY410?si=YfXiibwzfE9dYEjh)
2. [Teletype Model 33](https://en.wikipedia.org/wiki/Teletype_Model_33)
3. [VT100](https://en.wikipedia.org/wiki/VT100)
4. [The TTY demystified](https://www.linusakesson.net/programming/tty/)
5. [Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)
6. [Tweeting from the Teletype: How To](https://www.youtube.com/watch?v=X904FYolBs0)
7. [Pi Configs](https://github.com/luizomf/ompi)
8. [OMSkills](https://github.com/luizomf/omskills)
9. [AT&T Tech Channel](https://youtu.be/tc4ROCJYbm0?si=NFe-Ava08x4Ngby9)
10. [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/index.html)
11. [xterm.js](https://xtermjs.org/)

## Licença

Este material está disponível sob a [licença MIT](./LICENSE).
