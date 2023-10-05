import random, sys

def random_aadhar():
    S = ""
    for i in range(16):
        S+=str(random.randint(1,9))
    return int(S)

def random_number():
    S = "9"
    for i in range(9):
        S+=str(random.randint(0,9))
    return int(S)

def random_name():
    df = pd.read_csv("data/names.csv")
    r, c = df.shape
    idx = random.randint(0,r)
    return df["names"][idx]

def random_gender():
    L = ["G","B"]
    return L[random.randint(0,len(L))]

def random_transaction_count():
    return random.randint(2,10)

def random_residence():
    L = ["Chennai","Delhi","Mumbai","Bangalore","Kolkata"]
    return L[random.randint(0,len(L)]

def random_age(): 
    return random.randint(18,40)

# Income is in Lakhs
def random_income():
    return random.randint(2,15)

def random_relationship():
    L = ["Single","Married"]
    return L[random.randint(0,len(L)]    

def random_bank():
    L = ["ICICI","Axis","SBI","Canara"]
    return L[random.randint(0,len(L)]

def random_class():
    return random.randint(0,1)

def create_dataset():
    random_aadhar()
    random_number()
    random_name()
    random_gender()
    random_transaction_count()
    random_residence()
    random_age()
    random_income()
    random_relationship()
    random_bank()
    random_class()


def main():
    create_dataset()


if __name__=="__main__":
    main()
