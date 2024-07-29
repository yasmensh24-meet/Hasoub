from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session 
import pyrebase




Config = {
  "apiKey": "AIzaSyDySMuW71nJCobS-SLkEU08AeHHFtD0OOA",
  "authDomain": "hasoub-4c475.firebaseapp.com",
 "databaseURL": "https://hasoub-4c475-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "hasoub-4c475",
  "storageBucket": "hasoub-4c475.appspot.com",
  "messagingSenderId": "187761184038",
  "appId": "1:187761184038:web:cbc58b72d9b2d5757745e7",
  "databaseURL":"https://hasoub-4c475-default-rtdb.europe-west1.firebasedatabase.app/"
};



firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'






