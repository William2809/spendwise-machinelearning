import numpy as np
import json
from sklearn.linear_model import LinearRegression
expenses=np.zeros((7,52))
incomes=np.zeros((7,52))
first_transaction=True 
place=0

def apicall(buffer, day, week_budget):  
    global bool, place
    bool=False 
    
    i=0 
    for elt in incomes[day]:
        if elt==0 : 
            incomes[day][i]=week_budget/7 
            i+=1
            break 
        i+=1
    place=i 
    transactions = []  # create an empty list to hold all transactions for this day
    for elt in buffer: 
        transactions.append(elt["amount"])  # add the transaction amount to the list
    avg_transaction = sum(transactions) / len(transactions)  # calculate the average transaction amount
    for i in range(place):  # update the expenses array with the average transaction amount
        expenses[day][i] = avg_transaction

def json_to_numpy(parsed_json, day): #add to the numpy expenses the data for one jsonfile and the day is the position of the day in the week 
    """
    Converts a json file to a numpy expenses.
    """
    global bool
    
    i=0 #counter for the expenses
    for transaction in parsed_json:  # iterate over each transaction in parsed_json
        if expenses[day][i] == 0 or bool:  # if we are the first transaction or bool is True
            bool = True
            expenses[day][i] += transaction["amount"]  # add the amount to the expenses
        i += 1

def train_model(day): 
    income = incomes[day,:place].reshape(-1, 1)
    expense = expenses[day,:place]
    model = LinearRegression()
    model.fit(income, expense)
    new_income = np.array([[sum(incomes[day,:place])/len(incomes[day,:place])]]) 
    predicted_budget = model.predict(new_income)
    return predicted_budget[0] 

def weekly_budget(week_number): 
    addition=0
    for elt in expenses:
        addition+=elt[week_number-1]
    return addition
