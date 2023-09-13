import numpy as np
from datetime import date
from cryptography.fernet import Fernet
import json, ast

import pandas as pd
import math
import random
import sys

key = Fernet.generate_key()
f = Fernet(key)


# Implement proof of stake to accept a new node
def accept_new_node(initial_graph_data):
    print("Accepting a new node by implementing proof of stake based on the number of transactions performed")
    
    transaction_count = {}

    for val in initial_graph_data[:10]:
        transaction_count[ast.literal_eval(decrypt_data(val))["aadhar"]] = int(ast.literal_eval(decrypt_data(val))["transaction_count"])
   
    print(list(transaction_count))
    
    # add the chosen persons id to every node
    # accept the person within time t
    # use backup person


def get_new_node():
    name = input("Enter your name : ")
    gender = input("Enter your gender [girl/boy/other]: ")
    try:
        year, month, day = map(int, input("Enter your DOB in the format - [yyyy:mm:dd] ").split(":"))
        DOB = date(year,month,day)
    except:
        print("The DOB data was not entered accurately")  
    aadhar = input("Enter your 16 digit aadhar number")
    new_node = {"name":name,"gender":gender,"DOB":DOB,"aadhar":aadhar,"transaction_count":0}
    return new_node


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
    transaction_count = random.randint(1,25)
    random_data = {"name":df.iloc[idx][0], "gender":df.iloc[idx][1], "DOB":birth_date, "aadhar":get_aadhar(), "transaction_count":transaction_count}
    return(random_data)


# Encrypt and decrypt the node data 
def decrypt_data(encrypt_data):
    return f.decrypt(encrypt_data).decode()
def encrypt_data(data):
    encrypt = f.encrypt(json.dumps(data, default=str).encode('utf-8'))
    return encrypt


# Add the initial n nodes to the network 
def initialize_blockchain(n):
    blockchain_network = []
    for i in range(n):
        data = get_random_values()
        blockchain_network.append(encrypt_data(data))
    return blockchain_network


def create_graph(n):
    random_matrix = np.random.rand(n,n)
    adjacency_matrix = (random_matrix + random_matrix.T)/2
    return adjacency_matrix


def main():
    n = 10
    initial_graph_data = initialize_blockchain(n)
    adjacency_matrix = create_graph(n)
    new_node = get_new_node()
    accept_new_node(initial_graph_data)


main()

"""
Questions
1) How will it prevent hackers from entering the blockchain
2) 
"""
