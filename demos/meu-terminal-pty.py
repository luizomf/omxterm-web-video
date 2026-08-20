#!/usr/bin/env python3

import fcntl
import os
import select
import termios
import tkinter as tk

# Informação: master/slave são termos oficiais. Mas, assim como o branch master
# do Git passou a ser chamado de main, hoje há uma preferência por evitar essa
# terminologia em novos textos. Ainda não existe um substituto universalmente
# adotado (pelo menos que eu saiba), mas algumas alternativas são
# controller/device, primary/secondary e leader/follower.
# Ultimamente, leader e follower são os termos que mais tenho encontrado.
# Estou usando os termos oficiais para não causar confusão.

# SHELL hardcoded para demo. Para usar seu shell, use:
# SHELL = os.getenv("SHELL", "/bin/bash")
SHELL = "/bin/bash"

# Cria explicitamente as duas pontas do pseudoterminal (PTY):
#
#       user     <-> [                KERNEL                 ] <-> user
#  este programa <-> [ master_fd <-> driver PTY <-> slave_fd ] <-> shell

# O master é a ponta do controlador, papel normalmente ocupado por um terminal
# emulator. Escrever nele produz input para o slave; ler dele recebe output do
# slave. O slave é o TTY visto pelo shell e contém as configurações de termios e
# a line discipline responsável por modo canônico, echo e caracteres especiais.
master_fd, slave_fd = os.openpty()

# Esvazia o buffer antes do fork para a mensagem não ficar pendente e acabar
# herdada pelos dois processos quando stdout não estiver ligado a um terminal.
print(f"Master FD={master_fd}", f"Slave FD={slave_fd}", flush=True)

# Depois do fork, pai e filho possuem cópias dos dois descritores. Cada processo
# fecha a ponta que não usará.

# fork = criar um novo processo a partir do processo atual com o mesmo contexto.
# Ambos (processos pai e filho) continuam logo depois do fork(), mas possuem
# identidades próprias e podem seguir caminhos diferentes.
pid = os.fork()  # fork deste programa (Ele rodará duas vezes)

if pid == 0:
    # FILHO: será substituído pelo shell e precisa apenas da ponta slave.
    # O zero é apenas o retorno de fork() no filho; o PID real vem de getpid().
    # stdout ainda é o do programa original, pois o dup2 acontece mais abaixo;
    # portanto esta mensagem aparece no terminal que iniciou a demonstração.
    print(
        f"Slave: PID={os.getpid()}. Closing master_fd={master_fd}",
        flush=True,
    )

    # Cria uma nova sessão. Como session leader, o filho pode adquirir o slave
    # como controlling terminal e usar process groups e job control.
    os.setsid()
    fcntl.ioctl(slave_fd, termios.TIOCSCTTY, 0)

    # Antes do dup2(), a tabela de descritores do processo filho está assim:
    #
    # fd 0 ─┐
    # fd 1 ─┼──→ slave do PTY original, herdado do processo pai
    # fd 2 ─┘
    #
    # slave_fd ──→ slave do novo PTY, criado por openpty()

    # Pense nessa tabela como um painel de conexões numeradas. slave_fd já é uma
    # tomada ligada ao novo PTY; dup2 refaz as conexões 0, 1 e 2 para a mesma
    # linha. Ele não copia bytes e não cria descritores dentro do PTY.
    os.dup2(slave_fd, 0)  # stdin do processo passa a vir do novo TTY
    os.dup2(slave_fd, 1)  # stdout do processo passa a ir para o novo TTY
    os.dup2(slave_fd, 2)  # stderr do processo também vai para o novo TTY

    # Depois dos três dup2():
    #
    # fd 0 ───────┐
    # fd 1 ───────┼──→ slave do novo PTY, criado por openpty()
    # fd 2 ───────┤
    # slave_fd ───┘

    # As três novas referências mantêm o slave aberto; o descritor original
    # slave_fd agora é uma conexão redundante e pode ser fechado.
    if slave_fd > 2:
        os.close(slave_fd)

    # Agora a tabela fica:
    #
    # fd 0 ─┐
    # fd 1 ─┼──→ slave do novo PTY, criado por openpty()
    # fd 2 ─┘

    # execvp() troca o programa Python pelo Bash, mas mantém o mesmo processo e
    # seu painel de descritores. Por isso o Bash já começa com stdin, stdout e
    # stderr conectados ao novo PTY. Em caso de sucesso, execvp() nunca retorna.
    try:
        os.execvp(SHELL, [SHELL])
    except OSError as error:
        # stderr já aponta para o slave, então a falha aparece na interface. O
        # filho precisa encerrar aqui para não continuar pelo caminho do pai.
        # os._exit() encerra imediatamente, sem executar limpezas e buffers do
        # Python herdados no fork; 127 é o status convencional para falha ao
        # localizar ou executar um comando.
        os.write(2, f"Não foi possível executar {SHELL}: {error}\n".encode())
        os._exit(127)

