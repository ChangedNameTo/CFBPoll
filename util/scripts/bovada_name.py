import csv

team_names = []
f = open('bovada_names.txt')
name = f.readline().replace('\n','')
while name:
    name = f.readline().replace('\n','')
    team_names.append(name)

with open('util/seeds/2019SeedFile.csv','r') as csvinput:
    with open('util/seeds/2019SeedFileNew.csv','w') as csvoutput:
        writer = csv.writer(csvoutput)
        reader = csv.reader(csvinput)

        copied_rows = []

        for row in reader:
            # No name attached
            if row[5] == 'REPLACE_ME':
                if row[0] in team_names:
                    row.append(row[0])
                    team_names.remove(row[0])
                else:
                    row.append('REPLACE_ME')

            copied_rows.append(row)

        writer.writerows(copied_rows)

with open('bovada_names.txt', 'w') as file:
    for name in team_names:
        file.write(name+'\n')