## NBA Fantasy Basketball Head to Head Categories Z-Score Analysis

This project calculates category z-scores for NBA players and produces overall fantasy rankings based on a supplied data set. The analysis script ingests player statistics from `input.csv`, standardizes each stat, sums the z-scores, and exports ranked results.

### Prerequisites

- Python 3.10+
- A virtual environment (the repo includes a `venv/` directory that can be recreated or replaced)
- Dependencies listed in `requirements.txt`

### Quick Start

```bash
cd /Users/elkingarcia/Documents/python/fantasy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python zscore_analysis.py
```

Running the script reads `input.csv`, prints the top 30 players in the console, and writes the full ranked table to `zscore_rankings.csv`.

### Sample Output

```
Rank  Player                         Total_ZScore  FG%_zscore  FT%_zscore  3:00 PM_zscore  REB_zscore  AST_zscore  STL_zscore  BLK_zscore  TO_zscore_inverted  PTS_zscore
1     Josh Giddey ChiSG, PG, SF              12.04        0.50        0.50             1.05        3.64        4.86        1.02       -0.79               -2.28        3.54
2     Will Richard GSSG, PF                  10.91        1.30        0.23             3.71        1.44        0.46        0.50       -0.79                0.15        3.91
3     Shai Gilgeous-Alexander OKCPG          10.31        0.23        0.86             1.45        0.56        3.04       -0.71        1.35               -0.70        4.23
4     Moses Moody GSSG, SF                    9.22        0.78        0.74             2.73       -0.18        0.29        0.50        2.85               -0.21        1.73
5     Ayo DosunmuDTD ChiSG                    8.65        2.15        0.56            -0.23        0.12        3.76        0.50       -0.79                0.15        2.42
```

### Input Format

The script expects a CSV with the following headers (case-sensitive) and numeric values for each category:

- `Player` – string; player name (additional team/position text is fine).
- `FG%` – field goal percentage expressed as a decimal (e.g., `0.512`).
- `FT%` – free throw percentage as a decimal.
- `3:00 PM` – three-pointers made per game.
- `REB` – rebounds per game.
- `AST` – assists per game.
- `STL` – steals per game.
- `BLK` – blocks per game.
- `TO` – turnovers per game.
- `PTS` – points per game.

All rows must include valid numeric data for every stat column. The final row in the source export often contains aggregate labels such as `STATS`; the script automatically drops the last row, so ensure actual player data appears above it.

Example snippet:

```
Player,FG%,FT%,3:00 PM,REB,AST,STL,BLK,TO,PTS
Player A,0.512,0.845,2.3,8.1,5.4,1.3,0.8,2.9,24.8
Player B,0.476,0.902,3.1,4.5,6.1,1.0,0.4,3.5,21.2
```

### Updating the Data

1. Replace or edit `input.csv` with the latest season or split (e.g., last 7 days).
2. Re-run `zscore_analysis.py`.
3. Find the generated CSV in the project root (e.g., `zscore_rankings.csv`).

### Output Files

- `zscore_rankings.csv` – default full-season rankings.
- `zscore_rankings_last_7.csv` – example recent-period rankings.
- `zscore_rankings_2025.csv` – example historical snapshot.

Each file includes the total z-score plus category-by-category z-scores for field goal percentage, free throw percentage, three-pointers made, rebounds, assists, steals, blocks, turnovers, and points.

### Notes

- The script assumes the input data already contains per-game or pace-adjusted stats that align with the target fantasy league format.
- To customize category weights or add new stats, modify `zscore_analysis.py` accordingly and rerun the script.
