from flask import Flask, request;

app = Flask(__name__);
from api.utils import apicall, train_model;

# 
# flask --app app run --port=5001

@app.route('/')
def test():
    return {
        'messages': "Welcome to spendwise machine learning api." 
    }
    
    
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    
    # print(data['transactions'])
    
    buffer = data['transactions']
    day = data['day']
    week_budget = data['budget']
    print(type(buffer))
    print(type(day))
    print(type(week_budget))
    
    
    apicall(buffer,day,week_budget)
    prediction = train_model(day)

    
    return {
        'prediction': prediction, 'day': day
    }

if __name__ == '__main__':
    app.run(port=5001)