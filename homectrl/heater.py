from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response, jsonify
)
from bluetooth.ble import DiscoveryService

from homectrl.auth import login_required
from homectrl.db import get_db


bp = Blueprint('heater', __name__, url_prefix='/heater')


@bp.route('/register/<int:room_id>', methods=['GET', 'POST'])
@login_required
def register(room_id):
    if g.user['usertype_fk'] != 1:
        response = make_response("You don't have permission to register a heater", 401)
        return reponse
    db = get_db()
    if request.method == 'POST':
        error = None
        mac = request.form['mac']
        name = request.form['name']
        room_id = request.form['room_id']
        if not name:
            error = "You have to give the heater a name"
        if db.execute("SELECT * FROM heater WHERE name = ?;", (name, )).fetchone() is not None:
            error = "This heater is already registered"
        if error is None:
            cur = db.execute("INSERT INTO heater(mac, name, room_fk) VALUES(?, ?, ?);", (mac, name, room_id))
            db.commit()
            return redirect(url_for('room.view', room_id=room_id))
    rooms = db.execute("SELECT * FROM room;").fetchall()
    room = db.execute("SELECT * FROM room WHERE id = ?;", (room_id, )).fetchone()
    return render_template('heater/register.html', rooms=rooms, room=room)


@bp.route('/register/scan')
@login_required
def scan():
    service = DiscoveryService()
    devices = service.discover(10)
    macs = [mac for mac in devices if devices[mac] == 'CC-RT-BT']
    db = get_db()
    heaters = {}
    for mac in macs:
        heater = db.execute("SELECT h.name, r.name as room FROM heater h JOIN room r ON h.room_fk = r.id WHERE h.mac = ?;", (mac,)).fetchone()
        if heater is not None:
            heaters[mac] = f"{heater['name']} ({heater['room']})"
        else:
            heater[mac] = 'unassigned'
    return jsonify(heaters)


