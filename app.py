from flask import Flask, render_template, request
from threading import Timer
import things
import logger
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

logger = logger.Logger('IOT_Log')

app = Flask(__name__)

sensor_1 = things.Sensor('wet_1')
sensor_2 = things.Sensor('wet_2')
sensor_3 = things.Sensor('wet_3')
sensor_4 = things.Sensor('wet_4')
sensor_5 = things.Sensor('wet_5')
sensor_6 = things.Sensor('wet_6')
sensor_7 = things.Sensor('wet_7')
sensor_8 = things.Sensor('wet_8')
sensor_9 = things.Sensor('wet_9')

# for count in range 

sensors1 = (sensor_5, sensor_6, sensor_7, sensor_8, sensor_9)
humidifier = things.Humidifier('Main_humidifier', 25)

sensors2 = (sensor_1, sensor_2, sensor_3, sensor_4)
humidifier_2 = things.Humidifier('Bedroom_humidifier', 25)

def log_wet():
    logger.insert_wet(sensor_1, sensor_2, sensor_3,
                              sensor_4, sensor_5, sensor_6,
                              sensor_7, sensor_8, sensor_9)
    Timer(5, log_wet).start()

log_wet()

@app.route('/connect_interface')
def connect_interface():
    return render_template('connect_interface.html')


@app.route('/connect')
def connect():
    cursor = logger.read_data('wet')
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
    plt.ylim(0, 30)

    # model = LinearRegression().fit(x, y)
    # x = np.arange(len(time), len(time) * 2).reshape((-1, 1))
    # y_pred = model.predict(x)
    # plt.plot(x, y_pred)
    # plt.xticks(rotation=90)
    # plt.ylim(0, 30)
    # plt.show()


    x = np.arange(len(time), len(time)*2)
    y_pred = np.poly1d(np.polyfit(x, y, 30))

    plt.plot(x, y_pred(x))
    plt.xticks(rotation=90)
    plt.ylim(0, 30)
    plt.show()
    return {}


@app.route('/')
def start_page():
    humidifier.humidify(*sensors1)
    result = {}
    for sensor in sensors1:
        result[sensor.name] = sensor.value
    return result


@app.route('/bedroom')
def bedroom_page():
    humidifier_2.humidify(*sensors2)
    result = {}
    for sensor in sensors2:
        result[sensor.name] = sensor.value
    return result


if __name__ == '__main__':
    app.run()
