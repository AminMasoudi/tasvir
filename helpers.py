from flask import render_template, redirect, session
from functools import wraps
from werkzeug.utils import secure_filename

import os
import sqlite3 as sql

con = sql.connect("Final.db",check_same_thread=False)
db = con.cursor()


def apology(message:str ="TODO", code=400):
    
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
    address = db.execute("SELECT * FROM load ORDER BY NO DESC;").fetchall()
    address = list(map(lambda x:discribe_spilit(x), address))
    return address


def save(file, name="anonimus", discire="no discription"):
    try:
        no = db.execute("SELECT COUNT(*) FROM UPLOAD;").fetchall()[0][0]
        addr = "static/img/" + secure_filename(file.filename)
        file.save(addr)
        db.execute("INSERT INTO upload (no, name, discribe, addr) VALUES(? ,?, ?, ?);",(no ,name,discire,addr))
        con.commit()
        return 0
    except:
        return 1

def upgrade(id:str):
    
    try:
        row = db.execute("SELECT * FROM upload WHERE no=?",id).fetchall()[0]
        row = list(row)
        no = db.execute("SELECT COUNT(*) FROM load ;").fetchall()[0][0]
        db.execute("INSERT INTO load(no, name, discribe, addr) VALUES(?, ?, ?, ?);",(no, row[1], row[2], row[3]))
        db.execute("DELETE FROM upload WHERE no=?;",id)
        con.commit()
        
        return redirect("/admin")
    except:    
        return apology("db problem!!")
    

def discribe_spilit(my_tuple):
    my_list = list(my_tuple)
    my_list[2] = my_list[2].split("\n")
    return my_list
    

def load_waited_img():
    img_list = db.execute("SELECT * FROM upload ORDER BY no").fetchall()
    img_list = list(map(lambda x : discribe_spilit(x), img_list))
    return img_list

def delete(id:str):
    try:
        #TODO : delete img
        file_path = db.execute("SELECT addr FROM upload WHERE no=?",id).fetchall()[0][0]
        os.remove(file_path)
        db.execute("DELETE FROM upload WHERE no=?;",id)
        con.commit()
        return redirect("/admin")
    except:
        return apology("couldn't delete img from db our system")