from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import pytz  # For handling timezones
from dotenv import load_dotenv
import os

# Load environment variables from .env file

load_dotenv()

app = Flask(__name__)
app.secret_key = 'grievance_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grievance.db'
db = SQLAlchemy(app)

utc_now = datetime.now(pytz.UTC)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')


mail = Mail(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    year = db.Column(db.String(80))
    sem = db.Column(db.String(80))
    branch = db.Column(db.String(80))
    section = db.Column(db.String(80))
    role = db.Column(db.String(10))  # student/admin

class Grievance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="Pending")
    submitted_by = db.Column(db.String(80))
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))


@app.before_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(email='admin@gmail.com').first():
        db.session.add(User(email='admin@gmail.com', password='admin123', role='admin'))
        db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        year = request.form['year']
        sem = request.form['sem']
        branch = request.form['branch']
        section = request.form['section']

        print("Form submitted:", email)  # DEBUGGING

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            print("User already exists.")  # DEBUGGING
            return "Email already exists. Please try another."

        new_user = User(
            firstName=firstname,
            lastName=lastname,
            email=email,
            password=password,
            year=year,
            sem=sem,
            branch=branch,
            section=section,
            role='student'
        )

        db.session.add(new_user)
        db.session.commit()
        print("User registered successfully!")  # DEBUGGING
        return redirect(url_for('login'))

    return render_template('register.html')


def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user'] = user.email
            session['role'] = user.role
            print("SESSION CONTENT:", session)
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        grievance = Grievance(
            title=request.form['title'],
            category=request.form['category'],
            description=request.form['description'],
            submitted_by=session['user']
        )
        db.session.add(grievance)
        db.session.commit()
        return redirect('/status')
    return render_template('submit.html')

@app.route('/dashboard')
def dashboard():
    print("SESSION CONTENT:", session)
    if 'user' not in session: return redirect('/')
    auto_escalate()
    return render_template('dashboard.html', role=session['role'])

@app.route('/status')
def status():
    if 'user' not in session: return redirect('/')
    auto_escalate()
    data = Grievance.query.filter_by(submitted_by=session['user']).all()
    return render_template('status.html', grievances=data)

@app.route('/admin')
def admin():
    if session.get('role') != 'admin': return redirect('/')
    auto_escalate()
    data = Grievance.query.all()
    return render_template('admin_dashboard.html', grievances=data)


@app.route('/update_status', methods=['POST'])
def update_status():
    if session.get('role') != 'admin':
        return redirect('/')
    grievance_id = request.form['grievance_id']
    new_status = request.form['status']
    grievance = Grievance.query.get(grievance_id)
    old_status = grievance.status
    grievance.status = new_status
    db.session.commit()

    # Send email if status has changed
    if old_status != new_status:
        subject = f"Grievance Status Updated: {grievance.title}"
        body = f"Dear {grievance.submitted_by},\n\nYour grievance titled '{grievance.title}' has been updated to: {new_status}."
        send_email(subject, grievance.submitted_by, body)

    return redirect('/admin')


def auto_escalate():
    ist = pytz.timezone('Asia/Kolkata')
    current_ist_time = datetime.now(pytz.utc).astimezone(ist)

    threshold = current_ist_time - timedelta(minutes=1)
    overdue_grievances = Grievance.query.filter(
        Grievance.status == "Pending",
        Grievance.submitted_at < threshold
    ).all()

    for g in overdue_grievances:
        g.status = "Escalated"
        db.session.commit()

        # Send email when grievance is escalated
        subject = f"Grievance Escalated: {g.title}"
        body = f"Dear {g.submitted_by},\n\nYour grievance titled '{g.title}' has been escalated due to lack of progress."
        send_email(subject, g.submitted_by, body)



if __name__ == '__main__':
    app.run(debug=True)
