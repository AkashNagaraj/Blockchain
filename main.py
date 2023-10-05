import sklearn
from sklearn import preprocessing
import numpy as np
from datetime import date
from cryptography.fernet import Fernet

import collections, csv, json, ast, math, random, sys, time
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt

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



# Encrypt and decrypt the node data 
def decrypt_data(encrypt_data):
    return f.decrypt(encrypt_data).decode()
def encrypt_data(data):
    encrypt = f.encrypt(json.dumps(data, default=str).encode('utf-8'))
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


def build_graph(data):
    G = nx.Graph()
    all_nodes = list(data.keys())
    for node in all_nodes:
        G.add_node(node)
    
    n = len(all_nodes)
    for i in range(n):
        for j in range(i+1,n):
            G.add_edge(all_nodes[i],all_nodes[j])
            G[all_nodes[i]][all_nodes[j]]['weight'] = data[all_nodes[i]]["Total_transactions"] + data[all_nodes[j]]["Total_transactions"]
    
    # Plot the graph along with the edge weights
    #plot_graph(G)   
    return G


def convert_to_text(df):
    df.to_csv('data/graph_features.txt', sep='\t', index=True)


def build_data(csv_file):
    df = pd.read_csv(csv_file)
    df.set_index("Aadhar",inplace=True)
    
    important_columns = ["Gender","Total_transactions","Residence","Age","Avg_Income","Relationship","Bank","Class"]
    df = df[important_columns]
    categorical_columns = df.select_dtypes(exclude=["number"]).columns
    
    label_encoder = preprocessing.LabelEncoder()
    for columns in categorical_columns:
        df[columns] = label_encoder.fit_transform(df[columns])
    
    #print(df.head())
    convert_to_text(df)


def write_nodes(L):
    file = open("data/graph_edges.txt","w")
    for val in L:
        file.write(str(val[0] + "\t" + val[1] + "\n"))


def main():
    n = 4
    convert_to_json("data/Personal_Info.csv","data/Personal_Info.json")
    json_data = read_data("data/Personal_Info.json")
    G = build_graph(json_data)
    build_data("data/Personal_Info.csv")
    write_nodes(G.edges())
    sys.exit()
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

