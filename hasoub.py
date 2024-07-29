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


@app.route('/',methods=["GET","POST"])
def main():
  if request.method == "POST":
    email= request.form ["email"]
    passw = request.form["password"]
    name= request.form["name"]
    phone= request.form[""]
    user = { "em": email,"fullname" :name,"phonenum":phone,"password":passw} 
    
    try:
      session['user'] = auth.create_user_with_email_and_password(email, passw)
      uid =session['user']['localId']

      db.child("Users").child(uid).set(user)
      acc= db.child("Users").child(uid).get().val()
      email = acc['em']
      session['em'] = email
      #added now
      name = acc['fullname']
      session['fullname'] = name
      phone = acc['phonenum']
      session['phonenum'] = phone
      passw = acc['password']
      session['password'] = passw



      return redirect(url_for('demo'))
    except:

      print("error try again")
    session.modified=True
    return redirect(url_for('demo'))
      
  else:
    return render_template("membership.html")



@app.route('/demo',methods=["GET","POST"])
def demo():
	return render_template("demo.html")





if __name__ == '__main__':
 
    app.run( debug=True)
