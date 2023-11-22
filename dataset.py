import pandas as pd
import random, sys

def random_aadhar():
    S = str(random.choice([2,3,4,5,6,7,8,9]))
    for i in range(11):
        S+=str(random.randint(1,9))
    return int(S)

def random_number():
    S = "9"
    for i in range(9):
        S+=str(random.randint(0,9))
    return int(S)

def random_name_gender():
    df = pd.read_csv("data/names.csv")
    r, c = df.shape
    idx = random.randint(0,r)
    return df["Name"][idx], df["Gender"][idx]

def random_transaction_count():
    return random.randint(2,10)

def random_residence():
    L = ["Chennai","Delhi","Mumbai","Bangalore","Kolkata","Hyderabad"]
    return L[random.randint(0,len(L)-1)]

def random_age(): 
    return random.randint(18,40)

# Income is in Lakhs
def random_income():
    return random.randint(2,15)

def random_relationship():
    L = ["Single","Married"]
    return L[random.randint(0,len(L)-1)]    

def random_bank():
    L = ["ICICI","Axis","SBI","Canara"]
    return L[random.randint(0,len(L)-1)]

def random_class():
    return random.randint(0,1)

def build_random_dataset(n):
    
    aadhar, number, name, gender, transaction_count, residence, age, income, relationship, bank, category = [],[],[],[],[],[],[],[],[],[],[] 
    for i in range(n):
        aadhar.append(random_aadhar())
        number.append(random_number())
        n,g = random_name_gender()
        name.append(n)
        gender.append(g)
        transaction_count.append(random_transaction_count())
        residence.append(random_residence())
        age.append(random_age())
        income.append(random_income())
        relationship.append(random_relationship())
        bank.append(random_bank())
        category.append(random_class())
    
    df = pd.DataFrame({"Name":name,"Gender":gender,"Aadhar":aadhar,"Total_transaction":transaction_count,"Phone_Number":number,
        "Residence":residence,"Age":age,"Avg_Income":income,"Relationship":relationship,"Bank":bank,"Class":category})
    df.index.name = "Index" 
    df.to_csv("data/dataset.csv",index=True)

#build_random_dataset(400)
