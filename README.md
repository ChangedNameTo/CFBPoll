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
| 1 | Clemson | [](#f/clemson) | (3 - 0) | 1763.73 | Virginia | (**41** - 23) W | 13.61 |
| 2 | Alabama | [](#f/alabama) | (2 - 0) | 1729.77 | Texas A&M | (**52** - 24) W | 18.46 |
| 3 | LSU | [](#f/lsu) | (1 - 1) | 1719.85 | Vanderbilt | (7 - **41**) W | 13.08 |
| 4 | Georgia | [](#f/georgia) | (2 - 0) | 1708.32 | Auburn | (**27** - 6) W | 20.73 |
| 5 | Notre Dame | [](#f/notredame) | (2 - 0) | 1694.11 | South Florida | (**52** - 0) W | 15.66 |
| 6 | Florida | [](#f/florida) | (2 - 0) | 1664.41 | South Carolina | (**38** - 24) W | 11.85 |
| 7 | UCF | [](#f/ucf) | (2 - 1) | 1651.99 | Tulsa | (**26** - 34) L | -29.76 |
| 8 | Appalachian State | [](#f/appalachianstate) | (2 - 1) | 1648.87 | Campbell | (**52** - 21) W | 4.6 |
| 9 | Cincinnati | [](#f/cincinnati) | (3 - 0) | 1638.97 | South Florida | (**28** - 7) W | 14.2 |
| 10 | Memphis | [](#f/memphis) | (1 - 1) | 1628.82 | SMU | (30 - **27**) L | -12.74 |
| 11 | Air Force | [](#f/airforce) | (1 - 0) | 1626.87 | Navy | (**40** - 7) W | 24.65 |
| 12 | Oklahoma | [](#f/oklahoma) | (1 - 2) | 1625.79 | Iowa State | (37 - **30**) L | -21.81 |
| 13 | Louisiana | [](#f/louisiana) | (3 - 0) | 1625.7 | Georgia Southern | (**20** - 18) W | 6.36 |
| 14 | Florida Atlantic | [](#f/fau) | (1 - 0) | 1614.77 | Charlotte | (**21** - 17) W | 7.85 |
| 15 | BYU | [](#f/byu) | (3 - 0) | 1614.01 | Louisiana Tech | (**45** - 14) W | 27.34 |
| 16 | SMU | [](#f/smu) | (3 - 0) | 1609.73 | Memphis | (**30** - 27) W | 12.74 |
| 17 | Texas | [](#f/texas) | (2 - 0) | 1603.44 | TCU | (**31** - 33) L | -13.17 |
| 18 | Oklahoma State | [](#f/oklahomastate) | (3 - 0) | 1601.84 | Kansas | (7 - **47**) W | 18.47 |
| 19 | Auburn | [](#f/auburn) | (1 - 1) | 1597.5 | Georgia | (27 - **6**) L | -20.73 |
| 20 | Miami | [](#f/miami) | (3 - 0) | 1586.59 | Florida State | (**52** - 10) W | 24.97 |
| 21 | Virginia Tech | [](#f/virginiatech) | (2 - 0) | 1576.95 | Duke | (31 - **38**) W | 14.47 |
| 22 | Baylor | [](#f/baylor) | (1 - 1) | 1573.64 | West Virginia | (27 - **21**) L | -20.48 |
| 23 | Tennessee | [](#f/tennessee) | (2 - 0) | 1569.94 | Missouri | (**35** - 12) W | 23.5 |
| 24 | Texas A&M | [](#f/texasam) | (1 - 1) | 1564.6 | Alabama | (52 - **24**) L | -18.46 |
| 25 | Virginia | [](#f/virginia) | (1 - 1) | 1562.88 | Clemson | (41 - **23**) L | -13.61 |
|||||||||
| 63 | Georgia Tech | [](#f/georgiatech) | (1 - 2) | 1416.71 | Syracuse | (37 - **20**) L | -22.28 |
|||||||||
| 74 | Kansas | [](#f/kansas) | (0 - 3) | 1342.55 | Oklahoma State | (**7** - 47) L | -18.47 |

---

**Mean Elo:** 1525.46

**Median Elo:** 1527.02

**Standard Deviation of Elo:** 97.95

**Easiest Strength of Schedule:** UTEP

**Hardest Strength of Schedule:** Vanderbilt

**Predictions Quality (Season):** 77.48% Correct

**Predictions Quality (Week):** 65.62% Correct (Last Week: 86.67%)

[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)

[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)

Poll program runtime: 100.2s