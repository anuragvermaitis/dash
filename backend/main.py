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

# --- Gmail SMTP Settings (FREE) ---
EMAIL_ADDRESS = "your_gmail@gmail.com"   # Replace with your Gmail
EMAIL_PASSWORD = "your_gmail_app_password"  # Use Gmail App Passwords, not real password!

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

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Save user with is_verified = False
    users_collection.insert_one({
        'email': email,
        'password': hashed_password,
        'otp': otp,
        'is_verified': False
    })

    # Send OTP email
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

# --- Cleaning Data ---
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

# --- Upload Route ---
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
        cleaned_data_json = df_cleaned.to_dict(orient='records')

        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return jsonify({"error": "No numeric columns to plot."}), 400
        
        fig = px.histogram(df_cleaned, x=numeric_cols[0], title=f"Histogram of {numeric_cols[0]}")
        img_bytes = pio.to_image(fig, format='png')
        img_base64 = base64.b64encode(img_bytes).decode()

        return jsonify({
            "cleaned_data": cleaned_data_json,
            "plot_base64": img_base64
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Generate OTP
    otp = str(random.randint(100000, 999999))

    # Save OTP to DB (or however you manage it)
    users_collection.update_one(
        {'email': email},
        {'$set': {'otp': otp, 'is_verified': False}},
        upsert=True
    )

    # Send OTP via email
    send_otp_email(email, otp)

    return jsonify({"message": f"OTP '{otp}' sent successfully to {email}"}), 200


# --- Main ---
if __name__ == '__main__':
    app.run(debug=True)
