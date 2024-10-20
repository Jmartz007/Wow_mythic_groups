import logging
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy

from sqlconnector.sqlReader import db

logger = logging.getLogger(f"main.{__name__}")


bp = Blueprint('auth', __name__, url_prefix='/groups/auth')

@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        with db.connect() as conn:
            user = conn.execute(sqlalchemy.text(
                """SELECT * FROM user where username = :username"""
            ), {"username": username}).first()
        
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user[2], password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session['username'] = user[1]
            return redirect(url_for('views.current_players'))
    
        flash(error, "error")

    return render_template('auth/login.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.username is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
            
@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    if username is None:
        g.username = None
        logger.debug(f"username is: {g.username}")
    else:
        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(
                """SELECT username FROM user WHERE username = :username"""), {"username": username}
            ).first()
            g.username = result[0]
            logger.debug(f"username is: {g.username}")