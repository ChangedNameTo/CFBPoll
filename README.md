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
| 1 | BYU | [](#f/byu) | (4 - 0) | 1606.64 | UT San Antonio | (**27** - 20) W | 13.25 |
| 2 | Clemson | [](#f/clemson) | (4 - 0) | 1591.09 | Miami | (**42** - 17) W | 27.67 |
| 3 | Georgia | [](#f/georgia) | (3 - 0) | 1582.2 | Tennessee | (**44** - 21) W | 24.83 |
| 4 | Alabama | [](#f/alabama) | (3 - 0) | 1578.3 | Ole Miss | (48 - **63**) W | 22.4 |
| 5 | Notre Dame | [](#f/notredame) | (3 - 0) | 1571.87 | Florida State | (**42** - 26) W | 18.14 |
| 6 | SMU | [](#f/smu) | (4 - 0) | 1570.99 | Memphis | (**30** - 27) W | 10.21 |
| 7 | Oklahoma State | [](#f/oklahomastate) | (3 - 0) | 1569.18 | Kansas | (7 - **47**) W | 28.5 |
| 8 | North Carolina | [](#f/northcarolina) | (3 - 0) | 1563.32 | Virginia Tech | (**56** - 45) W | 20.38 |
| 9 | Coastal Carolina | [](#f/coastalcarolina) | (3 - 0) | 1559.68 | Arkansas State | (**52** - 23) W | 24.98 |
| 10 | Marshall | [](#f/marshall) | (3 - 0) | 1558.9 | Western Kentucky | (14 - **38**) W | 27.27 |
| 11 | Cincinnati | [](#f/cincinnati) | (3 - 0) | 1556.0 | South Florida | (**28** - 7) W | 21.53 |
| 12 | Liberty | [](#f/liberty) | (4 - 0) | 1553.14 | Louisiana Monroe | (**40** - 7) W | 18.89 |
| 13 | Louisiana | [](#f/louisiana) | (3 - 0) | 1549.05 | Georgia Southern | (**20** - 18) W | 8.09 |
| 14 | Miami | [](#f/miami) | (3 - 1) | 1547.92 | Clemson | (42 - **17**) L | -27.67 |
| 15 | Army | [](#f/army) | (4 - 1) | 1543.77 | The Citadel | (**14** - 9) W | 3.81 |
| 16 | UCF | [](#f/ucf) | (2 - 1) | 1537.61 | Tulsa | (**26** - 34) L | -24.99 |
| 17 | UAB | [](#f/uab) | (3 - 1) | 1537.08 | UT San Antonio | (**21** - 13) W | 18.47 |
| 18 | Kansas State | [](#f/kansasstate) | (3 - 1) | 1536.34 | TCU | (14 - **21**) W | 19.47 |
| 19 | Florida | [](#f/florida) | (2 - 1) | 1534.21 | Texas A&M | (41 - **38**) L | -13.17 |
| 20 | Boston College | [](#f/bostoncollege) | (3 - 1) | 1528.47 | Pittsburgh | (**31** - 30) W | 5.85 |
| 21 | Air Force | [](#f/airforce) | (1 - 0) | 1527.16 | Navy | (**40** - 7) W | 27.16 |
| 22 | Pittsburgh | [](#f/pittsburgh) | (3 - 2) | 1526.48 | Boston College | (31 - **30**) L | -5.85 |
| 23 | Houston | [](#f/houston) | (1 - 0) | 1526.37 | Tulane | (**49** - 31) W | 26.37 |
| 24 | Troy | [](#f/troy) | (2 - 1) | 1525.95 | Texas State | (**37** - 17) W | 24.04 |
| 25 | Iowa State | [](#f/iowastate) | (3 - 1) | 1524.57 | Texas Tech | (**31** - 15) W | 20.89 |
|||||||||
| 51 | Georgia Tech | [](#f/georgiatech) | (2 - 2) | 1481.05 | Louisville | (**46** - 27) W | 26.72 |
|||||||||
| 76 | Louisiana Monroe | [](#f/ulm) | (0 - 5) | 1380.75 | Liberty | (40 - **7**) L | -18.89 |

---

**Mean Elo:** 1502.54

**Median Elo:** 1506.02

**Standard Deviation of Elo:** 45.74

**Easiest Strength of Schedule:** UTEP

**Hardest Strength of Schedule:** Houston

**Predictions Quality (Season):** 62.14% Correct

**Predictions Quality (Week):** 51.72% Correct (Last Week: 68.75%)

[Explanation of the poll methodology here](https://www.reddit.com/user/TehAlpacalypse/comments/dwfsfi/cfb_poll_30_oops/)

[Link to the github repository here](https://github.com/ChangedNameTo/CFBPoll)

Poll program runtime: 81.88s