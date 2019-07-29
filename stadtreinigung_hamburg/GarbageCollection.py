from datetime import datetime

class GarbageCollection:
    def __init__(self, date, container, interval, uuid):
        self.date = date
        self.container = container
        self.interval = interval
        self.uuid = uuid

    def __str__(self):
        return self.date.strftime("%Y/%m/%d") + ' ' + self.container + ' ' + self.interval + '(' + self.uuid + ')'
