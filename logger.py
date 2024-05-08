import pymongo
import datetime


class Logger:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]

    def insert_wet(self, *sensors):
        result = {'timeStamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for sensor in sensors:
            result[sensor.name] = sensor.value

        return self.db['wet'].insert_one(result)

    def read_data(self, collection, value={}, field={}):
        return self.db[collection].find(value, field)
