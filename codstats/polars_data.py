from pathlib import Path
from typing import Union

import polars as pl

from codstats.data import DataStore


class PolarsDataStore(DataStore):
    def __init__(self, data_directory: Union[Path, str]):
        super().__init__(data_directory)

    def load_csv(self, filename: str) -> pl.DataFrame:
        return pl.read_csv(self.data_directory / filename)

    def get_overall_dataframe(self) -> pl.DataFrame:
        df = self.load_csv("MatchesGames.csv")

        df_games = self.load_csv("Games.csv")
        df = df.join(df_games, left_on="Game", right_on="ID")

        df_matches = self.load_csv("Matches.csv")
        df = df.join(df_matches, left_on="Match", right_on="ID")

        df_maps = self.load_csv("Maps.csv")
        df = df.join(df_maps, left_on="Map", right_on="ID").rename({"Name": "MapName"})

        df_modes = self.load_csv("Modes.csv")
        df = df.join(df_modes, left_on="Mode", right_on="ID").rename({"Name": "ModeName"})

        df_teams = self.load_csv("Teams.csv")
        df = df.join(df_teams, left_on="Team1", right_on="ID").rename({"Name": "Team1Name"})
        df = df.join(df_teams, left_on="Team2", right_on="ID").rename({"Name": "Team2Name"})

        return df.sort(by=["Match", "Game"])

    def get_team_dataframe(self, team_id: int = None, team_name: str = None) -> pl.DataFrame:
        if team_id is None and team_name is None:
            raise ValueError("Must specify either team_id or team_name")

        df = self.get_overall_dataframe()

        if team_id is not None:
            df1 = df.filter(pl.col("Team1") == team_id)
            df2 = df.filter(pl.col("Team2") == team_id)
        else:
            df1 = df.filter(pl.col("Team1Name") == team_name)
            df2 = df.filter(pl.col("Team2Name") == team_name)

        df1 = df1.rename({"Team1": "Team", "Team1Name": "TeamName", "Team2": "Opponent", "Team2Name": "OpponentName", "Team1Score": "Score", "Team2Score": "OpponentScore"})
        df2 = df2.rename({"Team2": "Team", "Team2Name": "TeamName", "Team1": "Opponent", "Team1Name": "OpponentName", "Team2Score": "Score", "Team1Score": "OpponentScore"})

        return pl.concat([df1, df2], how="diagonal").sort(by=["Match", "Game"])

    def get_player_dataframe(self, player_id: int = None, player_name: str = None) -> pl.DataFrame:
        if player_id is None:
            if player_name is None:
                raise ValueError("Must specify either player_id or player_name")

            players = self.load_csv("Players.csv")
            player_id = players.filter((pl.col("Name") == player_name)).select("ID").item()

        df = self.load_csv("PlayersGames.csv")
        df = df.filter(pl.col("Player") == player_id)

        df_games = self.load_csv("Games.csv")
        df = df.join(df_games, left_on="Game", right_on="ID")

        df_matches_games = self.load_csv("MatchesGames.csv")
        df = df.join(df_matches_games, left_on="Game", right_on="Game")

        df_matches = self.load_csv("Matches.csv")
        df = df.join(df_matches, left_on="Match", right_on="ID")

        df_maps = self.load_csv("Maps.csv")
        df = df.join(df_maps, left_on="Map", right_on="ID").rename({"Name": "MapName"})

        df_modes = self.load_csv("Modes.csv")
        df = df.join(df_modes, left_on="Mode", right_on="ID").rename({"Name": "ModeName"})

        df_teams = self.load_csv("Teams.csv")
        df = df.join(df_teams, left_on="Team1", right_on="ID").rename({"Name": "Team1Name"})
        df = df.join(df_teams, left_on="Team2", right_on="ID").rename({"Name": "Team2Name"})

        df1 = df.filter(pl.col("Team1") == df["Team"])
        df2 = df.filter(pl.col("Team2") == df["Team"])
        df1 = df1.drop(columns=["Team1"]).rename({"Team1Name": "TeamName", "Team2": "Opponent", "Team2Name": "OpponentName", "Team1Score": "TeamScore", "Team2Score": "OpponentScore"})
        df2 = df2.drop(columns=["Team2"]).rename({"Team2Name": "TeamName", "Team1": "Opponent", "Team1Name": "OpponentName", "Team2Score": "TeamScore", "Team1Score": "OpponentScore"})

        return pl.concat([df1, df2], how="diagonal").sort(by=["Match", "Game"])
