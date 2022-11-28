from Models.Block import Block
from Models.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self,id,hashPower):
        super().__init__(id)#,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        self.blockchain = []  # create an array for each miner to store chain state locally
        self.transactionsPool = []
        self.balance = 0  # to count all reward that a miner made, including block rewards + uncle rewards + transactions fees
        self.timer = 0
        self.first_come = []
