import csv

f = open('new_teams.txt','r')

with open('2018SeedFile.csv','a') as seed:
    writer = csv.writer(seed)
    writer.writerow(())
    name = f.readline().replace('\n','')
    while name:
        writer.writerow((name,1500,'REPLACE',False))
        name = f.readline().replace('\n','')