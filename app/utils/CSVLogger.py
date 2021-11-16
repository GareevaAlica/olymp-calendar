from datetime import datetime
import csv


class CSVLogger:
    file = 'logs.csv'
    headers = ['action', 'client', 'content', 'time']

    def __init__(self):
        with open(self.file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def add_row(self, data):
        with open(self.file, 'a', encoding='UTF8',
                  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data + [datetime.now()])


logger = CSVLogger()
