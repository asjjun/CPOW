from Scheduler import Scheduler
from InputsConfig import InputsConfig as p
from Models.Transaction import CPOWTransaction as CT
from Models.Network import Network
from Models.SZOcoin.Consensus import Consensus as c
from Models.BlockCommit import BlockCommit as BaseBlockCommit
from Event import Event


class BlockCommit(BaseBlockCommit):

    # Block Creation Event
    def generate_block (event, round_index):
        miner = p.NODES[event.block.ip]
        blockPrev = event.block.previous

        if blockPrev == miner.last_block().hash:
            if p.hasTrans:
                blockTrans, blockSize = CT.execute_transactions(miner)

                event.block.transactions = blockTrans
                event.block.usedgas = blockSize
                ### block만들기

            miner.blockchain.append(event.block)
            BlockCommit.propagate_block(event.block)

    # Block Receiving Event
    def receive_block (event):

        miner = p.NODES[event.block.ip]
        blockPrev = event.block.previous # previous block id

        node = p.NODES[event.first_come[0].id] # recipint
        lastBlockId = node.last_block().hash # the id of last block

        #### case 1: the received block is built on top of the last block according to the recipient's blockchain ####
        if blockPrev == lastBlockId:
            node.blockchain.append(event.block) # append the block to local blockchain

            #######################################################
            # BlockCommit.update_transactionsPool(node, event.block)

         #### case 2: the received block is  not built on top of the last block ####
        else:
            depth = event.block.depth + 1
            if (depth > len(node.blockchain)):
                BlockCommit.update_local_blockchain(node,miner,depth)

            BlockCommit.update_transactionsPool(node,event.block) # not sure yet.


    def generate_initial_events(first_come, round_index):
        currentTime = 0
        blockTimes = []

        if round_index != 3 :
            for node in first_come:
                blockTimes.append((currentTime + c.Protocol(node), node))

            blockTimes = sorted(blockTimes, key=lambda x: x[0])
            RNR = int(len(blockTimes) * p.SNR)  # Remain Node Rate

            first_come = []
            for node in blockTimes[0:RNR]:
                first_come.append(node[1])

            Scheduler.create_block_event(first_come, blockTimes[0][0], round_index)

            return first_come
        else :
            for node in first_come:
                blockTimes.append((currentTime + c.Protocol(node), node))

            blockTimes = sorted(blockTimes, key=lambda x: x[0])
            Scheduler.create_block_event([blockTimes[0][1]], blockTimes[0][0], 3)
            return [blockTimes[0][1]]


    def propagate_block (block):
        for recipient in p.NODES:
            if recipient.id != block.ip:
                receive_block_time = block.timestamp + Network.block_prop_delay()
                BlockCommit.receive_block(Event([recipient], receive_block_time, block))
