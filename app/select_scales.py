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
        name = row[1]
        octaves = str(row[3])
        if row[2] == grade and row[0] == instrument:
            if len(name.split()) > 2:
                scale = f"{name}, {row[3]} octave"
                scales.append(scale)
                continue
            elif int(octaves) > 1:
                scale = f"{name} scale, {octaves} octaves"
                arp = f"{name} arpeggio, {octaves} octaves"
            else:
                scale = f"{name} scale, {octaves} octave"
                arp = f"{name} arpeggio, {octaves} octaves"
            scales.append(scale)
            scales.append(arp)
    return scales

