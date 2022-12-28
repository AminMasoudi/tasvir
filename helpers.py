from flask import render_template, redirect, session
from functools import wraps
from werkzeug.utils import secure_filename

import os
import sqlite3 as sql

con = sql.connect("Final.db",check_same_thread=False)
db = con.cursor()


def apology(message, code=400):
    #def escape(s):
        # for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
        #                  ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        #     s = s.replace(old, new)
        # return s
    return render_template("apology.html",top = code, message=message), code

#TODO : Login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def addresses():
    files = os.listdir("static/img")
    return ["static/img/"+ i for i in files]

def save(file, name="anonimus", discire="no discription"):
    try:
        no = db.execute("SELECT COUNT(*) FROM UPLOAD;").fetchall()[0][0]
        addr = "static/img/" + secure_filename(file.filename)
        file.save(addr)
        db.execute("INSERT INTO upload (no, name, discribe, addr) VALUES(? ,?, ?, ?);",(no ,name,discire,addr))
        return 0
    except:
        return 1

def upgrade():
    return

def discribe_spilit(my_tuple):
    my_list = list(my_tuple)
    my_list[2] = my_list[2].split("\n")
    return my_list
    

def load_waited_img():
    img_list = db.execute("SELECT * FROM upload ORDER BY no").fetchall()
    img_list = list(map(lambda x : discribe_spilit(x), img_list))
    return img_list