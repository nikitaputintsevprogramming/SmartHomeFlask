from flask import Flask, render_template, request, json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from threading import Timer
import things

import re
from array import *
from things import sensors, devices

from logger import Logger as logger
from logger import LoggerGraph as lg

app = Flask(__name__)

array_name_sensors = []
for count in range(12):
    array_name_sensors.append("sensor_"+ str(count))
    sensors.append(things.Sensor(array_name_sensors[count]))

sensorsWet = (sensors[0], sensors[1], sensors[2], sensors[3])
sensorsTemp = (sensors[4], sensors[5], sensors[6], sensors[7])
sensorsSmoke = (sensors[8])

MusicPlayer = things.Device('MusicPlayer', False)
LightValue = things.Device('LightValue', False)

KitchenMusicPlayer = things.Device('KitchenMusicPlayer', False)
BedroomMusicPlayer = things.Device('BedroomMusicPlayer', False)
HollMusicPlayer = things.Device('HollMusicPlayer', False)
BathroomMusicPlayer = things.Device('BathroomMusicPlayer', False)

KitchenLightValue = things.Device('KitchenLightValue', False)
BedroomLightValue = things.Device('BedroomLightValue', False)
HollLightValue = things.Device('HollLightValue', False)
BathroomLightValue = things.Device('BathroomLightValue', False)

logger_instance = logger('HomeInformation')

def log_sensorsData():
    logger_instance.insert_data_sensors('DateOfSensors', sensors)
    Timer(10, log_sensorsData).start()
log_sensorsData()
   
@app.route('/')
def connect_interface():
    return render_template('mainUI.html')

@app.route('/SetValues')
def set_values():
    print(f'Название: { request.args.get("name")}, Значение: {request.args.get("value")}')
    for device in devices:
        if(device.name == request.args.get("name")):
            device.value = request.args.get("value")
            logger_instance.insert_data_sensors('DateOfDevices', devices)
    LightValue.value = request.args.get("check")
    return json.dumps({'Название:': request.args.get('name'), 'Значение:': request.args.get('value')})

@app.route('/GraphSensors')
def read_data_sensors():
    lg.connect('DateOfSensors', 'HomeInformation')

@app.route('/GraphDevices')
def read_data_devices():
    lg.connect('DateOfDevices', 'HomeInformation')

@app.route('/up')
def upSensorValue():
    things.SensorSimulator.valueUp(*sensors)
    result = {}
    for sensor in sensors:
        result[sensor.name] = sensor.value
    return result

@app.route('/down')
def downSensorValue():
    things.SensorSimulator.valueDown(*sensors)
    result = {}
    for sensor in sensors:
        result[sensor.name] = sensor.value
    return result

if __name__ == '__main__':
    app.run()