from flask import render_template, redirect, session
from functools import wraps


#TODO : apology


def apology(message, code=400):
    #def escape(s):
        # for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
        #                  ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        #     s = s.replace(old, new)
        # return s
    return render_template("apology.html",top = code, message=message), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
