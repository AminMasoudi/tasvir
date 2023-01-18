#TODO : imports
from flask import Flask ,request ,redirect ,render_template ,session, flash, url_for
from flask_session import Session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required, addresses, save, upgrade, load_waited_img, delete
import sqlite3 as sql


# app conf
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "upload"
#TODO : auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

#db connct
con = sql.connect("Final.db",check_same_thread=False)
con.row_factory = sql.Row
db = con.cursor()

#Session conf 
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


#routs
@app.route("/")
def index():
    """index (SHOW Images)\n
    `return render_template(index.html, addresses = addresses()`)"""
    return render_template("index.html",addresses = addresses())

@app.route("/upload",methods = ["GET","POST"])
def upload():
    """ UPLOAD images
    \nPOST :
    \n\tsave the image
    \nGET :
    \n\t `return render_template("upload.html")`  """
    if request.method=="POST":

        if (file:=request.files["file"]):
            discribe= request.form.get("discribe")
            name = request.form.get("name")       
            if save(file,name=name,discribe=discribe)== 1:
                return apology("file did not saved")
            #TODO : redirect with seccess mesage
            flash('Uploaded!!')
            return redirect(url_for("upload"))


        else:
            #TODO : send erorr
            return apology("no file uploaded", )
    return render_template("upload.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    """Login admins\n\tusername : admin\n\tpassword : admin"""

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
    """admin can confirm pictures or delete them
    \nby click on Y or N
    \nPOST :
    \n\tcheck admin's button and `return upgrade() if Y else delete()`
    \nGET :
    \n\tshow the waiteing_list by `return render_template("Admin.html",WaitingList=WaitingList)`  """
    if request.method=="POST":
        if request.form["AdminButton"] == "Y":
           return upgrade(request.form.get("my_id"))

        else:
            #TODO : delete img
            return delete(request.form.get("my_id"))
            
    WaitingList = load_waited_img()
    return render_template("Admin.html",WaitingList=WaitingList)
#DONE : logout
@app.route("/logout")
def logout():
    """Log admin out by clearing sessions and  `redirect("/")`"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/rools")
def rools():
    """shows the rolls & privecy pollocy by 
        \n\t `return render_template("rools.html")`"""
    return render_template("rools.html")