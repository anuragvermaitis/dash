from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import io
import base64
import plotly.express as px
import plotly.io as pio

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# --- Cleaning Data ---
def clean_data(df):
    """
    Cleans the dataframe by:
    1. Stripping spaces from string columns.
    2. Dropping duplicate rows.
    3. Filling missing values in numeric columns with the median.
    4. Filling missing values in categorical columns with the mode.
    """
    df_cleaned = df.copy()
    
    # Clean string columns by stripping spaces
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].str.strip()

    # Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates()

    # Fill missing numeric columns with median
    for col in df_cleaned.select_dtypes(include=['float64', 'int64']).columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())

    # Fill missing categorical columns with mode
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        if df_cleaned[col].mode().size > 0:
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])

    return df_cleaned

# --- Routes ---
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the file is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        # If no file is selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file)

        # Clean the data
        df_cleaned = clean_data(df)

        # Convert cleaned data into JSON format
        cleaned_data_json = df_cleaned.to_dict(orient='records')

        # Generate a plot (e.g., a histogram of the first numeric column)
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return jsonify({"error": "No numeric columns to plot."}), 400
        
        # Generate a histogram using Plotly
        fig = px.histogram(df_cleaned, x=numeric_cols[0], title=f"Histogram of {numeric_cols[0]}")
        
        # Convert the plot to an image (PNG format)
        img_bytes = pio.to_image(fig, format='png')
        
        # Convert the image to a base64 encoded string
        img_base64 = base64.b64encode(img_bytes).decode()

        # Send back the cleaned data and the plot as base64 image
        return jsonify({
            "cleaned_data": cleaned_data_json,
            "plot_base64": img_base64
        })

    except Exception as e:
        # Print the error for debugging purposes
        print(f"Error: {e}")
        
        # Return error message in response
        return jsonify({"error": str(e)}), 500

# --- Main ---
if __name__ == '__main__':
    # Start the Flask app in debug mode
    app.run(debug=True)
