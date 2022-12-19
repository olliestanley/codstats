## codstats

Call of Duty League data and stats helpers. Supports the MW2 (2023) season.

### Data Acquisition

- Use BreakingPoint.gg for match data.
- If a player, team, map, or mode is not in the database add them to `[Players/Teams/Maps/Modes].csv`.
- Use `input_matches.py` to populate match records.
- Then use `input_games.py` to populate the individual game records for each match.
- Populate a new file `data/match_urls.txt` with a list of match urls to scrape, one line with a URL per match added which does not already have player stats populated.
- Then use `scrape_stats.py` to populate the individual player stats for each game.

Note: Output data files will not immediately be moved to the `data/` directory. Check data to ensure accuracy and then move them manually.
