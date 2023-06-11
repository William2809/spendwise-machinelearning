import numpy as np
import json
from sklearn.linear_model import LinearRegression
expenses=np.arange(364).reshape(7,52)
expenses.fill(0)
incomes=np.arange(364).reshape(7,52)
incomes.fill(0)
bool=False 
place=0
def apicall(buffer,day,week_budget):  #buffer contains the name of the json files and the day is the position of the day in the week 
    # day=0 is monday, day=1 is tuesday, etc...
    """ 
    Calls the API to get the data assign the budget per day
    """
    global bool,place
    bool=False #if we are the first json file => bool=False 
    
    i=0 #counter for the incomes
    for elt in incomes[day]:
        if elt==0 : #we add the daily budget on the first 0 we meet
            incomes[day][i]=week_budget/7 #add the amount to the expenses
            i+=1
            break #daily budget added we can break the loop
        i+=1
    place=i #save the place of the first 0 so the end of the data filled
    for elt in buffer: #for each json file
        json_to_numpy(elt,day)
        
def json_to_numpy(json_file,day): #add to the numpy expenses the data for one jsonfile and the day is the position of the day in the week 
    """
    Converts a json file to a numpy expenses.
    """
    global bool
    
    with open(json_file) as jsonfile: #parse the json file
        file = jsonfile.read()
    parsed_json = json.loads(file)
    
    i=0 #counter for the expenses
    for elt in expenses[day]:
        if elt==0 or bool: #if we are the first json file => bool=False so we take the first 0 value
            bool=True
            expenses[day][i]+=parsed_json["Amount"] #add the amount to the expenses
            break #json file is treated so we can stop the loop
        i+=1

def train_model(day): #add the data for the day to the model
    """
    Trains a linear regression model using the given data.
    """
    income = incomes[day,:place].reshape(-1, 1) #reshape the data to fit the model
    expense = expenses[day,:place]
    model = LinearRegression()
    model.fit(income, expense)
    new_income = np.array([[sum(incomes[day,:place])/len(incomes[day,:place])]])  # new day incomes = average
    predicted_budget = model.predict(new_income)
    return predicted_budget[0] #prediction of the day

def weekly_budget(week_number): #addition for the week of number week_number
    """
    Calculates the weekly budget using the daily budget.
    """
    addition=0
    for elt in expenses:
        addition+=elt[week_number-1]
    return addition