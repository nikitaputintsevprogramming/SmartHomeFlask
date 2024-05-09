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
sensorsTemp = []

for count in range(9):
    array_name.append("wet_"+ str(count))
    sensorsTemp.append(things.Sensor(array_name[count]))

sensorsTempBedroom = (sensorsTemp[5], sensorsTemp[6], sensorsTemp[7], sensorsTemp[8])
humidifier = things.Humidifier('Main_humidifier', 35)

sensorsTempBathroom = (sensorsTemp[0], sensorsTemp[1], sensorsTemp[2], sensorsTemp[3], sensorsTemp[4])
humidifier_2 = things.Humidifier('Bedroom_humidifier', 35)
# ------------------ ------------------ ------------------ ------------------

# Log
def log_wet():
    # for count in range(len(sensorsTemp)):
    logger.insert_wet('DateOfComfort', sensorsTemp[0], sensorsTemp[1], sensorsTemp[2], sensorsTemp[3], sensorsTemp[4], sensorsTemp[5], sensorsTemp[6], sensorsTemp[7], sensorsTemp[8])
    Timer(1, log_wet).start()

log_wet()

# Разворачиваем интерфейс
@app.route('/mainUI')
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
        time.append(item['timeStamp'])
        avg_wet.append(np.average(list(item.values())[2:]))

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
@app.route('/upTempBath')
def start_page():
    humidifier.humidify(*sensorsTempBedroom)
    result = {}
    for sensor in sensorsTempBedroom:
        result[sensor.name] = sensor.value
    return result


@app.route('/upTempBed')
def bedroom_page():
    humidifier_2.humidify(*sensorsTempBathroom)
    result = {}
    for sensor in sensorsTempBathroom:
        result[sensor.name] = sensor.value
    return result
# -------------------


if __name__ == '__main__':
    app.run()
