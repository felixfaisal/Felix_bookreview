from flask import Flask,render_template, request

app= Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/response", methods=["POST"])
def response():
    username=request.form.get("username")
    return render_template("response.html", username=username)
