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

## Fontes e referências

1. [How the teleprinter works (1940) \[Dufaycolor\]](https://youtu.be/Mi2Sx-ZY410?si=YfXiibwzfE9dYEjh)
2. [Teletype Model 33](https://en.wikipedia.org/wiki/Teletype_Model_33)

## Licença

Este material está disponível sob a [licença MIT](./LICENSE).

