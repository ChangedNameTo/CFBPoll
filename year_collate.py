# needed to open csvs
import csv

def main(args):
    week = args[1]
    year = args[2]

    # Define our output file
    year_csv  = year + '/' + year +'_weekly_elo.csv'
    team_list = 'util/teams.txt'
    rank_map  = {}

    # Iterates to dump them all into an array
    fbs_teams = open(team_list, "r")
    for line in fbs_teams:
        if(len(line)>0):
            line = line.strip("\n")
            rank_map[line] = []


    for x in range(1,int(week) + 1):
        # Iterates over each of the weekly csvs
        f        = open(str(year) + "/week" + str(x) + ".csv", 'r')
        week_csv = csv.reader(f)
        next(week_csv, None)

        for team in week_csv:
            # The tamu exception
            if team[1] == 'Texas A&M;':
                team[1] = 'Texas A&M'

            if team[1] == 'Idaho':
                continue

            rank_map[team[1]].append(team[5])


    with open(year_csv, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        header = []
        for x in range(1, int(week) + 1):
            header.append(x)
        header.insert(0, 'Team')
        writer.writerow(header)

        for team in rank_map.keys():
            team_elo = []
            team_elo = rank_map[team]
            team_elo.insert(0, team)
            writer.writerow(team_elo)

if __name__ == '__main__':
    import sys
    main(sys.argv)
