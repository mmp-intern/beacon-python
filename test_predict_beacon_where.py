import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load JSON data
with open('main_data/reference_coordinates_data.json', 'r') as file:
    data = json.load(file)

# Prepare data for the model
X = []
y_x = []
y_y = []

for details in data.values():
    averages = [details[f'number{i}']['average'] for i in range(1, 6)]
    X.append(averages)
    y_x.append(details['x'])
    y_y.append(details['y'])

X = np.array(X)
y_x = np.array(y_x)
y_y = np.array(y_y)

# Split data into training and testing sets
X_train, X_test, y_x_train, y_x_test, y_y_train, y_y_test = train_test_split(
    X, y_x, y_y, test_size=0.2, random_state=42)

# Create and train models
model_x = LinearRegression()
model_y = LinearRegression()

model_x.fit(X_train, y_x_train)
model_y.fit(X_train, y_y_train)

# Make predictions
y_x_pred = model_x.predict(X_test)
y_y_pred = model_y.predict(X_test)

# Evaluate the models
print("Mean Squared Error for x:", mean_squared_error(y_x_test, y_x_pred))
print("Mean Squared Error for y:", mean_squared_error(y_y_test, y_y_pred))

# Example input for prediction
example_averages = np.array([[ -85.24, -86.57, -70.92, -65.13, -60.23]])  # Replace with actual average values
predicted_x = model_x.predict(example_averages)
predicted_y = model_y.predict(example_averages)

print("Predicted x:", predicted_x[0])
print("Predicted y:", predicted_y[0])
