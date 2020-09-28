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
| 1 | Clemson |  | (2 - 0) | 1680.34 | The Citadel | (*49* - 0) W | 4.49 |
| 2 | LSU |  | (0 - 1) | 1650.72 | Mississippi State | (*34* - 44) L | -31.35 |
| 3 | Notre Dame |  | (2 - 0) | 1647.91 | South Florida | (*52* - 0) W | 18.99 |
| 4 | Alabama |  | (1 - 0) | 1638.1 | Missouri | (19 - *38*) W | 21.09 |
| 5 | UCF |  | (2 - 0) | 1636.23 | East Carolina | (28 - *51*) W | 17.84 |
| 6 | Georgia |  | (1 - 0) | 1634.85 | Arkansas | (10 - *37*) W | 17.02 |
| 7 | Louisiana |  | (3 - 0) | 1629.21 | Georgia Southern | (*20* - 18) W | 6.14 |
| 8 | Memphis |  | (1 - 0) | 1624.52 | Arkansas State | (*37* - 24) W | 16.35 |
| 9 | Appalachian State |  | (2 - 1) | 1623.83 | Campbell | (*52* - 21) W | 5.24 |
| 10 | Florida |  | (1 - 0) | 1614.17 | Ole Miss | (35 - *51*) W | 19.93 |
| 11 | SMU |  | (2 - 0) | 1609.39 | Stephen F. Austin | (*50* - 7) W | 5.85 |
| 12 | Cincinnati |  | (2 - 0) | 1602.51 | Army | (*24* - 10) W | 18.8 |
| 13 | Baylor |  | (1 - 0) | 1594.29 | Kansas | (*47* - 14) W | 16.41 |
| 14 | Oklahoma |  | (1 - 1) | 1594.24 | Kansas State | (*35* - 38) L | -15.88 |
| 15 | Texas |  | (2 - 0) | 1588.13 | Texas Tech | (56 - *63*) W | 15.85 |
| 16 | Auburn |  | (1 - 0) | 1580.71 | Kentucky | (*29* - 13) W | 22.16 |
| 17 | BYU |  | (2 - 0) | 1575.34 | Troy | (*48* - 7) W | 28.12 |
| 18 | Louisiana Tech |  | (2 - 0) | 1571.64 | Houston Baptist | (*66* - 38) W | 6.45 |
| 19 | Miami |  | (3 - 0) | 1568.24 | Florida State | (*52* - 10) W | 25.32 |
| 20 | Oklahoma State |  | (2 - 0) | 1566.23 | West Virginia | (*27* - 13) W | 17.97 |
| 21 | Navy |  | (1 - 1) | 1559.71 | Tulane | (24 - *27*) W | 12.96 |
| 22 | North Carolina |  | (1 - 0) | 1559.04 | Syracuse | (*31* - 6) W | 22.5 |
| 23 | Virginia |  | (1 - 0) | 1556.53 | Duke | (*38* - 20) W | 17.02 |
| 24 | Virginia Tech |  | (1 - 0) | 1552.01 | NC State | (*45* - 24) W | 19.44 |
| 25 | Tulane |  | (2 - 1) | 1546.66 | Southern Mississippi | (24 - *66*) W | 32.61 |
|||||||||
| 68 | Georgia Tech |  | (1 - 2) | 1391.73 | Syracuse | (37 - *20*) L | -22.31 |
|||||||||
| 72 | Louisiana Monroe |  | (0 - 3) | 1378.78 | UTEP | (*6* - 31) L | -35.07 |

---

**Mean Elo:** 1512.67

**Median Elo:** 1512.53

**Standard Deviation of Elo:** 79.08

**Predictions Quality (Season):** 79.75% Correct

**Predictions Quality (Week):** 16.46% Correct (Last Week: 21.52%)

[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)

[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)

Poll program runtime: 72.88s