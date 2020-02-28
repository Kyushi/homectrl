from flask import (
	Blueprint, g, redirect, render_template, request, url_for
)
from homectrl.auth import login_required
from homectrl.db import get_db


bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    rooms = db.execute("SELECT * FROM room ORDER BY name;").fetchall()
    if not rooms:
        return redirect(url_for('room.register'))
    return render_template('index.html', rooms=rooms) 