print(f"Master: {os.getpid()}. Closing slave_fd={slave_fd}")

# PAI: assume o papel mínimo de um terminal emulator e usa apenas o master. Se
# mantivesse o slave aberto, poderia não observar o encerramento quando o shell
# fechasse suas próprias cópias.
os.close(slave_fd)

# Esta interface demonstra somente o encanamento fundamental de um emulator:
# captura eventos de teclado, envia bytes ao PTY, recebe bytes e os exibe. Ela
# propositalmente não implementa parser VT/ANSI, screen model, cursor, cores,
# composição de texto nem decoding UTF-8 incremental.
root = tk.Tk()
root.title(f"Not a terminal: {SHELL}")

# O Text é apenas uma superfície simples para visualizar os bytes decodificados;
# ele não transforma esta demonstração em um terminal emulator completo.
out = tk.Text(
    root,
    bg="#000000",
    fg="#eae8ff",
    insertbackground="#eae8ff",
    highlightthickness=0,
    padx=15,
    pady=10,
    relief="flat",
    font=("Fira Code", 18),
    width=90,
    height=20,
    wrap=tk.NONE,
    borderwidth=0,
)
out.pack(fill="both", expand=True)

# Uma sequência de controle pode ser dividida entre dois reads. Guardamos aqui
# o prefixo incompleto para terminá-lo quando o próximo chunk chegar.
pending_output_control = b""
ERASE_TO_END = b"\x1b[K"  # CSI K: apaga do cursor até o fim da linha


def consume_erase_to_end(data, pending):
    """Remove CSI K completa e devolve qualquer prefixo pendente."""

    combined = pending + data
    pending = b""

    # Se o chunk terminar com ESC ou ESC + [, ainda não sabemos se a sequência
    # será CSI K. Adiamos esses bytes em vez de deixar "[K" escapar na tela.
    for prefix_size in range(1, len(ERASE_TO_END)):
        prefix = ERASE_TO_END[:prefix_size]
        if combined.endswith(prefix):
            combined = combined[:-prefix_size]
            pending = prefix
            break

    return combined.replace(ERASE_TO_END, b""), pending


def render_output(data):
    """Exibe bytes do PTY com suporte visual mínimo a backspace."""

    global pending_output_control

    # Em modo canônico com ECHOE, a line discipline pode ecoar erase como BS +
    # espaço + BS. Já o Bash interativo usa Readline, que controla sua própria
    # edição e neste sistema desenha o erase como BS + CSI K. Como o BS abaixo já
    # remove o último caractere do Text, CSI K não tem trabalho visual restante
    # e pode ser consumida. Isto não pretende processar outras sequências CSI ou
    # substituir um parser de terminal completo.
    data, pending_output_control = consume_erase_to_end(data, pending_output_control)

    # O Text do Tk não interpreta BS: inserir o caractere de controle não move
    # nem apaga seu conteúdo. Para esta demo, tratamos cada BS como uma remoção
    # visual do último caractere. Isso cobre as duas formas de erase descritas
    # acima, mas não substitui o cursor e o screen model de um emulator real.
    text = data.decode(errors="replace")

    for character in text:
        if character == "\b":
            # O Text sempre mantém uma quebra de linha final implícita. Estes
            # índices selecionam o caractere visível imediatamente anterior.
            if out.compare("end-1c", ">", "1.0"):
                previous = out.get("end-2c", "end-1c")
                if previous != "\n":
                    out.delete("end-2c", "end-1c")
            continue

        out.insert("end", character)


