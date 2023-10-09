import sklearn
from itertools import combinations
from sklearn import preprocessing
import numpy as np
from datetime import date
from cryptography.fernet import Fernet
from create_dataset import build_random_dataset

import collections, csv, json, ast, math, random, sys, time
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt
sys.path.insert(1,"/home/akash/Desktop/Sem3/Project/Blockchain/torchGCN")
from train import train_model

key = Fernet.generate_key()
f = Fernet(key)


def get_answer(v1):
    # Randomly select true or false or get input from another user on another server
    #return random.choice([True, False])
    return True


# Implement proof of stake to accept a new node
def accept_new_node():
    
    print(" Verifying a new node by implementing proof of stake based on the number of transactions performed")
    existing_df = pd.read_csv("data/dataset.csv")
    aadhar_details = existing_df["Aadhar"]
    node_class = existing_df["Class"]
    transaction_count = existing_df["Total_transaction"]

    d = dict(zip(aadhar_details,transaction_count))
    all_transactions = list(collections.Counter(d).elements())
    start_time = time.time()
    idx = random.randint(0,len(all_transactions)-1)
    chosen_person = all_transactions[idx]
    class_type = existing_df.loc[existing_df["Aadhar"]==chosen_person,"Class"]

    return get_answer(chosen_person), class_type


def new_node_features():
    
    df = pd.read_csv("data/temp_node.csv")
    important_columns = ["Gender","Total_transaction","Residence","Age","Avg_Income","Relationship","Bank"]
    df = df[important_columns]
    df["Gender"].replace(["girl","boy"],[1,2],inplace=True)
    df["Residence"].replace(["Chennai","Delhi","Mumbai","Bangalore","Kolkata"],[1,2,3,4,5],inplace=True)
    df["Relationship"].replace(["Single","Married"],[1,2],inplace=True)
    df["Bank"].replace(["ICICI","Axis","SBI","Canara"],[1,2,3,4],inplace=True)
    features = df.to_numpy()
    return features


def get_new_node():
    read_new_node()
    features = new_node_features()
    return features


def read_new_node():
    name = input("Enter your name : ")
    gender = input("Enter your gender [girl/boy/other] : ")
    aadhar = input("Enter your 16 digit aadhar number : ")
    total_transactions = 0
    phone_num = input("Enter your phone number : ")
    residence = input("Enter your city [Bangalore,Kolkata,Chennai,Delhi] : ")
    age = int(input("Enter your age : "))
    avg_income = int(input("Enter your yearly income in lakhs : "))
    relationship = input("Enter your relationship [Single/Married] : ")
    bank = input("Enter your bank name[ICICI,SBI,Axis,Canara] : ")
    df = pd.DataFrame({"Name":name,"Gender":gender,"Aadhar":aadhar,"Total_transaction":0,"Phone_Number":phone_num,"Residence":residence,"Age":age,"Avg_Income":avg_income,"Relationship":relationship,"Bank":bank},index=[0])
    df.to_csv("data/temp_node.csv",index=False)


# Encrypt and decrypt the node data 
def decrypt_data(encrypt_data):
    return f.decrypt(encrypt_data).decode()
def encrypt_data(data):
    encrypt = f.encrypt(json.dumps(data, default=str).encode('utf-8'))
    #encypt = f.encrypt(data)
    return encrypt


def convert_to_json(csvFilePath, jsonFilePath):

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Aadhar']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def read_data(file):
    f = open(file)
    data = json.load(f)
    return(data) 


# Add the initial n nodes to the network 
def initialize_blockchain(n):
    dataframe = read_data()
    
    convert_to_json("data/Personal_Info.csv","data/Personal_Info.csv")
    blockchain_network = []
    sys.exit()

    for i in range(n):
        encrypted_data = encrypt_data(data)
        print("The current data is : {}, encypted as : {}".format(data, encrypted_data))
        blockchain_network.append(encrypted_data)
    return blockchain_network


def plot_graph(G):
    pos = nx.circular_layout(G)
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()


