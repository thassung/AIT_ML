# Dash Plotly App

This is a Car Selling Price Prediction Web App that was trained with a dataset provided in the repositories (/code/data/Cars - Cars.csv). Users can input 5 values including:
- Car brand: A dropdown selection of car brand
- Built year: Built year of the car
- Transmission: A gear transmission type of cars
- Engine capacity: The size of the engine (unit is CC)
- Max power: Maximum force produced by car's engine (unit is bhp)

To run this folder, `Docker` is needed and then run the following command line in terminal

```sh
docker compose up --build
```

Access the app with http://localhost:9999