import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from homectrl.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    has_user = db.execute("SELECT count(*) FROM user;").fetchone()[0] 
    if has_user != 0 or (g.user is not None and g.user.usertype_fk != 1):
        return redirect(url_for('index'))
    if request.method == 'POST':
        error = None
        name = request.form['name']
        email = request.form['email']
        usertype = request.form['usertype']
        password = request.form['password']
        if not name:
            error = 'You forgot the name'
        if not email:
            error = 'You forgot the email'
        if not password:
            error = 'You forgot the password'
        if not usertype:
            error = "you forgot the user type"
        if error is None:
            cur = db.execute(
                  """
                  INSERT INTO
                  user (name, email, password, usertype_fk)
                  VALUES (?, ?, ?, ?)
                  """,
                  (name, email, generate_password_hash(password), usertype)
                  )
            db.commit()
        return redirect(url_for('index'))
    return render_template('auth/register.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        error = None
        email = request.form['email']
        password = request.form['password']
        user = db.execute("SELECT * FROM user WHERE email = ?", (email, )).fetchone()
        if user is None or not check_password_hash(user['password'], password):
                error = "Email unknown or password incorrect"
        if error is None:
                session.clear()
                session['uid'] = user['id']
                return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')    


@bp.route('/edit', methods=['GET', 'POST'])
def edit_user():
    return "Page to edit user data"


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('uid')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?;", (user_id, )).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view



