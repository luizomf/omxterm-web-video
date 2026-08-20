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

## Licença

Este material está disponível sob a [licença MIT](./LICENSE).

