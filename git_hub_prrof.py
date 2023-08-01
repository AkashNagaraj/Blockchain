import hashlib
import pickle
import random


# Block Structure, note in reality there are a number of different variables in the blockheader see https://bitcoin.org/en/developer-reference#block-headers for more info

block_header = {
    'previousBlockHash': 'effb6c85c6ee147a0f6813f1f6b6f12ffed373cef37a47cd59f4945427872f3d',
    'nonce': 0,
    'transactions': [ # In reality this array of transaction would be captured in a single hash known as the merkle root
        {
            'from': 'Anthony', # From and To would actually be bitcoin addresses
            'to': 'Bill',
            'amount': 10
        },
        {
            'from': 'Bill',
            'to': 'Charles',
            'amount': 10
        },
        {
            'from': 'Charles',
            'to': 'Damien',
            'amount': 10
        }
    ]
}

# Set up, converting json to byte output and hashing that byte output

hashed_block = pickle.dumps(block_header)
m = hashlib.sha256(hashed_block)

# Set difficulty, the difficulty_hash below is the equivalent of requiring 2 zeros at the front of the hash

difficulty_hash = 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
difficult_decimal = 452312848583266388373324160190187140051835877600158453279131187530910662655


# Set Miners involved and their respective CPU's

alice = 3 * ['Alice'] # Represents 3 cpu units for alice
bob = 5 * ['Bob'] # Represents 5 cpu units for bob
charlie = 10 * ['Charlie'] # Represents 10 cpu units for charlie
deborah = 1 * ['Deborah'] # Represents 1 cpu unit for deborah

# Add Miners to an array and shuffle

cpus = [alice, bob, charlie, deborah]
miners = []
for cpu in cpus:
    miners.extend(cpu)
random.shuffle(miners)

# While the hash is bigger than or equal to the difficulty continue to iterate the nonce

while int(m.hexdigest(), 16) >= difficulty_hash:
    block_header['nonce'] += 1 # Increment nonce (ie change your guess)
    m = hashlib.sha256(pickle.dumps(block_header)) # Convert data to byte form so it can be hashed
    print('Nonce Guess: ' + str(block_header['nonce']))
    print('Resultant Hash: ' + str(m.hexdigest()))
    print('Decimal value of hash: ' + str(int(m.hexdigest(), 16)) + '\n')
    miner = miners[block_header['nonce'] % len(miners)] # The miner who mined the block
    block_hash = m.hexdigest() # The hash of the blockheader with that nonce yields the block hash for that block


print('Valid Hash: ' + str(int(m.hexdigest(), 16)) + ' is less than ' + str(difficulty_hash))
print('Miner who Mined Block: ' + miner)
