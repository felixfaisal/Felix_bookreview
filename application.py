import os
import psycopg2
import sqlalchemy

from flask import Flask,render_template, request, session, redirect, url_for, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://lxkmowkqptjcgm:a5834dd9d25a29e13d062b5acae2982a5e101b5261fa16b9cc23a81159f4068e@ec2-54-83-27-162.compute-1.amazonaws.com:5432/d3rfbh0s2i8fs0")
db = scoped_session(sessionmaker(bind=engine))

app= Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
     if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
      "<b><a href = '/logout'>click here to log out</a></b>"
     return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"
@app.route("/login")
def login():
    if request.method == 'POST':
      session['username'] = request.form['username']
    return render_template("login.html")

@app.route("/response", methods=["POST","GET"])
def response():
   count=0
   data = db.execute("SELECT * FROM data ")
   username=request.form.get("username")
   password=request.form.get("password")
   return render_template("response.html", username=username, password=password, data=data, count=count)

@app.route("/logout")
def logout():
   session.pop('username', None)
   return redirect("/")


@app.route("/search", methods=["POST","GET"])
def search():
    book=request.form.get("book")
    return render_template("search.html", book=book)


@app.route("/register", methods=["POST","GET"])
def register():
	return render_template("register.html")

@app.route("/success", methods=["POST","GET"])
def success():
       username1=request.form.get("username1")
       password1=request.form.get("password1")
       db.execute("INSERT INTO data VALUES(:username,:password)",{"username":username1, "password":password1})
       db.commit()


       return render_template("success.html")
