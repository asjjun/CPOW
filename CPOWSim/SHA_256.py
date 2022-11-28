import hashlib

class SHA_256() :
    input_data = ""
    hash = ""
    def __init__(self, previous, depth, timestamp, round, ip, nonce, transactions, first_come):
        self.input_data = str(previous) + str(depth) + str(timestamp) + str(round) + str(ip) + str(nonce)

        for transaction in transactions :
            self.input_data += str(transaction)

        for node_ip in first_come:
            self.input_data += str(node_ip)

        self.hash = hashlib.sha256(self.input_data.encode("utf-8")).hexdigest()

    def getHash(self):
        return self.hash