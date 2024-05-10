import pymongo
import datetime
import numpy as np
import matplotlib.pyplot as plt
from flask import request
from datetime import datetime as dt

import pymongo
import datetime
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from flask import request

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

class LoggerGraph(Logger):
    def __init__(self, db_name):
        super().__init__(db_name)
        print(f'Инициализация БД: {db_name}')

    def showGraph(self, name_collection):
        device_name = request.args.get("name")
        print(f'Считываем значение с датчика: {device_name}')

        if device_name is None:
            print("Имя датчика не передано в запросе.")
            return {}

        cursor = self.read_data(name_collection)
        time = []
        device_values = []

        for item in cursor:
            if 'timeOfRead' in item and device_name in item:
                time_str = item['timeOfRead']
                time.append(dt.strptime(time_str, '%Y-%m-%d %H:%M:%S').time())
                # device_values.append(item[device_name])
                value = item[device_name]
                if isinstance(value, (int, float)):
                    device_values.append(value)
                else:
                    print(f"Значение '{value}' не является числом, пропускаем.")
            else:
                print(f"Ключ 'timeOfRead' или датчик '{device_name}' отсутствует в документе:", item)
                return {}
        if not device_values:
            print("Нет числовых значений для построения графика.")
            return {}
        # print(f"до сортировки '{device_values}' ")
        # Выстраиваем числа по порядку от наим. к наиб.
        sorted_data = sorted(zip(time, device_values), key=lambda x: x[0])
        time, device_values = zip(*sorted_data)
        # print(f"после сортировки '{device_values}' ")
        print(f"Ключ 'timeOfRead' или датчик '{device_name}' отсутствует в документе:", item)
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
