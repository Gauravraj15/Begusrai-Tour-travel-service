from dotenv import load_dotenv
import os
from datetime import timedelta
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from flask_mail import Mail, Message
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

# --- Secrets / Config ---
# Use environment variables in production (Render). Fallback values provided for local/testing.
app.secret_key = os.getenv("SECRET_KEY", "change-me")
app.permanent_session_lifetime = timedelta(days=180)

ADMIN_EMAIL = "samarkings12@gmail.com"

# --- MongoDB Setup (Atlas) ---
# Prefer environment variable on Render:

#   MONGODB_URI = mongodb+srv://<user>:<pass>@cluster12.gr4cutd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster12
MONGO_URI = "mongodb+srv://himroy14:Ray8sKq7Zp2@cluster12.gr4cutd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

#client = MongoClient(MONGO_URI)

# Two databases:
db_users = client['user_details']
users = db_users['user_info']
queries = db_users['queries']
bookings = client['travel_db']['bookings']

# --- Mail Configuration (use env vars on Render) ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'gau879731raj@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'bnwl wmja ghul shwh')

mail = Mail(app)

# --- Routes ---

@app.route("/healthz")
def healthz():
    # Simple health check; Atlas ping optional
    try:
        client.admin.command("ping")
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "detail": str(e)}, 500

