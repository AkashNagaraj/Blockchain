import time
import hashlib
import json
import random

class Block:
    def __init__(self, timestamp, transactions, previous_hash):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = random.randint(0, 1000000)
    def hash(self):
        return hashlib.sha256(
            json.dumps(self.__dict__).encode('utf-8')
        ).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, [], '0')]
    def create_block(self, transactions):
        previous_hash = self.chain[-1].hash()
        new_block = Block(
            int(time.time()), transactions, previous_hash
        )
        while not new_block.hash().startswith('0000'):
            new_block.nonce += 1
        return new_block
    def mine_block(self):
        new_block = self.create_block([])
        while not self.validate_block(new_block):
            new_block.nonce += 1
        return new_block
    def validate_block(self, block):
        return block.hash().startswith('0000')

def main():
    blockchain = Blockchain()
    block = blockchain.create_block([])
    print(block)
    print(blockchain.validate_block(block))

if __name__=="__main__":
    main()
