import csv


def get_scales(instrument, grade):
    filename = 'app/scales.csv'
    scales = []

    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)

    for row in rows:
        name = row[2]
        octaves = str(row[3])
        if row[1] == grade and row[0] == instrument:
            if octaves == 1:
                scale = "{}, {} octave".format(name, row[3])
                scales.append(scale)
                continue
            elif int(octaves) > 1:
                scale = "{} scale, {} octaves".format(name, octaves)
                arp = "{} arpeggio, {} octaves".format(name, octaves)
            else:
                scale = "{} scale, {} octave".format(name, octaves)
                arp = "{} arpeggio, {} octaves".format(name, octaves)
            scales.append(scale)
            scales.append(arp)
    return scales

