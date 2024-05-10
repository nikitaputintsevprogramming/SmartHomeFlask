import pymongo
import datetime
import numpy as np
import matplotlib.pyplot as plt
from flask import request
from datetime import datetime as dt


class Logger:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]

    def insert_data_sensors(self, nameDB, sensorsArray):
        result = {'timeOfRead': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for sensor in sensorsArray:
            result[sensor.name] = sensor.value
        return self.db[nameDB].insert_one(result)

    def read_data(self, nameDB, value={}, field={}):
        return self.db[nameDB].find(value, field)

class LoggerGraph:
    def connect(name_collection, name_bd):
        logger = Logger(name_bd)

        # Получаем имя датчика из запроса
        device_name = request.args.get("name")
        print(f'Считываем значение с датчика: {device_name}')

        if device_name is None:
            print("Имя датчика не передано в запросе.")
            return {}

        # Получаем данные из коллекции БД
        cursor = logger.read_data(name_collection)

        time = []
        device_values = []

        for item in cursor:
            if 'timeOfRead' in item and device_name in item:
                time_str = item['timeOfRead']
                time.append(dt.strptime(time_str, '%Y-%m-%d %H:%M:%S').time())
                device_values.append(item[device_name])
            else:
                print(f"Ключ 'timeOfRead' или датчик '{device_name}' отсутствует в документе:", item)
                return {}

        x = np.array([t.hour + t.minute / 60 for t in time])
        y = np.array(device_values)

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