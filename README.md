## codstats

Call of Duty League data and stats helpers. Supports the MW2 (2023) season.

### Data Acquisition

- Use BreakingPoint.gg for match data.
- If a player, team, map, or mode is not in the database add them to `data/[Players/Teams/Maps/Modes].csv`.
- Use `scripts/input_matches.py` to populate match records.
- Then use `scripts/input_games.py` to populate the individual game records for each match.
- Populate a new file `data/match_urls.txt` with a list of match urls to scrape, one line with a URL per match added which does not already have player stats populated.
- Then use `scripts/scrape_stats.py` to populate the individual player stats for each game.

If I have some time I may write a scraper to replace manual input for `input_matches` and `input_games`, but it's easy enough to keep up with matches being played.

Note: Output data files will not immediately be moved to the `data/` directory. Check data to ensure accuracy and then move them manually.

### Data Loading

Build merged frames as Pandas `DataFrame`:

```python
from codstats.pandas_data import PandasDataStore

store = PandasDataStore("data/")

overall_df = store.get_overall_dataframe()
rokkr_team_df = store.get_team_dataframe(team_name="Minnesota Rokkr")
attach_player_df = store.get_player_dataframe(player_name="Attach")
```

From here data can be manipulated as usual with Pandas.

Polars `DataFrame` format is also supported:

```python
from codstats.polars_data import PolarsDataStore

store = PolarsDataStore("data/")

overall_df = store.get_overall_dataframe()
rokkr_team_df = store.get_team_dataframe(team_name="Minnesota Rokkr")
attach_player_df = store.get_player_dataframe(player_name="Attach")
```

Alternatively the CSV files in `data/` can be loaded and manipulated manually.
