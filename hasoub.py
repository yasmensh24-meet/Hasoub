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
    phone= request.form["phone"]
    user = { "em": email,"fullname" :name,"phonenum":phone,"password":passw} 
    
    #try:
    session['user'] = auth.create_user_with_email_and_password(email, passw)
    uid =session['user']['localId']

    db.child("Users").child(uid).set(user)
    acc = db.child("Users").child(uid).get().val()

    print(acc)

    email = acc['em']
    session['em'] = email
    name = acc['fullname']
    session['fullname'] = name
    phone = acc['phonenum']
    session['phonenum'] = phone
    passw = acc['password']
    session['password'] = passw



    return redirect(url_for('demo'))
    #except:
    #  print("error try again")
    #  session.modified=True
    #  return redirect('/error')
      
  else:
    return render_template("membership.html")

@app.route('/signin', methods=["GET","POST"])
def signin():
  if request.method == "POST":
    email= request.form ["email"]
    passw = request.form["password"]

    try:
      session['user'] = auth.sign_in_with_email_and_password(email, passw)
      if email == "guys@gmail.com":
        return redirect(url_for("admin"))

      #if email == "":
       # return redirect(url_for("admin"))

      return redirect(url_for("demo"))
    except:

      print("error try again")
      session.modified=True
      return redirect(url_for('error'))
      
  else:
    return render_template("signin.html")

@app.route('/admin',methods=["GET","POST"])
def admin():

  uid = session['user']['localId']
  users = db.child("Users").get().val()
  feedback = db.child("feedback").get().val()



  return render_template("admin.html", users = users, feedback = feedback )



@app.route('/demo',methods=["GET","POST"])
def demo():
	return render_template("demo.html")

@app.route('/signout')
def signout():
    # session.pop('user')
    session['user']=None
    auth.current_user = None
    print("signed out user")
    return redirect(url_for('main'))

@app.route('/error',methods=["GET","POST"])
def error():

	return render_template("error.html")

@app.route('/history',methods=["GET","POST"])
def history():
	if 'user' in session:
		uid = session['user']['localId']
		history = db.child('booked').child(uid).get().val()
		if history:
			booking_history = [entry for entry in history.values()]
		else:
			booking_history = []
		return render_template("history.html", history=booking_history)
	else:
		return redirect(url_for('signin'))


	return render_template("history.html") 


@app.route('/custome',methods=["GET","POST"])
def custome():
  if request.method == "GET":
    return render_template("custome.html")
  else:
    return render_template("thankcustome.html")



@app.route('/priority',methods=["GET","POST"])
def priority():
  if request.method == "GET":   
    return render_template("priority.html")

  else:
    date = request.form["date"]
    try:
      session['dates']=[]
      session['dates'].append(date)
      session.modified = True

      uid =session['user']['localId']
      #print('uid')
      #ref = db.child("Users").child(uid).get().val()
      
      saved = {"date":date}
      db.child('booked').child(uid).push(saved)
      session['date_apt'] = date

      return redirect(url_for("thank"))
    except:
      print("error try again")
      return render_template('error.html')

  

@app.route('/feedback',methods=["GET","POST"])
def feedback():
  if request.method=="POST":
    
    feed=request.form['feedback']
    uid =session['user']['localId']
      
    ref = db.child('Users').child(uid).get().val()
##add a new key/value to the dict
    ref['feedback']=feed
    db.child('Users').child(uid).set(ref)
   

    return render_template("thankfeed.html")
  else:
    return render_template("feedback.html")




@app.route('/thank',methods=["GET","POST"])
def thank():
  return render_template("thank.html")

@app.route('/discounts',methods=["GET","POST"])
def discounts():
  return render_template("discounts.html")









if __name__ == '__main__':
    app.run( debug=True)
