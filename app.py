from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model and preprocessing objects
model = joblib.load('model.pkl')
imputer_X = joblib.load('imputer_X.pkl')
encoded_column_names = joblib.load('encoded_column_names.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    age = int(request.form['age'])
    weight_on_admission = float(request.form['weight_on_admission'])
    total_days = int(request.form['total_days'])
    days_of_fasting = int(request.form['days_of_fasting'])
    diet = request.form['diet']
    
    # Create a dataframe from form data
    input_data = pd.DataFrame({
        'Age': [age],
        'Weight_on_admission': [weight_on_admission],
        'Total__days': [total_days],
        'Days_of_fasting': [days_of_fasting],
        'Diet': [diet]
    })

    # One-hot encode the 'Diet' column
    diet_encoded = pd.get_dummies(input_data['Diet'], prefix='Diet')
    input_data = input_data.drop('Diet', axis=1)
    input_data = pd.concat([input_data, diet_encoded], axis=1)

    # Align input data with the model's expected columns
    input_data = input_data.reindex(columns=encoded_column_names, fill_value=0)
    
    # Impute missing values
    input_data = imputer_X.transform(input_data)

    # Make a prediction
    prediction = model.predict(input_data)
    
    return jsonify({'predicted_weight_on_discharge': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
