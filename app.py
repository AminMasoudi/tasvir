#TODO : imports
from flask import Flask ,request ,redirect ,render_template ,session
from flask_session import Session
from werkzeug.security import check_password_hash
from helpers import apology, login_required
import sqlite3 as sql


#TODO : app conf
app = Flask(__name__)

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

#TODO : index(SHOW FILES)
@app.route("/")
def index():
    return apology("TODO")

#TODO : UPLOAD
@app.route("/upload")
def upload():
    return apology("TODO")

#TODO : login
@app.route("/login",methods=["GET","POST"])
def login():
    return apology("TODO")

#TODO : admin page
@app.route("/admin")
@login_required
def admin():
    return apology("TODO")