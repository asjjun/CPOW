import hashlib
import json
from time import time
from urllib.parse import urlparse
import threading

import requests
from flask import Flask, jsonify, request, render_template
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.first_come = []
        self.valid_node = []
        self.chain = []
        self.previous_firstcome = 0
        self.hash_stop = False
        self.strange_hash_stop = False
        self.SNR = 0.8
        self.port = port
        self.nodes = set()
        self.finish_signal = True
        self.strange_rate = 0.5
        self.strange_node = []
        self.bad_first = True
        self.permute_hash = 0
        self.wallet = 0

        # Create the genesis block
        self.genensis_new_block()

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(block['port'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/nodechain')

            if response.status_code == 200:

                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain

            c_round = len(self.chain) % 3 + 1
            if c_round == 0:
                c_round = 3
            if c_round != 3:
                blockchain.previous_firstcome = len(self.chain[-1].get("first_come"))
            else:
                print("--------3라운드 종료----------")
                blockchain.previous_firstcome = len(blockchain.nodes) + 1
                blockchain.hash_stop = False

            state = False
            for node in self.chain[-1].get("first_come"):
                if port in node:
                    state = True
            if not state:
                blockchain.hash_stop = True

            blockchain.first_come = []
            blockchain.valid_node = []
            blockchain.permute_hash = 0
            # print("검증 됐냐?", self.chain)
            conclude_transactions = self.chain[-1].get('transactions')
            blockchain.update_transaction(conclude_transactions)
            return True

        return False

    def new_block(self, proof, previous_hash, first_come, port):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
        b_round = len(self.chain) % 3
        if len(self.chain) != 0 and b_round == 0:
            b_round = 3
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'round': b_round,
            'port': port,
            'first_come': first_come,
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def genensis_new_block(self):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': 1,
            'timestamp': 0,
            'transactions': [],
            'proof': 100,
            'previous_hash': 1,
            'round':0,
            'port':0,
            'first_come':[]
        }

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def update_transaction(self, conclude_transactions):
        pre_transactions = []
        # print("conclude_transactions", conclude_transactions)
        # print("self.current_transactions", self.current_transactions)
        for transaction in self.current_transactions:
            if transaction not in conclude_transactions:
                pre_transactions.append(transaction)
        #
        # print("pre_transactions", pre_transactions)
        self.current_transactions = pre_transactions

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes

        if blockchain.permute_hash == 0 :
            block_string = json.dumps(block, sort_keys=True).encode()
        else :
            block_string = (str(json.dumps(block, sort_keys=True)) + str(blockchain.permute_hash)).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_hash = self.hash(last_block)

        proof = 0
        ##port
        while self.valid_proof(port, proof, last_hash) is False and not self.hash_stop and not self.strange_hash_stop:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(port, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{port}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"


parser = ArgumentParser()
parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
args = parser.parse_args()
port = args.port

# Instantiate the Node
app = Flask(__name__)

blockchain = Blockchain()


def get_url(url):
    return requests.get(url)


def post_url(args):
    return requests.post(args[0], json.dumps(args[1]))


@app.route('/allmine', methods=['GET'])
def allmine():
    while 1:
        print("Start Mining")

        response = {
            'total_nodes': list(blockchain.nodes),
        }
        trans_nodes = []
        for node in blockchain.nodes:
            trans_nodes.append('http://' + node + '/mine')
        trans_nodes.append('http://localhost:' + str(port) + '/mine')

        with ThreadPoolExecutor(max_workers=10) as pool:
            list(pool.map(get_url, trans_nodes))

    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.hash_stop:
        print(str(port), "채굴 시작")
        if blockchain.permute_hash != 0 :
            blockchain.bad_first = False
        if blockchain.strange_hash_stop :
            blockchain.strange_hash_stop = False
            blockchain.strange_node = []
            blockchain.first_come = []
            blockchain.valid_node = []

        # print("receive_nodesFirstcome", blockchain.first_come)
        # print("receive_nodesFirstcome", blockchain.valid_node)
        # print("receive_nodesFirstcome", blockchain.bad_first)
        blockchain.finish_signal = True

        if len(blockchain.chain) % 3 == 1:
            blockchain.previous_firstcome = len(blockchain.nodes) + 1
        proof = blockchain.proof_of_work(blockchain.chain[-1])
        # print("proof", proof)
        # print("------------------block to chain-----------------------\n", blockchain.chain[-1])
        blockchain.new_transaction(
            sender="0",
            recipient=port,
            amount=1
        )
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(blockchain.chain[-1])
        print("previous_hash", previous_hash)

        frame = {
            'nonce': proof,
            'port': port,
            'previous_hash': previous_hash
        }

        if len(blockchain.first_come) == 0:
            blockchain.first_come.append([port, proof])
            blockchain.valid_node.append([port, proof])

        list_of_urls = []
        for node in blockchain.nodes:
            list_of_urls.append(('http://' + node + '/validation', frame))

        with ThreadPoolExecutor(max_workers=10) as pool:
            list(pool.map(post_url, list_of_urls))

        return jsonify(frame), 200
    else:
        drop = {
            'message': "I dropped out."
        }
        return jsonify(drop), 200


@app.route('/receive_nodesFirstcome', methods=['POST'])
def receive_nodesFirstcome():
    values = json.loads(request.get_data())
    if "True" == values.get("state"):
        if values.get("port") not in blockchain.strange_node :
            blockchain.strange_node.append(values.get("port"))

        if len(blockchain.strange_node) >= int(blockchain.previous_firstcome * blockchain.strange_rate) and not blockchain.strange_hash_stop :
            blockchain.permute_hash += 1
            blockchain.strange_hash_stop = True
            blockchain.strange_node = []
            blockchain.first_come = []
            blockchain.valid_node = []
            print("악성 노드로 인해 해당 라운드 초기화")
            print("채굴 라운드 재시작")
            return jsonify(values), 200

    return jsonify(values), 200


@app.route('/unreceiveFirstcome', methods=['POST'])
def unreceiveFirstcome():
    values = json.loads(request.get_data())
    s_port = values.get("port")
    if s_port in blockchain.strange_node :
        return jsonify(values), 200

    blockchain.strange_node.append(s_port)
    if len(blockchain.valid_node) - len(blockchain.first_come) >= int(blockchain.previous_firstcome * blockchain.strange_rate):
        if port not in blockchain.strange_node:
            blockchain.strange_node.append(port)

        data_frame = {
            'state': "True",
            'port' : port
        }
        list_of_urls = []
        for node in blockchain.nodes:
            # if blockchain.first_come[0][0] in node:  # 1등을 제외한 다른노드들에게
            #     continue
            list_of_urls.append(('http://' + node + '/receive_nodesFirstcome', data_frame))  # 1등이 이상한지 아닌지 묻는다.
        with ThreadPoolExecutor(max_workers=10) as pool:
            list(pool.map(post_url, list_of_urls))
    else:
        data_frame = {
            'state': "False"
        }
        requests.post(f'http://127.0.0.1:' + str(s_port) + '/receive_nodesFirstcome',
                      data=json.dumps(data_frame))

    return jsonify(values), 200


@app.route('/validation', methods=['POST'])
def validation():
    values = json.loads(request.get_data())

    mined_port, mined_nonce, mined_previous_hash = values.get("port"), values.get("nonce"), values.get("previous_hash")
    print(str(port)," 가", mined_port," 의 블록을 검증")
    # print("---------------", values.get("previous_hash"))
    # print("===============", blockchain.hash(blockchain.chain[-1]))
    if mined_previous_hash == blockchain.hash(blockchain.chain[-1]):
        if blockchain.valid_proof(mined_port, mined_nonce, mined_previous_hash):
            if [mined_port, mined_nonce] not in blockchain.valid_node:
                blockchain.valid_node.append([mined_port, mined_nonce])
                # 1등이 이상하다는 것을 감지할 때
                if len(blockchain.valid_node) - len(blockchain.first_come) >= int(blockchain.previous_firstcome * blockchain.strange_rate):
                    if port not in blockchain.strange_node :
                        blockchain.strange_node.append(port)
                    data_frame = {
                        'port': port
                    }
                    list_of_urls = []
                    for node in blockchain.nodes:
                        # if blockchain.first_come[0][0] in node:  # 1등을 제외한 다른노드들에게
                        #     continue
                        list_of_urls.append(('http://' + node + '/unreceiveFirstcome', data_frame))  # 1등이 이상한지 아닌지 묻는다.
                    with ThreadPoolExecutor(max_workers=10) as pool:
                        list(pool.map(post_url, list_of_urls))

            if len(blockchain.first_come) == 0:
                blockchain.first_come.append([mined_port, mined_nonce])
            elif blockchain.first_come[0][0] == port:
                if blockchain.bad_first and mined_port != port:
                    print("악성 노드 감지 : ",mined_port)
                else:
                    if [mined_port, mined_nonce] not in blockchain.first_come:
                        blockchain.first_come.append([mined_port, mined_nonce])
                        print("선착순 배열 : ", blockchain.first_come)
                        data_frame = {
                            'first_come': "tobecontinue",
                            'nonce': mined_nonce,
                            'port': mined_port
                        }

                        list_of_urls = []
                        for node in blockchain.nodes:
                            list_of_urls.append(('http://' + node + '/receiveFirstcome', data_frame))
                        with ThreadPoolExecutor(max_workers=10) as pool:
                            list(pool.map(post_url, list_of_urls))

                        # print("--------------------------------------------------------------------",
                        #       blockchain.previous_firstcome)
                        remainNode_len = int(blockchain.previous_firstcome * blockchain.SNR)
                        if len(blockchain.first_come) >= remainNode_len and blockchain.finish_signal:
                            blockchain.new_block(blockchain.first_come[0][1], blockchain.hash(blockchain.chain[-1]),
                                                 blockchain.first_come, blockchain.first_come[0][0])
                            # print("--------------------------------------------------------")
                            # print(blockchain.chain)
                            # print(blockchain.chain[-1])
                            blockchain.finish_signal = False
                            data_frame = {
                                'first_come': blockchain.first_come,
                                'block': blockchain.chain[-1]
                            }

                            list_of_urls = []
                            for node in blockchain.nodes:
                                list_of_urls.append(('http://' + node + '/finish', data_frame))
                            with ThreadPoolExecutor(max_workers=10) as pool:
                                list(pool.map(post_url, list_of_urls))

                            c_round = (len(blockchain.chain) - 1) % 3
                            if c_round == 0:
                                c_round = 3
                            if c_round != 3:
                                blockchain.previous_firstcome = remainNode_len
                            else:
                                blockchain.previous_firstcome = len(blockchain.nodes) + 1
                                blockchain.hash_stop = False
                                blockchain.wallet += 1

                            blockchain.first_come = []
                            blockchain.valid_node = []
                            blockchain.permute_hash = 0

                            data_frame = {
                                'port': port
                            }

                            list_of_urls = []
                            for node in blockchain.nodes:
                                list_of_urls.append(('http://' + node + '/resolve_all',  data_frame))
                            with ThreadPoolExecutor(max_workers=10) as pool:
                                list(pool.map(post_url, list_of_urls))

                            # blockchain.current_transactions = []
                            conclude_transactions = blockchain.chain[-1].get('transactions')
                            blockchain.update_transaction(conclude_transactions)
                            # print("blockchain.current_transactions", blockchain.current_transactions)

        else:
            print(mined_port," 가 채굴 라운드에서 제외되었습니다")
    else :
        if mined_previous_hash != blockchain.hash(blockchain.chain[-1]) :
            # print("mining한 previous_hash가 내 previous_hash와 다를 때")
            print(" ")

    return jsonify(values), 200


@app.route('/resolve_all', methods=['POST'])
def resolve_all():
    blockchain.resolve_conflicts()
    resolve = {
        'resolve': port
    }

    return jsonify(resolve), 200

@app.route('/announce_tx', methods=['POST'])
def announce_tx():
    values = request.get_json()
    for node in blockchain.nodes:
        requests.post(f'http://{node}/receiveTransaction', data=json.dumps(values))
    blockchain.current_transactions.append(values)

    return jsonify(values), 200


@app.route('/receiveTransaction', methods=['POST'])
def receiveTransaction():
    values = json.loads(request.get_data())
    blockchain.current_transactions.append(values)
    # print("receiveTransaction", blockchain.current_transactions)
    return jsonify(values), 200


@app.route('/finish', methods=['POST'])
def finish():
    values = json.loads(request.get_data())
    first_come = values.get("first_come")
    block = values.get("block")
    # print("AAAAAAAAAAAAAAAAAAA", block.get("port"))
    # print("AAAAAAAAAAAAAAAAAAA", block.get("proof"))
    # print("AAAAAAAAAAAAAAAAAAA", block.get("previous_hash"))
    #
    # print(blockchain.valid_proof(block.get("port"), block.get("proof"), block.get("previous_hash")))

    if block.get("port") == blockchain.first_come[0][0]:
        if blockchain.valid_proof(block.get("port"), block.get("proof"), block.get("previous_hash")):
            c_round = len(blockchain.chain) % 3
            if c_round == 0:
                c_round = 3
            if c_round != 3:
                blockchain.previous_firstcome = len(first_come)
            else:
                print("----------------3라운드 종료----------------")
                blockchain.previous_firstcome = len(blockchain.nodes) + 1
                blockchain.hash_stop = False

            blockchain.first_come = []
            blockchain.valid_node = []
            blockchain.chain.append(block)
            blockchain.permute_hash = 0
            # print("들어오냐? 미친련")
            # print("체인있냐?: ", blockchain.chain)
            conclude_transactions = block.get('transactions')
            blockchain.update_transaction(conclude_transactions)
            # print("blockchain.current_transactions", blockchain.current_transactions)

        else:
            print("1등이 보낸 블록이 정당한 블록이 아닙니다")
    else :
        print("다른 1등이 보낸 블록입니다.")

    return jsonify(values), 200


@app.route('/receiveFirstcome', methods=['POST'])
def receiveFirstcome():
    values = json.loads(request.get_data())
    first_come, mined_port, mined_nonce = values.get("first_come"), values.get("port"), values.get("nonce")
    if first_come == "tobecontinue":  # 미구현 방학때 할일
        if [mined_port, mined_nonce] not in blockchain.first_come:
            blockchain.first_come.append([mined_port, mined_nonce])
        print("선착순 배열을 받음 : ", blockchain.first_come)

        remainNode_len = int(blockchain.previous_firstcome * blockchain.SNR)
        if len(blockchain.first_come) >= remainNode_len:
            state = False
            for node in blockchain.first_come:
                if port in node:
                    state = True
            if not state:
                blockchain.hash_stop = True

    return jsonify(values), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain')
def full_chain():
    return render_template('chain.html')


@app.route('/chain/update', methods = ['POST'])
def update_chain():
    return jsonify(blockchain.chain)


@app.route('/nodechain', methods=['GET'])
def node_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register():
    values = json.loads(request.get_data())

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    print("nodes", nodes)  # list타입
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    print("bn", blockchain.nodes)
    return jsonify(response), 201


@app.route('/nodes/help_nodes', methods=['POST'])
def help_nodes():
    values = request.get_json()
    help_node = values.get("nodes")
    data = {
        'port': port
    }
    requests.post(help_node[0] + '/nodes/give_peer', json.dumps(data))
    return jsonify(data), 201


@app.route('/nodes/give_peer', methods=['POST'])
def give_peer():
    values = json.loads(request.get_data())
    new_port = values.get('port')

    new_port_url = "http://127.0.0.1:" + str(new_port)
    data = {
        "nodes": [new_port_url]
    }
    print(blockchain.nodes)
    for node in blockchain.nodes:
        requests.post('http://' + node + '/nodes/register', json.dumps(data))

    help_node = list(blockchain.nodes)
    help_node.append("127.0.0.1:" + str(port))
    print("help_node: ", help_node)
    frame = {
        "nodes": help_node
    }
    requests.post('http://127.0.0.1:' + str(new_port) + '/nodes/register_others', json.dumps(frame))
    blockchain.nodes.add("127.0.0.1:" + str(new_port))
    print("give_peer_block_nodes: ", blockchain.nodes)
    return jsonify(values), 201


@app.route('/nodes/register_others', methods=['POST'])
def register_others():
    values = json.loads(request.get_data())
    blockchain.nodes = set(values.get('nodes'))

    return jsonify(values), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


def thread_start():
    th = threading.Thread()
    th.start()


@app.route('/')
def index():
    return render_template('index.html', title='CPOW', port=port, coin=blockchain.wallet)


if __name__ == '__main__':
    # from argparse import ArgumentParser
    #
    # parser = ArgumentParser()
    # parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    # args = parser.parse_args()
    # port = args.port

    thread_start()
    app.run(host='0.0.0.0', port=port, debug=True)