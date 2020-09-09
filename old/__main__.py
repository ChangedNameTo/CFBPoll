from Ranking import Ranking

ranking = Ranking()
ranking.generate_weeks()
ranking.mean_reversion()
ranking.run_poll()

result = ranking.get_results()
ranking.get_elo_array(result)
ranking.set_mean_elo()
ranking.set_median_elo()
ranking.set_stdev_elo()
ranking.set_variance_elo()

ranking.generate_this_week()

ranking.get_sos_ranks()
ranking.get_weakest_sos()
ranking.get_hardest_sos()

ranking.markdown_output()

ranking.output_week_csv(result)
ranking.conference_ranking()
ranking.conference_output()

# Prediction time
ranking.parse_future()