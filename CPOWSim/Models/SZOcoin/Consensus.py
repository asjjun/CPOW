import numpy as np
from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as BaseConsensus
import random

class Consensus(BaseConsensus):

    def Protocol(miner):
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        return random.expovariate(hashPower * 1/p.Binterval)

    def fork_resolution():
        BaseConsensus.global_chain = []

        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().ip]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().ip == z:
                for bc in range(len(i.blockchain)):
                    BaseConsensus.global_chain.append(i.blockchain[bc])
                break
