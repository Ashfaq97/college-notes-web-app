import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hello321'


############## DATABASE CONNECTION ################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

###################### MODELS ###########################

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

login_manager = LoginManager()

class Notebook(db.Model):

    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    subjectName = db.Column(db.Text)
    semester = db.Column(db.Integer)

    def __init__(self, id, subjectName, semester):
        self.id = id
        self.subjectName = subjectName
        self.semester = semester

    def __repr__(self):
        return f"{self.subjectName} of {self.semester}"



@login_manager.user_loader
def load_user(User.id):
    return User.query.get(User.id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(64), unique=True, index=True)
    userEmail = db.Column(db.String(64), unique=True, index=True)
    hashed_password = db.Column(db.String(128))

    def __init__(self, password, userName, userEmail):
        self.id = id
        self.userName = userName
        self.userEmail = userEmail
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"User Name is {self.userName} and Email is {self.userEmail}."

####################### ROUTES ##########################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/login/')
def login():
    return render_template('login.html')



if __init__ == '__main__':
    app.run(debug=True)
