from datetime import date

import pandas as pd
import math
import random
import sys


def accept_new_node():
    print("Accepting a new node")
    # implement proof of stake
    # add the chosen persons id to every node
    # accept the person within time t
    # use backup person


def get_new_node():
    print("Accepting data from user/node")
    # read data from user
    # verify data 

def get_aadhar():
    s = ""
    for i in range(16):
        s += str(random.randint(1,9))
    return int(s) 

def get_random_values():
    
    # Name
    df = pd.read_csv("data/names.csv")
    idx = math.ceil(random.random()*df.shape[0])
    
    # Birthdate
    year = random.randint(1980,2005)
    month = random.randint(1,12)
    if month==2:
        day = random.randint(1,28)
    else:
        day = random.randint(1,30)
    try:
        birth_date = date(year,month,day)
    except:
        print("Year : {}, Month : {}, Day : {}".format(year,month,day))
        sys.exit()

    # Aadhar Number 
    random_data = {"name":df.iloc[idx][0], "gender":df.iloc[idx][1], "DOB":birth_date, "aadhar":get_aadhar(), "transaction_count":0}
    return(random_data)

# Add the initial n nodes to the network 
def initialize_blockchain(n):
    blockchain_network = []
    for i in range(n):
        data = get_random_values()
        blockchain_network.append(data)
    return blockchain_network


def main():
    n = 1000
    data = initialize_blockchain(n)
    print(data)

    """
    get_new_node()
    accept_new_node()
    """

main()
"""
Questions
1) How will it prevent hackers from entering the blockchain
2) 
"""
