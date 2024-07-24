# import json
# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error

# # Load JSON data
# with open('main_data/reference_coordinates_data.json', 'r') as file:
#     data = json.load(file)

# # Prepare data for the model
# X = []
# y_x = []
# y_y = []

# for details in data.values():
#     averages = [details[f'number{i}']['average'] for i in range(1, 6)]
#     X.append(averages)
#     y_x.append(details['x'])
#     y_y.append(details['y'])

# X = np.array(X)
# y_x = np.array(y_x)
# y_y = np.array(y_y)

# # Split data into training and testing sets
# X_train, X_test, y_x_train, y_x_test, y_y_train, y_y_test = train_test_split(
#     X, y_x, y_y, test_size=0.2, random_state=42)

# # Create and train models
# model_x = LinearRegression()
# model_y = LinearRegression()

# model_x.fit(X_train, y_x_train)
# model_y.fit(X_train, y_y_train)

# # Make predictions
# y_x_pred = model_x.predict(X_test)
# y_y_pred = model_y.predict(X_test)

# # Evaluate the models
# print("Mean Squared Error for x:", mean_squared_error(y_x_test, y_x_pred))
# print("Mean Squared Error for y:", mean_squared_error(y_y_test, y_y_pred))

# # Example input for prediction
# example_averages = np.array([[ -75.42, -80.34, -75.29, -63.94, -49.72]])  # Replace with actual average values
# predicted_x = model_x.predict(example_averages)
# predicted_y = model_y.predict(example_averages)

# print("Predicted x:", predicted_x[0])
# print("Predicted y:", predicted_y[0])


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

# Ensure predictions are non-negative
y_x_pred = np.where(y_x_pred < 0, 0, y_x_pred)
y_y_pred = np.where(y_y_pred < 0, 0, y_y_pred)

# Evaluate the models
print("Mean Squared Error for x:", mean_squared_error(y_x_test, y_x_pred))
print("Mean Squared Error for y:", mean_squared_error(y_y_test, y_y_pred))

# Example input for prediction
example_averages = np.array([[-76.77, -83.28, -70.83, -64.52, -69.06]])  # Replace with actual average values

# Retry prediction until both x and y values are non-negative
while True:
    predicted_x = model_x.predict(example_averages)
    predicted_y = model_y.predict(example_averages)
    
    # Break the loop if both predicted_x and predicted_y are non-negative
    if predicted_x[0] >= 0 and predicted_y[0] >= 0:
        break

# Ensure y prediction is non-negative (though it should already be due to the loop condition)
predicted_y = np.where(predicted_y < 0, 0, predicted_y)

print("Predicted x:", predicted_x[0])
print("Predicted y:", predicted_y[0])
