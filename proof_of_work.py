# https://www.geeksforgeeks.org/implementing-the-proof-of-work-algorithm-in-python-for-blockchain-mining/
import hashlib
import datetime

class Block:
    def __init__(self,data,previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8')+
                    str(self.previous_hash).encode('utf-8')+
                    str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self,target_difficulty):
        while self.hash[:len(target_difficulty)] != target_difficulty:
            print(self.hash)
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined:",self.hash)

# genesis_block = Block("Genesis Block", "0")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_gensis_block()]

    def create_gensis_block(self):
        return Block("Genesis Block","0")

    def add_block(self,new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.mine_block("0000")
        self.chain.append(new_block)


blockchain = Blockchain()

block1 = Block("Transaction data 1","")
blockchain.add_block(block1)

block2 = Block("Transaction data 2","")
blockchain.add_block(block2)

block3 = Block("Transaction data 3","")
blockchain.add_block(block3)