@app.route("/")
def index():
    user_name = None
    welcome_msg = session.pop('welcome_status', None)
    if 'user' in session:
        user_data = users.find_one({'email': session['user']})
        if user_data:
            user_name = user_data.get('name')
    return render_template('index.html', user=user_name, welcome_msg=welcome_msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', login_error=None, email_value="")

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', login_error="Missing email or password", email_value=email or "")

    user = users.find_one({'email': email})

    if not user:
        return render_template('login.html', login_error="Invalid Email", email_value="")

    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return render_template('login.html', login_error="Invalid Password", email_value=email)

    session.permanent = True
    session['user'] = user['email']
    if user.get('is_first_login', True):
        session['welcome_status'] = f"Welcome, {user.get('name','User')}!"
        users.update_one({'email': email}, {'$set': {'is_first_login': False}})
    else:
        session['welcome_status'] = f"Welcome back, {user.get('name','User')}!"
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/about')
def About():
    return render_template('About.html', user=session.get('user'))

@app.route('/book')
def book():
    if 'user' not in session:
        return "<h3 style='color:red;text-align:center;'>You need to login to access the booking section.</h3><a href='/' style='display:block;text-align:center;'>Back to Home</a>"
    return render_template('book.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form.get('name'),
        'mobile_no': request.form.get('mobile_no'),
        'email_id': request.form.get('email_id'),
        'address': request.form.get('address'),
        'from_location': request.form.get('custom_from') if request.form.get('from_location') == "Custom" else request.form.get('from_location'),
        'to_location': request.form.get('custom_to') if request.form.get('to_location') == "Custom" else request.form.get('to_location'),
        'travel_date': request.form.get('travel_date')
    }

    bookings.insert_one(data)

    try:
        msg = Message(
            subject="Booking Confirmation - Begusarai Tour & Travel",
            sender=app.config['MAIL_USERNAME'],
            recipients=[data['email_id']],
        )
        msg.body = f"""Dear {data['name']},

Your booking has been confirmed with the following details:

Name: {data['name']}
Mobile: {data['mobile_no']}
Email: {data['email_id']}
From: {data['from_location']}
To: {data['to_location']}
Travel Date: {data['travel_date']}

Thank you for booking with Begusarai Tour & Travel Service.

Regards,
Begusarai Tour & Travel Team
"""
        mail.send(msg)
    except Exception as e:
        print("Email sending failed:", str(e))

    return "<h3>Booking submitted successfully! A confirmation email has been sent.</h3><a href='/'>Back to Home</a>"

@app.route('/query')
def query():
    if 'user' not in session:
        return "<h3 style='color:red;text-align:center;'>You need to login to access the query section.</h3><a href='/' style='display:block;text-align:center;'>Back to Home</a>"
    return render_template('Query.html')

@app.route('/submit_problem', methods=['POST'])
def submit_problem():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = users.find_one({'email': session['user']})
    if user:
        queries.insert_one({
            'name': user.get('name', ''),
            'email': user.get('email', ''),
            'problem': request.form.get('problemDescription', '')
        })
        return "<h3>Thank you! Your query has been submitted.</h3><a href='/'>Back to Home</a>"
    return redirect(url_for('login'))

@app.route('/confirm_logout')
def confirm_logout():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_data = users.find_one({'email': session['user']})
    name = user_data['name'] if user_data else "User"
    return render_template('confirm_logout.html', username=name)

@app.route('/signup_user', methods=['POST'])
def signup_user():
    name = request.form.get('name')
    email = request.form.get('email_signup')
    password_raw = request.form.get('password_signup')

    if not (name and email and password_raw):
        return "<h3>All fields are required.</h3><a href='/login'>Back</a>"

    password = bcrypt.hashpw(password_raw.encode('utf-8'), bcrypt.gensalt())

    if users.find_one({'email': email}):
        return "<h3>User already exists.</h3><a href='/login'>Back</a>"

    users.insert_one({
        'name': name,
        'email': email,
        'password': password,
        'is_first_login': True
    })

    return "<h3>Signup successful!</h3><a href='/login'>Login</a>"

@app.route('/verify_email', methods=['POST'])
def verify_email():
    email_data = request.get_json()
    email = email_data.get('email') if email_data else None
    return jsonify({'exists': bool(users.find_one({'email': email}))})

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('verified_email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not email or not new_password or not confirm_password:
        return "<h3>All fields are required.</h3><a href='/login'>Back</a>"

    if new_password != confirm_password:
        return "<h3>Passwords do not match.</h3><a href='/login'>Back</a>"

    if users.find_one({'email': email}):
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        users.update_one({'email': email}, {'$set': {'password': hashed_pw}})
        return "<h3>Password reset successful!</h3><a href='/login'>Login</a>"

    return "<h3>Email not found.</h3><a href='/login'>Back</a>"

@app.route('/admin')
def admin():
    if session.get('user') != ADMIN_EMAIL:
        return "<h3>Access Denied</h3><a href='/login'>Login as Admin</a>"
    all_queries = queries.find()
    return render_template('admin.html', queries=all_queries)

@app.route('/admin/bookings')
def admin_bookings():
    if session.get('user') != ADMIN_EMAIL:
        return "<h3>Access Denied</h3><a href='/login'>Login as Admin</a>"
    all_bookings = bookings.find()
    return render_template('admin_bookings.html', bookings=all_bookings)

@app.route('/admin/download_queries')
def download_queries():
    if session.get('user') != ADMIN_EMAIL:
        return "<h3>Access Denied</h3><a href='/login'>Login as Admin</a>"
    all_queries = queries.find()
    csv_data = "Name,Email,Problem\n"
    for q in all_queries:
        csv_data += f"{q.get('name','')},{q.get('email','')},{q.get('problem','').replace(',', ' ')}\n"
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=queries.csv"})

@app.route('/admin/download_bookings')
def download_bookings():
    if session.get('user') != ADMIN_EMAIL:
        return "<h3>Access Denied</h3><a href='/login'>Login as Admin</a>"
    all_bookings = bookings.find()
    csv_data = "Name,Mobile,Email,Address,From,To,Travel Date\n"
    for b in all_bookings:
        csv_data += f"{b.get('name','')},{b.get('mobile_no','')},{b.get('email_id','')},{b.get('address','')},{b.get('from_location','')},{b.get('to_location','')},{b.get('travel_date','')}\n"
    return Response(csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=bookings.csv"})

if __name__ == '__main__':
    # Bind to 0.0.0.0 for Render; use PORT env if present
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
