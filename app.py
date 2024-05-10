from flask import Flask, render_template, request, json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime as dt

from threading import Timer
import things
import logger
import re
from array import *
from things import sensors, devices

logger = logger.Logger('HomeInformation')

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

def log_sensorsData():
    logger.insert_data_sensors('DateOfSensors', sensors)
    Timer(10, log_sensorsData).start()

log_sensorsData()

def log_devicesData():
    logger.insert_data_sensors('DateOfDevices', devices)
   
@app.route('/')
def connect_interface():
    return render_template('mainUI.html')

@app.route('/SetValues')
def set_values():
    print(f'Название: { request.args.get("name")}, Значение: {request.args.get("value")}')
    for device in devices:
        if(device.name == request.args.get("name")):
            device.value = request.args.get("value")
            log_devicesData()
    LightValue.value = request.args.get("check")
    return json.dumps({'Название:': request.args.get('name'), 'Значение:': request.args.get('value')})

@app.route('/GraphSensors')
def connect():
    cursor = logger.read_data('DateOfSensors')
    time = []
    average_value = []
    for item in cursor:
        if 'timeOfRead' in item:
            time_str = item['timeOfRead']
            time.append(dt.strptime(time_str, '%Y-%m-%d %H:%M:%S').time())
            average_value.append(np.average(list(item.values())[2:]))
        else:
            print("Ключ 'timeOfRead' отсутствует в документе:", item)
            return {}

    x = np.array([t.hour + t.minute / 60 for t in time])
    y = np.array(average_value)

    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.ylim(0, 50)
    plt.xlabel('Время дня')
    plt.ylabel('Значение')
    
    current_time = dt.now().time()
    plt.axvline(x=current_time.hour + current_time.minute / 60, color='r', linestyle='--', label='Текущее время')

    hours = range(0, 25, 1)  # интервал каждый час
    plt.xticks(hours, [f"{h:02}:00" for h in hours], rotation=90)

    plt.legend()
    plt.show()
    
    return {}

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