from flask import Flask, request;

app = Flask(__name__);
from utils import apicall, train_model;

# 
# flask --app app run --port=5001

@app.route('/')
def test():
    apicall(["json2.json", "json1.json"],0,50000)
    prediction = train_model(0)
    return {
        'prediction': prediction, 'day': 0
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