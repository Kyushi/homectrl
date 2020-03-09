from flask import (
	Blueprint, g, redirect, render_template, request, url_for, jsonify
)
from homectrl.auth import login_required
from homectrl.db import get_db
from homectrl.heater import Heater 
from eq3bt import Thermostat

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    rooms = db.execute("SELECT * FROM room ORDER BY name;").fetchall()
    if not rooms:
        return redirect(url_for('room.register'))
    return render_template('index.html', rooms=rooms) 



@bp.route('/air/start', methods=['POST'])
@login_required
def air_start():
    db = get_db()
    heaters = db.execute("SELECT * FROM heater").fetchall()
    response = {'message': 'success'}
    for heater in heaters:
        h = Heater(heater)
        h.thermostat = Thermostat(h.mac)
        h.thermostat.mode = 3  # set to manual mode (3)
        h.thermostat.target_temperature = 5
        h.thermostat.update()
        response[h.name] = {
                'temperature': h.thermostat.target_temperature,
                'mode': h.thermostat.mode_readable
                }
    return jsonify(response)
    

@bp.route('/air/end', methods=['POST'])
@login_required
def air_end():
    db = get_db()
    heaters = db.execute("SELECT * FROM heater").fetchall()
    response = {'message': 'success'}
    for heater in heaters:
        h = Heater(heater)
        h.thermostat = Thermostat(h.mac)
        h.thermostat.mode = 2  # Set mode to auto to return to current desired temperature
        h.thermostat.update()
        response[h.name] = {
                'temperature': h.thermostat.target_temperature,
                'mode': h.thermostat.mode_readable
                }
    return jsonify(response)

