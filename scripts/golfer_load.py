import csv

from golfpicks.models import Golfer

def run():
    fhand = open('golfers.csv')
    reader = csv.reader(fhand)

    for row in reader:
        print(row)
        b, created = Golfer.objects.get_or_create(name=row[0])