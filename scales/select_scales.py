import csv
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Scale:
    def __init__(self, instrument, grade, name, octaves, arp):
        self.instrument = instrument
        self.grade = grade
        self.name = name
        self.octaves = octaves
        self.arp = arp


def get_scales(instrument, grade):
    filename = os.path.join(basedir, 'scales.csv')

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        filtered_csv = filter(lambda r: instrument == r[0] and grade == r[1], csvreader)
        rows = [row for row in filtered_csv]

    return [Scale(instrument, grade, row[2], row[3], row[4] == 'T') for row in rows]