def build_graph():
    G = nx.Graph()
    df = pd.read_csv("data/dataset.csv")
    all_nodes = df.index
    
    for node in all_nodes:
        G.add_node(node)
    
    edges = list(combinations(all_nodes,2))
    for edge in edges:
        G.add_edge(edge[0],edge[1])
        G[edge[0]][edge[1]]["weight"] = df.iloc[edge[0]]["Total_transaction"] + df.iloc[edge[1]]["Total_transaction"] 
     
    # Plot the graph along with the edge weights
    # plot_graph(G)   
    return G


def convert_to_text(df):
    df.to_csv('data/graph_data/graph.features', sep='\t',header=False, index=True)


def build_graph_features(csv_file):
    df = pd.read_csv(csv_file)
    df.set_index("Index",inplace=True)
    
    important_columns = ["Gender","Total_transaction","Residence","Age","Avg_Income","Relationship","Bank","Class"]
    df = df[important_columns]
    
    df["Gender"].replace(["girl","boy"],[1,2],inplace=True)
    df["Residence"].replace(["Chennai","Delhi","Mumbai","Bangalore","Kolkata"],[1,2,3,4,5],inplace=True)
    df["Relationship"].replace(["Single","Married"],[1,2],inplace=True)
    df["Bank"].replace(["ICICI","Axis","SBI","Canara"],[1,2,3,4],inplace=True)

    convert_to_text(df)
    

def write_nodes(L):
    file = open("data/graph_data/graph.edges","w")
    for val in L:
        file.write(str(str(val[0]) + "\t" + str(val[1]) + "\n"))


def add_to_existing_dataframe(node_type):
    df1 = pd.read_csv("data/dataset.csv")
    df2 = pd.read_csv("data/temp_node.csv")
    df2["Class"] = node_type
    df2["Index"] = df1.shape[0]
    print(df2)
    new_df = pd.concat([df1,df2])
    new_df.set_index("Index")
    new_df.to_csv("data/dataset.csv",index=False) 


def write_hash_to_file(L):
    # open file in write mode
    with open(r'data/hash_values.txt', 'w') as fp:
        for item in L:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')


def build_chain():
    df = pd.read_csv("data/dataset.csv")

    previous_hash = [0]
    initial_data = df.iloc[0].to_dict()
    block_data = {"time":time.time(),"previous_hash":previous_hash[-1],"data":initial_data}
    hashed_data = encrypt_data(block_data) # decrypt_data(hashed_data)
    previous_hash.append(hashed_data)

    for idx in range(1,df.shape[0]):
        data = df.iloc[idx].to_dict()
        block_data = {"time":time.time(),"previous_hash":previous_hash[-1],"data":data}
        hashed_data = encrypt_data(block_data)
        print("The block data is :", block_data)
        print("The decrypted value is :", decrypt_data(hashed_data))
        previous_hash.append(hashed_data)

    return previous_hash


def append_blockchain(hashed_chain):
    df = pd.read_csv("data/dataset.csv")
    data = df.iloc[-1].to_dict()
    block_data = {"time":time.time(),"previous_hash":hashed_chain[-1],"data":data}
    hashed_data = encrypt_data(block_data) # decrypt_data(hashed_data)
    hash_chain.append(hashed_data)
    return hash_chain


def main():
    # Build a random dataset 
    n = int(input("Enter number of users : "))
    build_random_dataset(n)
   
    # Build a blockchain
    hashed_chain = build_chain()
    
    check = True
    while check:
        # Convert csv to graph
        G = build_graph()
    
        # Add edges and nodes in the graph
        categorical_codes = build_graph_features("data/dataset.csv")
        write_nodes(G.edges())
    
        # Get new node
        new_node_features = get_new_node()
    
        # Train the graph
        # print("The new node features are:",new_node_features)
        # train_model(new_node_features)

        # Proof of stake to add it to the graph
        validation, class_type = accept_new_node()
        
        if validation:
            add_to_existing_dataframe(class_type)    
            hashed_chain = append_blockchain(hashed_chain)
        else:
            print("The node has been rejected by PoS")

        choice = input("Validate some more nodes [Y/N]? : ")

        if choice=="N":
            check=False

    write_hash_to_file(hashed_chain)

    print("Halting execution")

main()

"""
Questions
1) How will it prevent hackers from entering the blockchain [Data is hashed]
2) Edge weight [transaction count]
3) Features [phone number, place, card limit, age, gender, avg income, single/married, card company]
4) Finally detect how far node is from the initial blockchain nodes [semi supervised classification problem]
"""

