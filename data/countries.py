from mainsite.models import Countries

import csv

with open('data/country_data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        rec = Countries()
        rec.country_name = row[0]
        rec.country_ISO = row[1]
        rec.country_UN = row[2]
        rec.country_UN_number = int(row[3])
        rec.country_dial_code = row[4]
        rec.save()
