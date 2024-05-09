import pymongo
import datetime


class Logger:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]

    def insert_wet(self, nameDB, *sensors):
        result = {'timeStamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for sensor in sensors:
            result[sensor.name] = sensor.value

        return self.db[nameDB].insert_one(result)

    def read_data(self, nameDB, value={}, field={}):
        return self.db[nameDB].find(value, field)
