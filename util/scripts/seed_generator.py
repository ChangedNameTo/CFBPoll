import csv

conference_aff = 'util/conferences.csv'

f = open(conference_aff)
conference_csv = csv.reader(f)

conference_dict = {}
p5_dict = {}

for team in conference_csv:
    conference_dict[team[0]] = team[1]
    p5_dict[team[1]] = team[2]

f.close()

final_ranking = 'csv/2018/weekFinal.csv'
f = open(final_ranking)
ranking_csv = csv.reader(f)
next(ranking_csv)

with open('2019SeedFile.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

    for team in ranking_csv:
        name = team[1]
        elo = team[5]
        conference = conference_dict[name]
        p5 = p5_dict[conference]

        writer.writerow((name, elo, conference, p5))