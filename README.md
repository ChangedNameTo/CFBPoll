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
| 1 | Army |  | (2 - 0) | 1556.84 | Louisiana Monroe | (*37* - 7) W | 25.9 |
| 2 | Notre Dame |  | (2 - 0) | 1553.73 | South Florida | (*52* - 0) W | 31.45 |
| 3 | SMU |  | (2 - 0) | 1553.07 | North Texas | (35 - *65*) W | 32.74 |
| 4 | Miami |  | (2 - 0) | 1549.88 | Louisville | (34 - *47*) W | 25.69 |
| 5 | Louisiana |  | (2 - 0) | 1540.96 | Georgia State | (31 - *34*) W | 12.7 |
| 6 | Clemson |  | (2 - 0) | 1540.48 | The Citadel | (*49* - 0) W | 9.01 |
| 7 | BYU |  | (1 - 0) | 1538.81 | Navy | (3 - *55*) W | 38.81 |
| 8 | Coastal Carolina |  | (2 - 0) | 1534.7 | Campbell | (*43* - 21) W | 7.6 |
| 9 | UCF |  | (1 - 0) | 1533.88 | Georgia Tech | (21 - *49*) W | 33.88 |
| 10 | Texas |  | (1 - 0) | 1533.84 | UTEP | (*59* - 3) W | 33.84 |
| 11 | Troy |  | (0 - 0) | 1532.1 | Middle Tennessee | (14 - *47*) W | 32.1 |
| 12 | Marshall |  | (2 - 0) | 1531.63 | Appalachian State | (*17* - 7) W | 20.33 |
| 13 | Pittsburgh |  | (2 - 0) | 1529.48 | Syracuse | (*21* - 10) W | 18.36 |
| 14 | Boston College |  | (1 - 0) | 1528.3 | Duke | (6 - *26*) W | 28.3 |
| 15 | North Carolina |  | (1 - 0) | 1526.8 | Syracuse | (*31* - 6) W | 26.8 |
| 16 | Memphis |  | (1 - 0) | 1521.71 | Arkansas State | (*37* - 24) W | 21.71 |
| 17 | UT San Antonio |  | (2 - 0) | 1519.79 | Stephen F. Austin | (*24* - 10) W | 6.85 |
| 18 | Oklahoma State |  | (1 - 0) | 1518.94 | Tulsa | (*16* - 7) W | 18.94 |
| 19 | Liberty |  | (1 - 0) | 1518.09 | Western Kentucky | (24 - *30*) W | 18.09 |
| 20 | Oklahoma |  | (1 - 0) | 1510.75 | Missouri State | (*48* - 0) W | 10.75 |
| 21 | NC State |  | (1 - 0) | 1510.44 | Wake Forest | (*45* - 42) W | 10.44 |
| 22 | West Virginia |  | (1 - 0) | 1510.11 | Eastern Kentucky | (*56* - 10) W | 10.11 |
| 23 | South Alabama |  | (1 - 1) | 1510.04 | Tulane | (*24* - 27) L | -14.25 |
| 24 | Cincinnati |  | (1 - 0) | 1509.41 | Austin Peay | (*55* - 20) W | 9.41 |
| 25 | Louisiana Tech |  | (1 - 0) | 1506.41 | Southern Mississippi | (30 - *31*) W | 6.41 |
|||||||||
| 38 | Georgia Tech |  | (1 - 1) | 1479.68 | UCF | (*21* - 49) L | -33.88 |
|||||||||
| 52 | Middle Tennessee |  | (0 - 1) | 1436.96 | Troy | (*14* - 47) L | -32.1 |

---

**Mean Elo:** 1502.25

**Median Elo:** 1502.7

**Standard Deviation of Elo:** 30.7

**Predictions Quality (Season):** 61.22% Correct

**Predictions Quality (Week):** 20.41% Correct (Last Week: 28.57%)

[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)

[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)

Poll program runtime: 1.11s