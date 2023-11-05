from train import train_model, predict
from itertools import combinations
import pandas as pd
#import numpy as np
from cryptography.fernet import Fernet

import collections, csv, json, random, sys, time, re
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt


key = Fernet.generate_key()
f = Fernet(key)


def update_transaction_count(user_id,choice,GCN_prediction):
    df = pd.read_csv("data/dataset.csv") 
    index = df.loc[df["Aadhar"]==user_id]["Index"]
    print("Transaction count before :",df.loc[index,"Total_transaction"].item())
    if choice==1 and GCN_prediction==0:
        update = -5
    elif choice==1 and GCN_prediction==1:
        update = 2
    else:
        update = 0
    
    current_count = df.loc[index,"Total_transaction"].item()
    updated_count = max(0,current_count + update)
    df.loc[index,"Total_transaction"] = updated_count
    df.to_csv("data/dataset.csv",index_label=False) 
    print("Transaction count after :",df.loc[index,"Total_transaction"].item())


def get_answer(user_id,model_prediction):
    # Randomly select true or false or get input from another user on another server
    print("The GCN models prediction is : ",model_prediction.item())
    choice = random.choice([0,1])
    print("The choice is : ",choice)
    GCN_prediction = model_prediction.item()
    update_transaction_count(user_id,choice,GCN_prediction)
    return choice


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


def is_valid_card(num):
  if len(num) > 12 or len(num) < 12:
      return False
  else:
      if num[0] == '0' or num[0] == '1':
          return False
      else:
          try:
              num = int(num)
              return True
          except:
              return False


def valid_phone(num):
  Pattern = re.compile("[6-9][0-9]{9}")

  if Pattern.match(num):
      return True
  else:
    return False


def read_new_node():
    name = input("Enter your name : ")
    gender = input("Enter your gender [girl/boy/other] : ")
    aadhar = input("Enter your 12 digit aadhar number : ")
    total_transactions = 0
    phone_num = input("Enter your 10 digit phone number : ")
    residence = input("Enter your city [Bangalore,Kolkata,Chennai,Delhi] : ")
    age = int(input("Enter your age : "))
    avg_income = int(input("Enter your yearly income in lakhs : "))
    relationship = input("Enter your relationship [Single/Married] : ")
    bank = input("Enter your bank name[ICICI,SBI,Axis,Canara] : ")
    if is_valid_card(aadhar) and valid_phone(phone_num):
        df = pd.DataFrame({"Name":name,"Gender":gender,"Aadhar":aadhar,"Total_transaction":0,"Phone_Number":phone_num,"Residence":residence,"Age":age,"Avg_Income":avg_income,"Relationship":relationship,"Bank":bank},index=[0])
        df.to_csv("data/temp_node.csv",index=False)
    else:
        print("The entered phone number or aadhar is incorrect")


def append_blockchain(hashed_chain):
    df = pd.read_csv("data/dataset.csv")
    data = df.iloc[-1].to_dict()
    block_data = {"time":time.time(),"previous_hash":hashed_chain[-1],"data":data}
    hashed_data = encrypt_data(block_data) # decrypt_data(hashed_data)
    hashed_chain.append(hashed_data)
    return hashed_chain


def accept_new_node(predicted_class):
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
    
    #class_type = existing_df.loc[existing_df["Aadhar"]==chosen_person,"Class"]
    class_type = get_answer(chosen_person,predicted_class)

    return class_type


def add_to_existing_dataframe(node_type):
    df1 = pd.read_csv("data/dataset.csv")
    df2 = pd.read_csv("data/temp_node.csv")
    df2["Class"] = node_type
    df2["Index"] = df1.shape[0]
    new_df = pd.concat([df1,df2])
    new_df.set_index("Index")
    new_df.to_csv("data/dataset.csv",index=False)


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
        previous_hash.append(hashed_data)

    return previous_hash


def encrypt_data(data):
    encrypt = f.encrypt(json.dumps(data, default=str).encode('utf-8'))
    return encrypt


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


def update_graph():
    check = "Y"

    while check=="Y":
        # Build the blockchain
        hashed_chain = build_chain()
        # Train the model
        train_model()
        # Get new data
        read_new_node()
        new_features = new_node_features()
        print("The new node features are :",new_features)
        # Predict new data
        # Inside the try block
        #try:
        predicted_class = predict(new_features)
        class_type = accept_new_node(predicted_class)

        if class_type==1:
            add_to_existing_dataframe(class_type)    
            hashed_chain = append_blockchain(hashed_chain)
            G = build_graph()
            build_graph_features("data/dataset.csv")
            write_nodes(G.edges())
        else:
            print("The node has been rejected by PoS")
        #except Exception as e:
        #    print("The information you have entered is incorrect please try again.")
        #    print("The exception is :",e)
        # Outside the try block
        check = input("Do you want to continue : [Y/N]")

update_graph()
