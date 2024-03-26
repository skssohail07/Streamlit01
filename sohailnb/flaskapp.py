import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

def preprocess_inp(data):
    data = data.copy()

    data['Vegetable'] = data['Vegetable'].replace({
        'cabage': 1,
        'radish': 2,
        'potato': 3,
        'tomato ': 4,
        'peas': 5,
        'pumkin': 6,
        'cucumber': 7,
        'pointed grourd ': 8,
        'Raddish': 9,
        'Bitter gourd': 10,
        'onion': 11,
        'ginger': 12,
        'garlic': 13,
        'califlower': 14,
        'brinjal': 15,
        'okra': 16,
        'chilly': 17,
    })

    data['Deasaster Happen in last 3month'] = data['Deasaster Happen in last 3month'].replace({'no' : 0,'yes' : 1})

    data['Month'] = data['Month'].replace({
        'jan' : 1,
        'feb':2 ,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6 ,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec' : 12,
        ' ' : np.NaN
    })

    data['Month'] = data['Month'].fillna(data['Month'].mode()[0])

    data['Vegetable condition'] = data['Vegetable condition'].replace({'fresh' : 0,'avarage':1,'scrap':2})

    data['Season'] = data['Season'].replace({'winter' : 0,'summer':1,'spring':2,'autumn': 3,'monsoon':4})
    
    return data

model = pickle.load(open("C:\\Users\\Mastermind\\Downloads\\sohailnb\\sohailnb\\model2\\model.sav", "rb"))

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        Vegetable = int(request.form["Vegetable"])
        Season = int(request.form["Season"])
        Temperature = float(request.form["Temperature"])
        Month = int(request.form["Month"])
        Vegetable_Condition = int(request.form["Vegetable_Condition"])
        Disaster_in_last_3months = int(request.form["Disaster_in_last_3months"])

        # Preprocess input
        input_data = preprocess_inp(np.array([[Vegetable, Season, Temperature, Month, Vegetable_Condition, Disaster_in_last_3months]]))

        # Predict using the model
        pred = model.predict(input_data)
        predicted_price = pred[0][0]

        return render_template("index.html", predicted_price=predicted_price)
    
    return render_template("index.html", predicted_price=None)

if __name__ == "__main__":
    app.run(debug=True)
