from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response, jsonify
)

from homectrl.auth import login_required
from homectrl.db import get_db
from homectrl.heater import Heater
from eq3bt import Thermostat

bp = Blueprint('room', __name__, url_prefix='/room')

def get_room(room_name):
    db = get_db()
    room = db.execute("SELECT * FROM room WHERE name = ?;", (room_name, )).fetchone()
    return room 


def get_heaters(room):
    db = get_db()
    heaters = db.execute("SELECT * FROM heater WHERE room_fk = ?;", (room['id'], )).fetchall()
    updated_heaters = []
    for heater in heaters:
        h = Heater(heater)
        h.room_name = room['name']
        h.thermostat = Thermostat(heater['mac'])
        h.thermostat.update()
        updated_heaters.append(h)
    return updated_heaters

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


@bp.route('/<room_name>', methods=['GET', 'POST'])
def view(room_name):
    room = get_room(room_name)
    heaters = get_heaters(room)
    return render_template('room/view.html', room=room, heaters=heaters)


@bp.route('/<room_name>/schedule')
def view_schedule(room_name):
    room = get_room(room_name)
    heaters = get_heaters(room)
    for heater in heaters:
        for day in range(7):
            heater.thermostat.query_schedule(day)
            heater.schedule[day] = heater.thermostat.schedule
    return render_template('room/view_schedule.html', room=room, heaters=heaters)

@bp.route('/<room_name>/set_target_temp', methods=['POST'])
@login_required
def set_temp(room_name):
    db = get_db()
    room = get_room(room_name)
    heaters = get_heaters(room)
    new_temp = float(request.form['target_temp'])
    for heater in heaters:
        heater.thermostat.target_temperature = new_temp
    return jsonify({'success': f'target temperature set to {new_temp}'})


