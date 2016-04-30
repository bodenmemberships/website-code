from mainsite.models import Countries
from mainsite.models import Regions

import csv

with open('data/country_to_region_mapping.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        rec = Countries.objects.get(country_UN=row[0])
        reg = Regions.objects.get(region_name=row[2])
        rec.region = reg
        rec.save()
