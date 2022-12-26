#TODO : imports
from flask import Flask ,request ,redirect ,render_template ,session
from flask_session import Session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required, maxNumber
import sqlite3 as sql


#TODO : app conf
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "upload"
#TODO : auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

#TODO : db
con = sql.connect("Final.db",check_same_thread=False)
con.row_factory = sql.Row
db = con.cursor()

#TODO : Session conf
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#TODO : routs

#DONE : index(SHOW FILES)
@app.route("/")
def index():
    return render_template("index.html",maxNumber = maxNumber())

#DONE : UPLOAD
@app.route("/upload",methods = ["GET","POST"])
def upload():
    if request.method=="POST":
        file = request.files["file"]
        file.save("static/load/" + secure_filename(file.filename))
        return redirect("/update")
    return render_template("upload.html")

#TODO : login
@app.route("/login",methods = ["GET","POST"])
def login():
    return apology("TODO")

#TODO : admin page
@app.route("/admin")
@login_required
def admin():
    return apology("TODO")

#TODO : logout