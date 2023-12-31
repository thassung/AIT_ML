import dash
import joblib
from dash import Dash, html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle

app = dash.Dash(__name__)
dash.register_page('demoapp', path='/app2')

# Create elements for app layout
x_1 = html.Div(
    [
        dbc.Label("Car brand: ", html_for="example-email"),
        dcc.Dropdown(id='x_1',
            options=[
                {'label': 'Ambassador', 'value': 1},
                {'label': 'Ashok', 'value': 2},
                {'label': 'Audi', 'value': 3},
                {'label': 'BMW', 'value': 4},
                {'label': 'Chevrolet', 'value': 5},
                {'label': 'Daewoo', 'value': 6},
                {'label': 'Datsun', 'value': 7},
                {'label': 'Fiat', 'value': 8},
                {'label': 'Force', 'value': 9},
                {'label': 'Ford', 'value': 10},
                {'label': 'Honda', 'value': 11},
                {'label': 'Hyundai', 'value': 12},
                {'label': 'Isuzu', 'value': 13},
                {'label': 'Jaguar', 'value': 14},
                {'label': 'Jeep', 'value': 15},
                {'label': 'Kia', 'value': 16},
                {'label': 'Land', 'value': 17},
                {'label': 'Lexus', 'value': 18},
                {'label': 'MG', 'value': 19},
                {'label': 'Mahindra', 'value': 20},
                {'label': 'Maruti', 'value': 21},
                {'label': 'Mercedes-Benz', 'value': 22},
                {'label': 'Mitsubishi', 'value': 23},
                {'label': 'Nissan', 'value': 24},
                {'label': 'Opel', 'value': 25},
                {'label': 'Peugeot', 'value': 26},
                {'label': 'Renault', 'value': 27},
                {'label': 'Skoda', 'value': 28},
                {'label': 'Tata', 'value': 29},
                {'label': 'Toyota', 'value': 30},
                {'label': 'Volkswagen', 'value': 31},
                {'label': 'Volvo', 'value': 32},
                {'label': 'Other/Unknown', 'value': 0}
            ],
            value='0', placeholder=' select car brand'),
        dbc.FormText(
            " \n",
            color="secondary",
        ),
    ],
    style={"width": "15%"},
    className="mb-3",
)

x_2 = html.Div(
    [
        dbc.Label("Built year: ", html_for="example-email"),
        dbc.Input(id="x_2", type="number", placeholder=" ex. 1999, 2015"),
        dbc.FormText(
            "",
            color="secondary",
        ),
    ],
    className="mb-3",
)

x_3 = html.Div(
    [
        dbc.Label("Transmission: ", html_for="example-email"),
        dcc.Dropdown(id='x_3',
            options=[
                {'label': 'Automatic', 'value': 0},
                {'label': 'Manual', 'value': 1}
            ],
            value='0', placeholder=' select transmission type'),
        dbc.FormText(
            " \n",
            color="secondary",
        ),
    ],
    style={"width": "15%"},
    className="mb-3",
)

x_4 = html.Div(
    [
        dbc.Label("Engine capacity: ", html_for="example-email"),
        dbc.Input(id="x_4", type="number", placeholder=" unit is CC"),
        dbc.FormText(
            " CC",
            color="secondary",
        ),
    ],
    className="mb-3",
)

x_5 = html.Div(
    [
        dbc.Label("Max power: ", html_for="example-email"),
        dbc.Input(id="x_5", type="number", placeholder=" unit is bhp"),
        dbc.FormText(
            " bhp",
            color="secondary",
        ),
    ],
    className="mb-3",
)

submit_button = html.Div([
            dbc.Button(id="submit_button", children="Submit", color="primary", className="me-1"),
            dbc.Label("  "),
            html.Output(id="selling_price", 
                        children='')
            ], style={'marginTop':'10px'})


form =  dbc.Form([
            x_1, x_2, x_3, x_4, x_5,
            submit_button,

        ],
        className="mb-3")


# Explain Text
text = html.Div([
    html.H1("Car Predicing (predict pricing)"),
    html.P("The model is a RandomForest model."),
])

# Dataset Example
from dash import Dash, dash_table
import pandas as pd
df = pd.read_csv('./code/data/Cars - Cars.csv')

table = dbc.Table.from_dataframe(df.head(50), 
                        striped=True, 
                        bordered=True, 
                        hover=True,
                        responsive=True,
                        size='sm'
                            )

app.layout =  dbc.Container([
        text,
        form,
        html.H1("The Dataset trained in the model (first 50 sentries)"),
        table
    ], fluid=True)

@app.callback(
    Output(component_id="selling_price", component_property="children"),
    Input(component_id='submit_button', component_property='n_clicks'),
    State(component_id="x_1", component_property="value"),
    State(component_id="x_2", component_property="value"),
    State(component_id="x_3", component_property="value"),
    State(component_id="x_4", component_property="value"),
    State(component_id="x_5", component_property="value"),
    prevent_initial_call=True
)

def calculate_selling_price(x_1, x_2, x_3, x_4, x_5, submit):
    
    model = joblib.load('./code/model/rf_random_selling_price.model')
    scaler = pickle.load(open('./code/model/scaler.pkl','rb'))

    ## scale engine and max_power
    tbs = pd.DataFrame({'engine':[x_4], 'max_power':[x_5]})
    tbs = scaler.transform(tbs)
    x_4, x_5 = tbs[0][0], tbs[0][1]

    ## create dummies value for brand
    brand_list = ['Ambassador','Ashok','Audi','BMW','Chevrolet','Daewoo','Datsun','Fiat',
                    'Force','Ford','Honda','Hyundai','Isuzu','Jaguar','Jeep',
                    'Kia','Land','Lexus','MG','Mahindra','Maruti','Mercedes-Benz',
                    'Mitsubishi','Nissan','Opel','Peugeot','Renault','Skoda','Tata',
                    'Toyota','Volkswagen','Volvo']

    col_order = ['year','transmission','engine','max_power','b_Ambassador','b_Ashok','b_Audi',
                'b_BMW','b_Chevrolet','b_Daewoo','b_Datsun','b_Fiat','b_Force','b_Ford',
                'b_Honda','b_Hyundai','b_Isuzu','b_Jaguar','b_Jeep','b_Kia','b_Land',
                'b_Lexus','b_MG','b_Mahindra','b_Maruti','b_Mercedes-Benz','b_Mitsubishi',
                'b_Nissan','b_Opel','b_Peugeot','b_Renault','b_Skoda','b_Tata',
                'b_Toyota','b_Volkswagen','b_Volvo']

    b_cols = np.zeros(len(brand_list))
    print(len(b_cols))
    # if x_1 is not None:
    #     for i, brand in enumerate(brand_list):
    #         if x_1 == brand:
    #             b_cols[i] = 1
    #             break
    if x_1 > 0:
        b_cols[x_1-1] = 1

    X = np.array([x_2, x_3, x_4, x_5])
    X = np.concatenate([X, b_cols])
    len(col_order)
    X = pd.DataFrame([X], columns =col_order)
    pred = np.exp(model.predict(X))[0]
    return f"Predicted car price is: {pred:.2f}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)