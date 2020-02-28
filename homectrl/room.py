from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response
)

from homectrl.auth import login_required
from homectrl.db import get_db


bp = Blueprint('room', __name__, url_prefix='/room')


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if g.user['usertype_fk'] != 1:
        response = make_response("You don't have permission to register a room", 401)
        return reponse
    if request.method == 'POST':
        db = get_db()
        error = None
        name = request.form['name']
        if not name:
            error = "You have to give the room a name"
        if db.execute("SELECT * FROM room WHERE name = ?;", (name, )).fetchone() is not None:
            error = "This room is already registered"
        if error is None:
            cur = db.execute("INSERT INTO room(name) VALUES(?);", (name,))
            db.commit()
            return redirect(url_for('index'))
    return render_template('room/register.html')

