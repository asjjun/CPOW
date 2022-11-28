from Models.Block import Block

class Node(object):
    def __init__(self,id):
        self.id= id
        self.blockchain= []
        self.transactionsPool= []
        self.blocks= 0#
        self.balance= 0

    # Generate the Genesis block and append it to the local blockchain for all nodes
    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain.append(Block())

    # Get the last block at the node's local blockchain
    def last_block(self):
        return self.blockchain[len(self.blockchain)-1]

    # Get the length of the blockchain (number of blocks)
    def blockchain_length(self):
        return len(self.blockchain)-1

