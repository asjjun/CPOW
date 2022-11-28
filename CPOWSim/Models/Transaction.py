import random , copy
from InputsConfig import InputsConfig as p
from Models.Network import Network

class Transaction(object):

    def __init__(self,
	 id=0,
	 timestamp=0 or [],
	 sender=0,
         to=0,
	 size=0.000546,
         fee=0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.size = size
        self.fee= fee


class CPOWTransaction():

    def create_transactions():
        Psize= int(p.Tn * p.simTime)

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            creation_time= random.randint(0,p.simTime-1)
            receive_time= creation_time
            tx.timestamp= [creation_time,receive_time]
            sender= random.choice (p.NODES)
            tx.sender = sender.id
            tx.to= random.choice (p.NODES).id
            tx.size= random.expovariate(1/p.Tsize)
            tx.fee= random.expovariate(1/p.Tfee)

            sender.transactionsPool.append(tx)
            CPOWTransaction.transaction_prop(tx)

    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for i in p.NODES:
            if tx.sender != i.id:
                t= copy.deepcopy(tx)
                t.timestamp[1] = t.timestamp[1] + Network.tx_prop_delay() # transaction propogation delay in seconds
                i.transactionsPool.append(t)


    def execute_transactions(miner):
        size, pool = 0, miner.transactionsPool

        for transactions in pool :
            size += transactions.size

        return pool, size
