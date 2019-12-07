import csv

f = open('util/csvs/conferences.csv')

conferences = []

lines = f.read().splitlines()
for line in lines:
    portions = line.split(',')
    if portions[1] not in conferences:
        conferences.append(portions[1])

f.close()

final_ranking = 'util/seeds/2019SeedFile.csv'
f = open(final_ranking)
ranking_csv = csv.reader(f)

with open('2019SeedFile_Test.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

    for team in ranking_csv:
        name = team[0]
        elo = team[1]
        conference = team[2]
        p5 = team[3]
        bv_name = team[4]
        fbs = conference in conferences

        writer.writerow((name, elo, conference, p5, bv_name, fbs))