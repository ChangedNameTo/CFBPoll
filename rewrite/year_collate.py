# needed to open csvs
import csv

def main(args):
    week = args[1]
    year = args[2]

    # Define our output file
    year_csv  = year + '/' + year +'_weekly_elo.csv'

    with open(year_csv, 'a+') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        # Output header row
        writer.writerow(('Team', 'Week', 'ELO', 'Rank'))

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

                writer.writerow((team[1], x, team[5], team[0]))

if __name__ == '__main__':
    import sys
    main(sys.argv)
