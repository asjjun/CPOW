from InputsConfig import InputsConfig as p
import random
from Event import Event, Queue
from Models.Block import Block
from Models.Transaction import CPOWTransaction as CT
from SHA_256 import SHA_256


class Scheduler:

    def create_block_event(first_come, eventTime, round):
        miner = first_come[0]
        block = Block()
        block.previous = miner.blockchain[len(miner.blockchain) - 1].hash
        block.depth = len(miner.blockchain)
        block.timestamp = eventTime
        block.round = round

        CT.create_transactions()
        block.transactions = p.NODES[miner.id].transactionsPool
        block.ip = miner.id

        block.nonce = random.randrange(100000000000)
        block.first_come = first_come
        block.hash = SHA_256(block.previous, block.depth, block.timestamp, block.round,
                             block.ip, block.nonce, block.transactions, block.first_come)

        event = Event(first_come, eventTime, block)  # create the event
        Queue.add_event(event)  # add the event to the queue
