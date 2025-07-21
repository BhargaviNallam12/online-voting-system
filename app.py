from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = 'secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config (use your email)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chandrabhargavi537@gmail.com'
app.config['MAIL_PASSWORD'] = 'khbuccsdbibeftek'



db = SQLAlchemy(app)
mail = Mail(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    otp = db.Column(db.String(6))
    voted = db.Column(db.Boolean, default=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    votes = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    otp = str(random.randint(100000, 999999))
    session['email'] = email

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, otp=otp)
        db.session.add(user)
    else:
        user.otp = otp
    db.session.commit()

    msg = Message('Your OTP', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your OTP is {otp}'
    mail.send(msg)

    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form['otp']
    email = session.get('email')
    user = User.query.filter_by(email=email).first()

    if user and user.otp == user_otp:
        session['voted'] = user.voted
        return redirect('/vote')
    return "Invalid OTP!"

@app.route('/vote')
def vote():
    if session.get('voted', False):
        return "You have already voted!"
    candidates = Candidate.query.all()
    return render_template('vote.html', candidates=candidates)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    candidate_id = request.form['candidate']
    email = session.get('email')
    user = User.query.filter_by(email=email).first()

    if not user.voted:
        candidate = Candidate.query.get(candidate_id)
        candidate.votes += 1
        user.voted = True
        db.session.commit()
        session['voted'] = True
        return redirect('/result')
    return "You have already voted!"

@app.route('/result')
def result():
    candidates = Candidate.query.all()
    return render_template('result.html', candidates=candidates)
db = db
Candidate = Candidate
app = app


if __name__ == '__main__':
    app.run(debug=True)
