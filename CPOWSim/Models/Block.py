class Block(object):

    def __init__(self, previous=0, hash="e7ce38343b4e44599f0f75943923e846acac210dbb9d847a950134ea74cf31dd",
                 depth=0, timestamp=0, round=0, ip=0, size=1.0, nonce=0, transactions=[], first_come=[]):
        self.previous = previous
        self.depth = depth
        self.timestamp = timestamp
        self.round = round
        self.transactions = transactions
        self.ip = ip
        self.nonce = nonce
        self.size = size
        self.first_come = first_come
        self.hash = hash
