from flask import Flask, render_template, request, json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from threading import Timer
import things
import logger
import re
from array import *
from things import sensors, devices

logger = logger.Logger('HomeInformation')

app = Flask(__name__)

# ------------------ Создание сенсоров и устройств (экзмепляров) ------------------

array_name_sensors = []
for count in range(12):
    array_name_sensors.append("sensor_"+ str(count))
    sensors.append(things.Sensor(array_name_sensors[count]))

sensorsWet = (sensors[0], sensors[1], sensors[2], sensors[3])
sensorsTemp = (sensors[4], sensors[5], sensors[6], sensors[7])
sensorsSmoke = (sensors[8])

MusicPlayer = things.Device('MusicPlayer', False)
LightValue = things.Device('LightValue', False)
# ------------------ ------------------ ------------------ ------------------

# ------------------ Log постоянный ------------------
def log_sensorsData():
    logger.insert_data_sensors('DateOfSensors', sensors)
    Timer(10, log_sensorsData).start()

log_sensorsData()

def log_devicesData():
    logger.insert_data_sensors('DateOfDevices', devices)
    # Timer(10, log_sensorsData).start()
# ------------------Разворачиваем интерфейс ------------------
@app.route('/')
def connect_interface():
    return render_template('mainUI.html')
# ----------------------

@app.route('/SetValues')
def set_values():
    print(f'Название: { request.args.get("name")}, Значение: {request.args.get("value")}')
    for device in devices:
        if(device.name == request.args.get("name")):
            device.value = request.args.get("value")
            log_devicesData()
    LightValue.value = request.args.get("check")
    print(request.args.get("check"))
    return json.dumps({'Название:': request.args.get('name'), 'Значение:': request.args.get('value')})

# ------------------ Выводим график изменений ------------------
@app.route('/GraphSensors')
def connect():
    cursor = logger.read_data('DateOfSensors')
    print(cursor)
    time = []
    avg_wet = []
    for item in cursor:
        if 'timeOfRead' in item:
            time.append(item['timeOfRead'])
            avg_wet.append(np.average(list(item.values())[2:]))
        else:
            print("Ключ 'timeOfRead' отсутствует в документе:", item)
            return {}

    x = np.arange(0, len(time))
    y = np.array(avg_wet)

    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.ylim(0, 50)
    plt.xlim()
    x = np.arange(len(time), len(time)*2)
    y_pred = np.poly1d(np.polyfit(x, y, 50))

    plt.plot(x, y_pred(x))
    plt.xticks(rotation=90)
    plt.ylim(0, 50)
    plt.show()
    return {}
# ------------------------------

# ------------------ Simulation ------------------
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
# -------------------

if __name__ == '__main__':
    app.run()