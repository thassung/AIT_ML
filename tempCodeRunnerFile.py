import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import joblib
import numpy as np

model = joblib.load('./code/model/rf_random_selling_price.model')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Car Selling Price Prediction"),
    
    dcc.Input(id='input1', type='number', placeholder='Enter value 1'),
    dcc.Input(id='input2', type='number', placeholder='Enter value 2'),
    dcc.Input(id='input3', type='number', placeholder='Enter value 1'),
    dcc.Input(id='input4', type='number', placeholder='Enter value 1'),
    dcc.Input(id='input5', type='number', placeholder='Enter value 1'),
    
    html.Div(id='prediction-output')
])

@app.callback(
    Output('prediction-output', 'children'),
    Input('input1', 'value'),
    Input('input2', 'value'),
    # Add more inputs as needed
)
def update_prediction(input1, input2):
    if input1 is not None and input2 is not None:
        # Assuming your model expects a 2D array-like input
        inputs = np.array([[input1, input2]])
        
        # Make prediction using the model
        prediction = model.predict(inputs)[0]
        
        return f"Predicted Value: {prediction:.2f}"
    else:
        return "Waiting for inputs..."

if __name__ == '__main__':
    app.run_server(debug=True)