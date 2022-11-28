
class InputsConfig:

    Binterval = 600 # Block interval
    Bdelay = 0.42 # Block 네트워크 Delay
    Breward = 12.5 # 채굴보상

    ''' Transaction Parameters '''
    hasTrans = True # Transaction 수신 유/무 (확장성)
    Tn = 2 # transaction을 받는 기준 (양)
    Tdelay = 5.1 # Transaction의 네트워크 Delay
    Tfee = 0.000062 # Transaction 수수료
    Tsize = 0.000546 # Transaction 크기

    ''' Node Parameters '''
    Nn = 30 # 노드의 수
    NODES = []
    from Models.SZOcoin.Node import Node

    # default NODES.
    for i in range(Nn) :
        NODES.append(Node(id=i, hashPower=40))

    ''' Simulation Parameters '''
    simTime = 2000 # transaction을 받는 기준 (시간)
    Runs = 1 # Cycle 횟수

    ''' CPOW Parameters '''
    SNR = 0.5 # Serviving Node Rate
