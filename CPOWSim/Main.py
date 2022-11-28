from InputsConfig import InputsConfig as p
from Event import Queue
from Models.SZOcoin.BlockCommit import BlockCommit
from Models.Transaction import CPOWTransaction as CT
from Models.SZOcoin.Node import Node

########################################################## Start Simulation ##############################################################


def main():
    for i in range(p.Runs):
        ### 1~3라운드 한번
        clock, first_come = 0, []  # set clock to 0 at the start of the simulation
        if p.hasTrans:
            CT.create_transactions()

        Node.generate_gensis_block()
        for node in p.NODES:
            first_come.append(node)

        for round_index in range(1,4) :
            first_come = BlockCommit.generate_initial_events(first_come, round_index)
            event = Queue.event_list[round_index - 1]
            BlockCommit.generate_block(event, round_index)

            ## 디버깅 코드 ##
            print(str(round_index) + "라운드에 통과한 노드 : ", end=" ")
            for node in event.first_come :
                print(node.id, end=" ")
            print()
        Queue.event_list = []


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
