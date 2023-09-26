import numpy as np
from datetime import date
from cryptography.fernet import Fernet

import collections, json, ast, math, random, sys, time
import pandas as pd

key = Fernet.generate_key()
f = Fernet(key)


def get_answer(v1,v2):
    return True


# Implement proof of stake to accept a new node
def accept_new_node(new_node, initial_graph_data):
    print("Accepting a new node by implementing proof of stake based on the number of transactions performed")
    
    # transaction_count has aadhar:no_transactions as a dictionary
    transaction_count = {}
    for val in initial_graph_data[:10]:
        transaction_count[ast.literal_eval(decrypt_data(val))["aadhar"]] = int(ast.literal_eval(decrypt_data(val))["transaction_count"])
   
    all_transactions = list(collections.Counter(transaction_count).elements())
    start_time = time.time()
    idx = random.randint(0,len(all_transactions))
    chosen_person1 = all_transactions[idx]
    
    remaining_transactions = [val for val in all_transactions if val != chosen_person1]
    idx = random.randint(0,len(all_transactions))
    chosen_person2 = remaining_transactions[idx]
    
    if get_answer(chosen_person1, chosen_person2)==True:
        return chosen_person1
    else:
        return new_node["aadhar"]


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
        encrypted_data = encrypt_data(data)
        print("The current data is : {}, encypted as : {}".format(data, encrypted_data))
        blockchain_network.append(encrypted_data)
    return blockchain_network


def create_graph(n):
    random_matrix = np.random.rand(n,n)
    #random_matrix = (random_matrix + random_matrix.T)/2
    return random_matrix


def update_graph():
    return    


def main():
    n = 4
    initial_graph_data = initialize_blockchain(n)
    adjacency_matrix = create_graph(n)
    new_node = get_new_node()
    connection = accept_new_node(new_node,initial_graph_data)
    if connection!=new_node["aadhar"]:
        update_graph()

main()

"""
Questions
1) How will it prevent hackers from entering the blockchain [Data is hashed]
2) Edge weight [transaction count]
3) Features [phone number, place, card limit, age, gender, avg income, single/married, card company]
4) Finally detect how far node is from the initial blockchain nodes [semi supervised classification problem]
"""

