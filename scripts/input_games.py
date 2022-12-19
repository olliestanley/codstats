import pandas as pd


def main():
    matches = pd.read_csv("data/Matches.csv")
    teams = pd.read_csv("data/Teams.csv", index_col="ID")
    maps = pd.read_csv("data/Maps.csv")
    modes = pd.read_csv("data/Modes.csv", index_col="ID")
    games = pd.read_csv("data/Games.csv")
    matches_games = pd.read_csv("data/MatchesGames.csv")

    map_aliases = {
        "Ho": "Breenbergh-Hotel",
        "Me": "Mercado-Las-Almas",
        "Hy": "Zarqwa-Hydroelectric",
        "Fo": "Al-Bagra-Fortress",
        "El": "El-Asilo",
        "Em": "Embassy",
    }

    exit = False

    for row in matches.itertuples(False):
        if exit:
            break

        match_id, date, index_in_date, team1, team2 = row
        if len(matches_games[matches_games.Match == match_id]) > 0:
            continue

        team1_name, team2_name = teams.loc[team1, "Name"], teams.loc[team2, "Name"]

        print(f"Match between {team1_name} and {team2_name} on {date} (#{index_in_date})")

        t1w, t2w = 0, 0
        game_idx = 0
        bo7 = False

        while True:
            mode_id = game_idx_to_mode_id(game_idx, bo7)
            mode_name = modes.loc[mode_id, "Name"]

            print(f"Game {game_idx + 1}, {mode_name}")
            print(f"Enter result [Map `{team1_name} Score` `{team2_name} Score`]")
            print("Type 'bo7' to toggle BO7, 'exit' to finish")

            user_input = input()
            if user_input == "bo7":
                bo7 = not bo7
                continue
            if user_input == "exit":
                exit = True
                break

            try:
                map_name, team1_score, team2_score = user_input.split(" ")
                if map_name in map_aliases:
                    map_name = map_aliases[map_name]
                team1_score, team2_score = int(team1_score), int(team2_score)
                map_id = maps.loc[maps["Name"] == map_name, "ID"].iloc[0]
                if team1_score > team2_score:
                    t1w += 1
                else:
                    t2w += 1
                games = pd.concat((games, pd.DataFrame([[len(games), map_id, mode_id, team1_score, team2_score]], columns=games.columns)))
                matches_games = pd.concat((matches_games, pd.DataFrame([[match_id, game_idx, len(games) - 1]], columns=matches_games.columns)))
            except Exception as e:
                print(e)
                continue

            threshold = 4 if bo7 else 3
            if t1w == threshold or t2w == threshold:
                break

            game_idx += 1

    games.to_csv("data/Games.csv", index=False)
    matches_games.to_csv("data/MatchesGames.csv", index=False)


def game_idx_to_mode_id(game_idx, bo7: bool):
    hps = [0,3] if bo7 else [0, 3]
    snds = [1,4,6] if bo7 else [1, 4]
    if game_idx in hps:
        return 0
    if game_idx in snds:
        return 1
    return 2


if __name__ == "__main__":
    main()