def pump():
    """Move o output disponível no master para a interface."""

    # select com timeout zero consulta o descritor sem bloquear o event loop do
    # Tk. Um read devolve um chunk arbitrário, não uma tecla, linha ou mensagem.
    readable, _, _ = select.select([master_fd], [], [], 0)

    if readable:
        try:
            # Estes bytes já atravessaram o caminho de output do TTY. Eles podem
            # vir do shell/programa ou do echo produzido pela line discipline.
            data = os.read(master_fd, 65536)
        except OSError:
            # Alguns sistemas sinalizam o fechamento do slave como erro no
            # master em vez de retornar um byte string vazio.
            data = b""

        if data:
            # O decode por chunk continua sendo uma simplificação didática. Um
            # emulator real usa decoder incremental porque um caractere UTF-8
            # pode ser dividido entre reads diferentes.
            render_output(data)
            out.see("end")

            # OUTPUT mostra os bytes depois do output processing. Isso inclui,
            # por exemplo, a conversão de NL para CR-LF feita por ONLCR.
            print("OUTPUT:", data)
            print(80 * "-")
        else:
            # Sem mais bytes, o shell fechou o slave e o pump pode parar.
            out.insert("end", "\n[shell encerrou]\n")
            out.see("end")
            return

    # Agenda a próxima consulta sem bloquear a thread responsável pela GUI.
    root.after(1, pump)


def send(data):
    """Envia bytes pelo master para o caminho de input do TTY."""

    try:
        # INPUT registra os bytes antes do input processing. Depois do write, a
        # line discipline pode convertê-los, armazená-los, ecoá-los, consumi-los
        # como controles ou entregá-los ao programa conectado ao slave.
        print("INPUT:", data)
        os.write(master_fd, data)
    except OSError:
        # A escrita pode falhar se o shell já tiver encerrado o slave.
        pass


def on_key(event):
    """Converte texto digitado no Tk em bytes UTF-8 para o PTY."""

    if event.char:
        send(event.char.encode("utf-8"))

    # Impede o Text de inserir a tecla localmente. O caractere só deve aparecer
    # quando voltar pelo master, seja por echo do TTY ou output do programa.
    return "break"


def special(byte):
    """Cria um handler para teclas que representam bytes de controle."""

    def handler(event):
        send(byte)
        return "break"

    return handler


# Teclas comuns seguem event.char. As ligações específicas abaixo reproduzem os
# bytes tradicionalmente enviados por um terminal emulator para estas teclas.
out.bind("<Key>", on_key)
out.bind("<BackSpace>", special(b"\x7f"))  # DEL: erase padrão no macOS
out.bind("<Return>", special(b"\r"))  # CR; ICRNL normalmente o converte em NL
out.bind("<Control-c>", special(b"\x03"))  # VINTR; ISIG normalmente gera SIGINT


def on_close():
    """Encerra o processo filho ao fechar a janela da demonstração."""

    try:
        # SIGKILL mantém o encerramento deste exemplo curto e determinístico. Um
        # emulator real tentaria encerrar a sessão de forma graciosa e aguardaria
        # todos os processos relacionados.
        os.kill(pid, 9)
    except OSError:
        # O shell pode já ter terminado por conta própria.
        pass

    root.destroy()


# Liga o fechamento da janela ao encerramento do shell filho.
root.protocol("WM_DELETE_WINDOW", on_close)

# O widget precisa de foco para receber as teclas. pump inicia a leitura do
# master; mainloop passa a despachar eventos de teclado, timer e janela.
out.focus_set()
pump()
root.mainloop()
