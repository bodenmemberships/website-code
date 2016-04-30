from mainsite.models import Regions

import csv

with open('data/regions.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        rec = Regions()
        rec.region_code = row[0]
        rec.region_name = row[1]
        rec.save()
