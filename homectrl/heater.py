from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, make_response, jsonify
)
from bluetooth.ble import DiscoveryService
import eq3bt
from homectrl.auth import login_required
from homectrl.db import get_db


bp = Blueprint('heater', __name__, url_prefix='/heater')

class Heater:
    def __init__(self, row):
        self.id = row['id']
        self.mac = row['mac']
        self.name = row['name']
        self.room_fk = row['room_fk']
        self.room_name = None
        self.thermostat = None
        self.schedule = {}


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
    # Scan for thermostats, try to get current status
    service = DiscoveryService()
    devices = service.discover(5)
    macs = [mac for mac in devices if devices[mac] == 'CC-RT-BLE']
    db = get_db()
    heaters = []
    for mac in macs:
        h = {}
        h['mac'] = mac
        heater = db.execute("SELECT h.name, r.name as room FROM heater h JOIN room r ON h.room_fk = r.id WHERE h.mac = ?;", (mac,)).fetchone()
        if heater is not None:
            h['status'] = 'registered'
            h['name'] = heater['name']
            h['assigned_to'] = heater['room']
        else:
            h['status'] = 'unassigned'
        t = eq3bt.Thermostat(mac)
        try:
            t.update()
            h['target_temp'] = t.target_temperature
            h['mode'] = t.mode_readable
        except BTLEDisconnectError as e:
            print(f"Unable to connect to thermostat: {mac}")
        heaters.append(h)
    return render_template('heater/register.html', rooms=rooms, room=room, heaters=heaters)

