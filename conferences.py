# Dumps all of this data to a csv
import csv

def conference_ranking(final_ranking, sos_ranking):
    conference_aff = 'util/conferences.csv'

    f = open(conference_aff)
    conference_csv = csv.reader(f)

    conference_sos_map   = {}
    conference_final_map = {}

    for team in conference_csv:
        if team[1] not in conference_sos_map.keys():
            conference_sos_map[team[1]] = []
        if team[1] not in conference_ranking_map.keys():
            conference_ranking_map[team[1]] = []

        conference_sos_map[team[1]].append(sos_ranking[team[0]])
        conference_ranking_map[team[1]].append(final_ranking[team[0]])

        print(conference_sos_map)
        print(conference_ranking_map)
