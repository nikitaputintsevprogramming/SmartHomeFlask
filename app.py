from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from threading import Timer
import things
import logger
import re
from array import *

logger = logger.Logger('HomeInformation')

app = Flask(__name__)

# ------------------ Создание сенсоров (датчики температуры) ------------------
array_name = []
sensors = []

for count in range(12):
    array_name.append("wet_"+ str(count))
    sensors.append(things.Sensor(array_name[count]))

sensorsWet = (sensors[0], sensors[1], sensors[2], sensors[3])
sensorsTemp = (sensors[4], sensors[5], sensors[6], sensors[7])
sensorsSmoke = (sensors[8])

MusicPlayer = things.Device('Music player', 35)
LightValue = things.Device('Light value', 35)
# ------------------ ------------------ ------------------ ------------------

# Log
def log_data():
    # for count in range(len(sensorsTemp)):
    logger.insert_data('DateOfComfort', sensorsWet[0], sensorsWet[1], sensorsWet[2], sensorsWet[3])
    Timer(1, log_data).start()

log_data()

# Разворачиваем интерфейс
@app.route('/')
def connect_interface():
    return render_template('mainUI.html')
# ----------------------

# Выводим график изменений после послания рез-ов
@app.route('/connect')
def connect():
    cursor = logger.read_data('DateOfComfort')
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

    # x = np.arange(0, len(time)).reshape((-1, 1))
    x = np.arange(0, len(time))
    y = np.array(avg_wet)

    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.ylim(0, 50)

    # model = LinearRegression().fit(x, y)
    # x = np.arange(len(time), len(time) * 2).reshape((-1, 1))
    # y_pred = model.predict(x)
    # plt.plot(x, y_pred)
    # plt.xticks(rotation=90)
    # plt.ylim(0, 30)
    # plt.show()

    x = np.arange(len(time), len(time)*2)
    y_pred = np.poly1d(np.polyfit(x, y, 50))

    plt.plot(x, y_pred(x))
    plt.xticks(rotation=90)
    plt.ylim(0, 50)
    plt.show()
    return {}
# ------------------------------

# Simulation
@app.route('/up')
def upSensorValue():
    things.SensorSim.valueUp(*sensors)
    result = {}
    for sensor in sensors:
        result[sensor.name] = sensor.value
    return result


@app.route('/down')
def downSensorValue():
    things.SensorSim.valueDown(*sensors)
    result = {}
    for sensor in sensors:
        result[sensor.name] = sensor.value
    return result
# -------------------


if __name__ == '__main__':
    app.run()
