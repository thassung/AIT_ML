import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import joblib
import numpy as np
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

model = joblib.load('./code/model/rf_random_selling_price.model')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Car Selling Price Prediction"),
    
    dcc.Input(id='input1', type='text', placeholder='brand'),
    dcc.Input(id='input2', type='number', placeholder='built year'),
    dcc.Input(id='input3', type='text', placeholder='petrol or diesel'),
    dcc.Input(id='input4', type='text', placeholder='manual or auto transmission'),
    dcc.Input(id='input5', type='number', placeholder='order of ownership'),
    dcc.Input(id='input6', type='number', placeholder='km driven'),
    dcc.Input(id='input7', type='number', placeholder='mileage (km/l)'),
    dcc.Input(id='input8', type='number', placeholder='engine capacity (cc)'),
    dcc.Input(id='input9', type='number', placeholder='max power (bhp)'),
    dcc.Input(id='input10', type='number', placeholder='No. of seats'),
    dcc.Input(id='input11', type='number', placeholder='seller type'),
    
    html.Div(id='prediction-output')
])

@app.callback(
    Output('prediction-output', 'selling_price'),
    Input('input1', 'brand'),
    Input('input2', 'year'),
    Input('input3', 'fuel'),
    Input('input4', 'transmission'),
    Input('input5', 'owner'),
    Input('input6', 'km_driven'),
    Input('input7', 'mileage'),
    Input('input8', 'engine'),
    Input('input9', 'max_power'),
    Input('input10', 'seats'),
    Input('input11', 'seller_type')
)
def update_prediction(input1, input2=2015, input3=0, input4=1, input5=1, 
                      input6=60000, input7=19.3, input8=None, input9=82.85, 
                      input10=5, input11=None):

    
    if input3 is not None:
        if input3.lowercase() == 'petrol':
            input3 = 1
        elif input3.lowercase() == 'diesel':
            input3 = 0
    
    if input4 is not None:
        if input4.lowercase()[:4] == 'auto':
            input4 = 0
        elif input4.lowercase() == 'manual':
            input4 = 1
    
    if input8 is None:
        if input3 == 0:
            input8 = 1497
        elif input3 == 1:
            input8 = 1197
        else:
            input8 = 1248
    
    if input11 is None:
        input11_1 = 1  #indi
        input11_2 = 0  #trust

    tbs = [input6, input7, input8, input9]
    scaler = pickle.load(open('./code/model/scaler.pkl','rb'))
    tbs = scaler.transform(tbs)
    input6, input7, input8, input9 = tbs

    inputs = np.array([[input1, input2, input6, input3, input4,
                        input5, input7, input8, input9, input10,
                        input11_1, input11_2]])

    brand_list = ['Ambassador', 'Ashok', 'Audi', 'BMW', 'Chevrolet', 
                     'Daewoo', 'Datsun', 'Fiat', 'Force', 'Ford', 'Honda', 
                     'Hyundai', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land', 
                     'Lexus', 'MG', 'Mahindra', 'Maruti', 'Mercedes-Benz', 
                     'Mitsubishi', 'Nissan', 'Renault', 'Skoda', 'Tata', 
                     'Toyota', 'Volkswagen', 'Volvo', 'Opel', 'Peugeot']
    b_cols = np.zeroes(len(brand_list))
    for i, col in enumerate(brand_list):
        if input1.capitalize() == col:
            b_cols[i] = 1
    
    inputs = np.concatenate((input, b_cols))
    inputs = inputs[1:]
    inputs = inputs.reshape(1, -1)

    prediction = np.exp(model.predict(inputs)[0])
        
    return f"Predicted Value: {prediction:.2f}"
    

if __name__ == '__main__':
    app.run_server(debug=True)
