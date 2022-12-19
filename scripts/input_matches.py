import pandas as pd


def main():
    matches = pd.read_csv("data/Matches.csv")
    teams = pd.read_csv("data/Teams.csv")

    while True:
        print(f"Enter match [Team1 Team2 Date IndexInDate] (Type 'exit' to finish)")

        user_input = input()
        if user_input == "exit":
            break

        try:
            team1_name, team2_name, date, index_in_date = user_input.split(" ")
            team1_id, team2_id = teams[teams.Name == team1_name].ID.iloc[0], teams[teams.Name == team2_name].ID.iloc[0]
            index_in_date = int(index_in_date)
            matches = pd.concat((matches, pd.DataFrame([[len(matches), date, index_in_date, team1_id, team2_id]], columns=matches.columns)))
        except Exception as e:
            print(e)
            continue

    matches.to_csv("data/Matches.csv", index=False)


if __name__ == "__main__":
    main()