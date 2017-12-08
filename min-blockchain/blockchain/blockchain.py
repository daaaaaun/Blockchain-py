import json
from hashlib import sha256
from time import time
from urllib.parse import urlparse


class Blockchain:
    DEFAULT_VERSION = '1.0'

    def __init__(self):
        """
        Initializes Chain, Nodes, Current Transactions
        """
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create genesis block
        self.new_block(100, '1')

    def register_node(self, address):
        self.nodes.add(urlparse(address).netloc)

    def new_block(self, nonce, prevhash):
        """
        Creates new block

        :param nonce: Block's nonce
        :param prevhash: Previous block's hash

        :return: Created block
        :rtype: dict
        """
        block = {
            'version': self.DEFAULT_VERSION,
            'prevhash': prevhash or self.hash_block(self.chain[-1]),
            'transactions': self.current_transactions,
            # Change to merkle tree's hash is better
            'timestamp': time(),
            'nonce': nonce
            # bits, hash required
        }

        self.current_transactions.clear()
        # Clear transactions to generate new block
        self.chain.append(block)
        # Append block to chain

        return block

    @staticmethod
    def hash_block(block):
        """
        Hashes the block by two times of sha256 algorithm

        :param block: Non-hashed block dictionary
        :type block: dict

        :return: Hashed block's hexdigest
        :rtype: str
        """
        block_str = json.dumps(block, sort_keys=True).encode()

        return sha256(sha256(block_str).digest()).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        """
        Adds new transaction to block

        :param sender: Sender's wallet ID of transaction
        :type sender: str
        :param recipient: Recipient wallet ID of transaction
        :type recipient: str
        :param amount: Amount of transaction
        :type amount: int

        :return: None
        :rtype: None
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @property
    def last_block(self):
        """
        Returns most recent block of chain

        :return: Most recent block of chain
        :rtype: dict
        """
        return self.chain[-1]

    def proof_of_work(self, prev_nonce):
        """
        Finds current block's nonce

        :param prev_nonce: Last block's nonce
        :type prev_nonce: int

        :return: nonce
        :rtype: int
        """
        nonce = 0
        while self.is_valid_nonce(prev_nonce, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def is_valid_nonce(prev_nonce, nonce):
        """
        Checks nonce is valid

        :param prev_nonce: Previous block's nonce
        :param nonce: Current block's nonce

        :return: Whether nonce is valid
        :rtype: bool
        """
        guess = '{0}{1}'.format(prev_nonce, nonce).encode()
        guess_hash = sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'
