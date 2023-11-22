from itertools import combinations
from dataset import build_random_dataset
import time
import csv
import pandas as pd
import networkx as nx
import sys
import matplotlib.pyplot as plt


def plot_graph(G):
    pos = nx.circular_layout(G) # circular,spring,random
    nx.draw_networkx(G,pos,node_color="darkmagenta")
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    #plt.show()
    plt.savefig("graph.png")


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
    plot_graph(G)   
    return G


def convert_to_text(df):
    df.to_csv('data/graph_data/graph.features', sep='\t',header=False, index=True)


def build_graph_features(csv_file):
    df = pd.read_csv(csv_file)
    df.set_index("Index",inplace=True)
    
    important_columns = ["Gender","Total_transaction","Residence","Age","Avg_Income","Relationship","Bank","Class"]
    df = df[important_columns]
    
    df["Gender"].replace(["girl","boy"],[1,2],inplace=True)
    df["Residence"].replace(["Chennai","Delhi","Mumbai","Bangalore","Kolkata","Hyderabad"],[1,2,3,4,5,6],inplace=True)
    df["Relationship"].replace(["Single","Married"],[1,2],inplace=True)
    df["Bank"].replace(["ICICI","Axis","SBI","Canara"],[1,2,3,4],inplace=True)

    convert_to_text(df)
    

def write_nodes(L):
    file = open("data/graph_data/graph.edges","w")
    for val in L:
        file.write(str(str(val[0]) + "\t" + str(val[1]) + "\n"))


def write_hash_to_file(L):
    # open file in write mode
    with open(r'data/hash_values.txt', 'w') as fp:
        for item in L:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')


def main():
    # Build a random dataset 
    n = int(input("Enter number of users : "))
    start = time.time()
    build_random_dataset(n)
    end = time.time()
    
    print("The total seconds taken to build the dataset : ",(end-start))
    G = build_graph()
    build_graph_features("data/dataset.csv")
    write_nodes(G.edges())

    print("Completed Building Graph")

main()

"""
Questions
1) How will it prevent hackers from entering the blockchain [Data is hashed]
2) Edge weight [transaction count]
3) Features [phone number, place, card limit, age, gender, avg income, single/married, card company]
4) Finally detect how far node is from the initial blockchain nodes [semi supervised classification problem]
"""

