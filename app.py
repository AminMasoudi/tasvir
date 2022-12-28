#TODO : imports
from flask import Flask ,request ,redirect ,render_template ,session
from flask_session import Session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required, addresses, save, upgrade, load_waited_img
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
    return render_template("index.html",addresses = addresses())

#DONE : UPLOAD
@app.route("/upload",methods = ["GET","POST"])
def upload():
    if request.method=="POST":

        if (file:=request.files["file"]):
            if save(file)== 1:
                return apology("file did not saved")
            #TODO : redirect with seccess mesage
            return redirect("/upload")


        else:
            #TODO : send erorr
            return apology("no file uploaded", )
    return render_template("upload.html")

#DONE : login
@app.route("/login",methods = ["GET","POST"])
def login():
    """Log user in"""

    if request.method == "POST":

        #Forget any Admin_id
        session.clear()

        #Ensure username was provided
        if not (username:=request.form.get("username")):
            return apology("must provid username",403)
        elif not (passIntry:=request.form.get("password")):
            return apology("must provid password",403)
        
        #ask db for username info
        row = db.execute("SELECT * FROM admins WHERE username=? ;", (username,)).fetchall()
        
        #check if username not exiced or password is not correct 
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password")):
            return apology("username or password is wrong")

        #remember whitch user has loged in
        session["user_id"] = row[0]["id"]
        return redirect("/admin")
    else:
        return render_template("AdminLogin.html")

#TODO : admin page
@app.route("/admin",methods=["GET","POST"])
@login_required
def admin():
    if request.method=="POST":
        if request.form["AdminButton"] == "Y":
            #TODO : move to upload db
            upgrade(request.form.get(id))
            return apology("TODO")
        else:
            #TODO : delete img
            return apology("TODO")

        return redirect("/admin")

    WaitingList = load_waited_img()
    return render_template("Admin.html",WaitingList=WaitingList)
#DONE : logout
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")
