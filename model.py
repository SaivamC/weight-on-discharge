import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer

# Load the data from the Excel file
data = pd.read_excel(r'C:\Users\kvsai\Desktop\obese.xlsx')

# Clean column names by stripping leading/trailing spaces and replacing spaces with underscores
data.columns = data.columns.str.strip().str.replace(' ', '_')

# Print the cleaned column names to confirm
print("Cleaned column names in the dataset:")
print(data.columns)

# Add a column for reduced weight (weight on admission - weight on discharge)
data['Reduced_Weight'] = data['Weight_on_admission'] - data['Weight_on_discharge']

# Convert dates to datetime format
data['Date_of_admission'] = pd.to_datetime(data['Date_of_admission'])
data['Date_of_discharge'] = pd.to_datetime(data['Date_of_discharge'])

# Calculate total days of treatment
data['Total_days'] = (data['Date_of_discharge'] - data['Date_of_admission']).dt.days

# Ensure correct column names for model features
X = data.drop(['Weight_on_discharge', 'Reduced_Weight', 'Date_of_admission', 'Date_of_discharge', 'S.No', 'ID'], axis=1)
y = data['Weight_on_discharge']

# Handle categorical data using one-hot encoding
diet_encoded = pd.get_dummies(X['Diet'], prefix='Diet')
X = X.drop('Diet', axis=1)
X = pd.concat([X, diet_encoded], axis=1)

# Store the column names after encoding and transformations
encoded_column_names = X.columns

# Impute missing values in X with the mean of each column
imputer_X = SimpleImputer(strategy='mean')
X = imputer_X.fit_transform(X)

# Impute missing values in y with the mean
imputer_y = SimpleImputer(strategy='mean')
y = imputer_y.fit_transform(y.values.reshape(-1, 1)).ravel()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Gradient Boosting Regressor model
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_model.fit(X_train, y_train)

# Save the model and preprocessing objects
joblib.dump(gb_model, 'model.pkl')
joblib.dump(imputer_X, 'imputer_X.pkl')
joblib.dump(encoded_column_names, 'encoded_column_names.pkl')

print("Model and preprocessing objects saved successfully.")
