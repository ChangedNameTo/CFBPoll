import csv

seed_file = '2019SeedFile.csv'

f = open(seed_file)
seed_csv = csv.reader(f)

with open('2018SeedFile.csv', 'w') as csv_file:
    new_writer = csv.writer(csv_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

    for row in seed_csv:
        name = row[0]
        elo = 1500
        conference = row[2]
        p5 = row[3]

        new_writer.writerow((name, elo, conference, p5))