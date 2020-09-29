# CFBPoll 4.0 by TheAlpacalypse - The Pandas Rewrite

Computerized poll to automatically rank college football teams each week
First install the dependencies using the command:

`pip install -r requirements.txt`

Then run the program using the command:

`python3 __main__.py`

Use `Constants.py` to tweak the values I use to generate the ranking. I have tried to avoid leaving any raw values in this main program to let users experiment.

---
|Rank|Team|Flair|Record|Elo|Last Played|Result|Change|
|---|---|---|---|---|---|---|---|
| 1 | Clemson | [](#f/clemson) | (2 - 0) | 1750.13 | The Citadel | (**49** - 0) W | 3.16 |
| 2 | Alabama | [](#f/alabama) | (1 - 0) | 1711.31 | Missouri | (19 - **38**) W | 18.29 |
| 3 | LSU | [](#f/lsu) | (0 - 1) | 1706.77 | Mississippi State | (**34** - 44) L | -31.79 |
| 4 | Notre Dame | [](#f/notredame) | (2 - 0) | 1694.11 | South Florida | (**52** - 0) W | 15.66 |
| 5 | Georgia | [](#f/georgia) | (1 - 0) | 1687.59 | Arkansas | (10 - **37**) W | 12.44 |
| 6 | UCF | [](#f/ucf) | (2 - 0) | 1681.75 | East Carolina | (28 - **51**) W | 12.81 |
| 7 | Florida | [](#f/florida) | (1 - 0) | 1652.55 | Ole Miss | (35 - **51**) W | 17.48 |
| 8 | Appalachian State | [](#f/appalachianstate) | (2 - 1) | 1648.87 | Campbell | (**52** - 21) W | 4.6 |
| 9 | Oklahoma | [](#f/oklahoma) | (1 - 1) | 1647.6 | Kansas State | (**35** - 38) L | -16.95 |
| 10 | Memphis | [](#f/memphis) | (1 - 0) | 1641.56 | Arkansas State | (**37** - 24) W | 15.85 |
| 11 | Louisiana | [](#f/louisiana) | (3 - 0) | 1625.7 | Georgia Southern | (**20** - 18) W | 6.36 |
| 12 | Cincinnati | [](#f/cincinnati) | (2 - 0) | 1624.77 | Army | (**24** - 10) W | 18.52 |
| 13 | Auburn | [](#f/auburn) | (1 - 0) | 1618.22 | Kentucky | (**29** - 13) W | 21.57 |
| 14 | Texas | [](#f/texas) | (2 - 0) | 1616.61 | Texas Tech | (56 - **63**) W | 14.31 |
| 15 | SMU | [](#f/smu) | (2 - 0) | 1596.99 | Stephen F. Austin | (**50** - 7) W | 6.1 |
| 16 | Baylor | [](#f/baylor) | (1 - 0) | 1594.12 | Kansas | (**47** - 14) W | 14.42 |
| 17 | BYU | [](#f/byu) | (2 - 0) | 1586.67 | Troy | (**48** - 7) W | 28.81 |
| 18 | Miami | [](#f/miami) | (3 - 0) | 1586.59 | Florida State | (**52** - 10) W | 24.97 |
| 19 | Oklahoma State | [](#f/oklahomastate) | (2 - 0) | 1583.37 | West Virginia | (**27** - 13) W | 18.54 |
| 20 | Texas A&M | [](#f/texasam) | (1 - 0) | 1583.06 | Vanderbilt | (**17** - 12) W | 8.87 |
| 21 | Virginia | [](#f/virginia) | (1 - 0) | 1576.48 | Duke | (**38** - 20) W | 17.48 |
| 22 | Louisiana Tech | [](#f/louisianatech) | (2 - 0) | 1571.43 | Houston Baptist | (**66** - 38) W | 6.45 |
| 23 | Virginia Tech | [](#f/virginiatech) | (1 - 0) | 1562.49 | NC State | (**45** - 24) W | 20.29 |
| 24 | Pittsburgh | [](#f/pittsburgh) | (3 - 0) | 1562.21 | Louisville | (**23** - 20) W | 9.92 |
| 25 | Marshall | [](#f/marshall) | (2 - 0) | 1560.76 | Appalachian State | (**17** - 7) W | 26.35 |
|||||||||
| 63 | Georgia Tech | [](#f/georgiatech) | (1 - 2) | 1416.71 | Syracuse | (37 - **20**) L | -22.28 |
|||||||||
| 72 | UTEP | [](#f/utep) | (3 - 1) | 1349.18 | Louisiana Monroe | (6 - **31**) W | 37.43 |

---

**Mean Elo:** 1522.77

**Median Elo:** 1524.82

**Standard Deviation of Elo:** 95.88

**Predictions Quality (Season):** 82.28% Correct

**Predictions Quality (Week):** 86.67% Correct (Last Week: 68.42%)

[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)

[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)

Poll program runtime: 69.64s