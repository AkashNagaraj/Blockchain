from __future__ import division
from __future__ import print_function

import pandas as pd
import time
import argparse
import numpy as np

import torch
import torch.nn.functional as F
import torch.optim as optim

from utils import load_data, accuracy
from models import GCN

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='Disables CUDA training.')
parser.add_argument('--fastmode', action='store_true', default=False,
                    help='Validate during training pass.')
parser.add_argument('--seed', type=int, default=42, help='Random seed.')
parser.add_argument('--epochs', type=int, default=200,
                    help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=0.01,
                    help='Initial learning rate.')
parser.add_argument('--weight_decay', type=float, default=5e-4,
                    help='Weight decay (L2 loss on parameters).')
parser.add_argument('--hidden', type=int, default=16,
                    help='Number of hidden units.')
parser.add_argument('--dropout', type=float, default=0.5,
                    help='Dropout rate (1 - keep probability).')

args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

#np.random.seed(args.seed)
torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

# Load data
adj, features, labels, idx_train, idx_val, idx_test = load_data()

# Model and optimizer
model = GCN(nfeat=features.shape[1],
            nhid=args.hidden,
            nclass=labels.max().item() + 1,
            dropout=args.dropout)
optimizer = optim.Adam(model.parameters(),
                       lr=args.lr, weight_decay=args.weight_decay)

if args.cuda:
    model.cuda()
    features = features.cuda()
    adj = adj.cuda()
    labels = labels.cuda()
    idx_train = idx_train.cuda()
    idx_val = idx_val.cuda()
    idx_test = idx_test.cuda()


def train(epoch):
    t = time.time()
    model.train()
    optimizer.zero_grad()
    output = model(features, adj)
    loss_train = F.nll_loss(output[idx_train], labels[idx_train])
    acc_train = accuracy(output[idx_train], labels[idx_train])
    loss_train.backward()
    optimizer.step()

    if not args.fastmode:
        # Evaluate validation set performance separately,
        # deactivates dropout during validation run.
        model.eval()
        output = model(features, adj)

    loss_val = F.nll_loss(output[idx_val], labels[idx_val])
    acc_val = accuracy(output[idx_val], labels[idx_val])
    print('Epoch: {:04d}'.format(epoch+1),
          'loss_train: {:.4f}'.format(loss_train.item()),
          'acc_train: {:.4f}'.format(acc_train.item()),
          'loss_val: {:.4f}'.format(loss_val.item()),
          'acc_val: {:.4f}'.format(acc_val.item()),
          'time: {:.4f}s'.format(time.time() - t))


def test():
    model.eval()
    output = model(features, adj)
    loss_test = F.nll_loss(output[idx_test], labels[idx_test])
    acc_test = accuracy(output[idx_test], labels[idx_test])
    print("Test set results:",
          "loss= {:.4f}".format(loss_test.item()),
          "accuracy= {:.4f}".format(acc_test.item()))
    # Save the model 
    torch.save(model.state_dict(),"data/model_weights.pt")


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


def predict(node_data):
    #node_data = new_node_features()
    input_features = torch.tensor(node_data,dtype=torch.float32)
    adj, features, labels, idx_train, idx_val, idx_test = load_data()
    model = GCN(7, 16, 2, 0.3) #  nfeat, nhid, nclass, dropout
    model.load_state_dict(torch.load("data/model_weights.pt"))
    df = pd.read_csv("data/dataset.csv")
    dummy_tensor = torch.randn((df.shape[0],7),dtype=torch.float32)
    dummy_tensor[0] = torch.tensor(node_data,dtype=torch.float32)
    output = model(dummy_tensor,adj)
    m = torch.nn.Softmax(dim=1)
    first_element = m(output)[0]
    print("The class is :",torch.argmax(first_element))
    return torch.argmax(first_element)


# Train model
def train_model():
    t_total = time.time()
    for epoch in range(args.epochs):
        train(epoch)
    print("Optimization Finished!")
    print("Total time elapsed: {:.4f}s".format(time.time() - t_total))
    # Testing
    test()

#train_model()
