from pathlib import Path
from typing import Any, Union


class DataStore:
    def __init__(self, data_directory: Union[Path, str]):
        self.data_directory = Path(data_directory)

    def load_csv(self, filename: str) -> Any:
        raise NotImplementedError()

    def get_overall_dataframe(self) -> Any:
        raise NotImplementedError()

    def get_team_dataframe(self, team_id: int = None, team_name: str = None) -> Any:
        raise NotImplementedError()

    def get_player_dataframe(self, player_id: int = None, player_name: str = None) -> Any:
        raise NotImplementedError()
