import json
import time
import hashlib

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__,sort_keys=True)
        sha_signature = hashlib.sha256(block_string.encode()).hexdigest()
        return sha_signature
    
    @property
    def last_block(self):
        return self.chain[-1]

def main():
    
    chains = []
    index = 0
    transactions = 1
    timestamp = time.time()
    print("Building first block")
    block = Block(index, transactions, timestamp, None, nonce=0) 
    chains.append(block.compute_hash())

    while True:
        index += 1
        transactions += 1
        timestamp = time.time()
        previous_hash = chains[-1]
        block = Block(index, transactions, timestamp, previous_hash, nonce=0)
        chains.append(block.compute_hash())

        check = str(input("Do you want to continue : [Y/N]"))
        if check=="N":
            break

    print(chains)

if __name__=="__main__":
    main()
