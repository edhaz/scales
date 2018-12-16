import csv
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def get_scales(instrument, grade):
    filename = os.path.join(basedir, 'scales.csv')
    scales = []

    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)

    for row in rows:
        # define rows
        csv_instrument = row[0]
        csv_grade = row[1]
        csv_name = row[2]
        csv_octaves = row[3]
        csv_arp = row[4]

        if csv_grade == grade and csv_instrument == instrument:
            if csv_arp == 'T':
                if csv_octaves == 1:
                    scale = "{}, {} octave".format(csv_name, csv_octaves)
                    arp = "{} arpeggio, {} octave".format(csv_name, csv_octaves)
                elif int(csv_octaves) > 1:
                    scale = "{} scale, {} octaves".format(csv_name, csv_octaves)
                    arp = "{} arpeggio, {} octaves".format(csv_name, csv_octaves)
                scales.append(scale)
                scales.append(arp)
            elif csv_arp == 'F':
                if csv_octaves == '1':
                    scale = "{}, {} octave".format(csv_name, csv_octaves)
                elif int(csv_octaves) > 1:
                    scale = "{} scale, {} octaves".format(csv_name, csv_octaves)
                scales.append(scale)

    return scales

if __name__ == "__main__":
    x = get_scales('violin', '4')
    for i in x:
        print(i)
