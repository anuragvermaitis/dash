from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import bcrypt
import datetime
import random
import smtplib
from email.message import EmailMessage
import pandas as pd
import numpy as np
import io
import base64
import plotly.express as px
import plotly.io as pio

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- MongoDB Setup ---
db_password = "Ubq4o46wcWqjy6Om"
client = MongoClient(f"mongodb+srv://eranurag029:{db_password}@cluster0.lro0gnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['UserDB']
users_collection = db['users']

# --- JWT Secret ---
JWT_SECRET = 'your_jwt_secret_here'  # Change this in production
JWT_ALGORITHM = 'HS256'

# --- Gmail SMTP Settings ---
EMAIL_ADDRESS = "your_gmail@gmail.com"   # Replace with your Gmail
EMAIL_PASSWORD = "your_gmail_app_password"  # Use Gmail App Passwords

# --- Helper Functions ---
def send_otp_email(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f'Your OTP for verification is: {otp}')
    msg['Subject'] = 'OTP Verification'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# --- Auth Routes ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    password = data['password']

    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    otp = str(random.randint(100000, 999999))

    users_collection.insert_one({
        'email': email,
        'password': hashed_password,
        'otp': otp,
        'is_verified': False
    })

    send_otp_email(email, otp)
    return jsonify({"message": "OTP sent to your email. Please verify."}), 200

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data['email']
    otp = data['otp']

    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user['otp'] == otp:
        users_collection.update_one({'email': email}, {'$set': {'is_verified': True}})
        token = generate_jwt(email)
        return jsonify({"message": "Account verified!", "token": token}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data['email']
    password = data['password']

    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user['is_verified']:
        return jsonify({"error": "User not verified"}), 400

    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = generate_jwt(email)
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 400

# --- Data Cleaning ---
def clean_data(df):
    df_cleaned = df.copy()
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].str.strip()
    df_cleaned = df_cleaned.drop_duplicates()
    for col in df_cleaned.select_dtypes(include=['float64', 'int64']).columns:
        df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        if df_cleaned[col].mode().size > 0:
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    return df_cleaned

# --- Upload & Filter API with Graph ---
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        df = pd.read_csv(file)
        df_cleaned = clean_data(df)

        # --- Apply filters ---
        for key, value in request.args.items():
            if key in df_cleaned.columns:
                df_cleaned = df_cleaned[df_cleaned[key].astype(str).str.lower() == value.lower()]

        # --- Dynamic filter options ---
        filter_options = {}
        for col in df.columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) <= 100:
                filter_options[col] = sorted(map(str, unique_vals))

        # --- Cleaned Data JSON ---
        cleaned_data_json = df_cleaned.to_dict(orient='records')

        # --- Plot graph from first numeric column ---
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        plot_base64 = None
        if len(numeric_cols) > 0:
            fig = px.histogram(df_cleaned, x=numeric_cols[0], title=f"Histogram of {numeric_cols[0]}")
            img_bytes = pio.to_image(fig, format='png')
            plot_base64 = base64.b64encode(img_bytes).decode()

        return jsonify({
            "cleaned_data": cleaned_data_json,
            "plot_base64": plot_base64,
            "filter_options": filter_options
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- Resend OTP ---
@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    otp = str(random.randint(100000, 999999))
    users_collection.update_one(
        {'email': email},
        {'$set': {'otp': otp, 'is_verified': False}},
        upsert=True
    )
    send_otp_email(email, otp)
    return jsonify({"message": f"OTP '{otp}' sent successfully to {email}"}), 200

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
