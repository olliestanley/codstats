import pandas as pd


def main():
    matches = pd.read_csv("data/Matches.csv")

    while True:
        print(f"Enter match [Team1 Team2 Date IndexInDate] (Type 'exit' to finish)")

        user_input = input()
        if user_input == "exit":
            break

        try:
            team1_id, team2_id, date, index_in_date = user_input.split(" ")
            team1_id, team2_id, index_in_date = int(team1_id), int(team2_id), int(index_in_date)
            matches = pd.concat((matches, pd.DataFrame([[len(matches), date, index_in_date, team1_id, team2_id]], columns=matches.columns)))
        except Exception as e:
            print(e)
            continue

    matches.to_csv("data/Matches.csv", index=False)


if __name__ == "__main__":
    main()