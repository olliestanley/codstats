import random

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def main():
    matches = pd.read_csv("data/Matches.csv")
    players = pd.read_csv("data/Players.csv")
    matches_games = pd.read_csv("data/MatchesGames.csv")
    players_games = pd.read_csv("data/PlayersGames.csv")

    with open("data/match_urls.txt", "r") as f:
        urls = f.readlines()

    url_n = 0
    for match in matches.itertuples(False):
        team1, team2 = match[3], match[4]

        match_games = matches_games.loc[matches_games.Match == match[0], "Game"]

        if any(
            match_games.iloc[n] in players_games["Game"].to_numpy()
            for n in range(len(match_games))
        ):
            continue

        num_games = len(match_games)
        match_stats = get_data(urls[url_n], num_games)
        url_n += 1

        for game_idx, game_stats in enumerate(match_stats):
            for i, (player_name, player_stats) in enumerate(game_stats.items()):
                try:
                    player_team = team1 if i < 4 else team2
                    player_id = players.loc[players["Name"] == player_name, "ID"].values[0]
                    player_kills, player_deaths, player_damage = player_stats
                    game_id = matches_games.loc[matches_games.Match == match[0], "Game"].iloc[game_idx]
                    players_games = pd.concat((
                        players_games,
                        pd.DataFrame([[player_id, game_id, player_team, player_kills, player_deaths, player_damage]], columns=players_games.columns)
                    ), ignore_index=True)
                except Exception:
                    print(player_name)
                    raise

    players_games.to_csv("PlayersGames.csv", index=False)


def get_data(url: str, games: int):
    options = Options()
    options.add_argument('window-size=700,600')
    proxy = get_proxy()
    options.add_argument('--proxy-server="http={};https={}"'.format(proxy, proxy))
    prefs = {'profile.managed_default_content_settings.images': 2}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    match_stats = []
    for i in range(1, games + 1):
        game_stats = {}
        if i == 1:
            game_tab = driver.find_element(By.CSS_SELECTOR, f"div.game-{i}.game-tab")
        else:
            driver.execute_script(f"document.getElementsByClassName('game-{i} game-tab')[0].style.display = 'block';")
            game_tab = driver.find_element(By.CSS_SELECTOR, f"div.game-{i}.game-tab")
        players_el = game_tab.find_element(By.CSS_SELECTOR, "div.players")
        for team_el in players_el.find_elements(By.CSS_SELECTOR, "div.team"):
            for player_el in team_el.find_elements(By.CSS_SELECTOR, "div.player"):
                spans = player_el.find_elements(By.CSS_SELECTOR, "span")
                player_name = spans[0].text
                player_kills = spans[1].text
                player_deaths = spans[2].text
                player_damage = spans[5].text
                game_stats[player_name] = (player_kills, player_deaths, player_damage)
        match_stats.append(game_stats)
    driver.close()
    driver.quit()
    return match_stats


def get_proxy():
    options = Options()
    options.headless = True
    options.add_argument("window-size=700,600")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get("https://sslproxies.org/")
        table = driver.find_elements(By.TAG_NAME, 'table')[0]
        df = pd.read_html(table.get_attribute('outerHTML'))[0]
        df = df.iloc[np.where(~np.isnan(df['Port']))[0],:]
        ips = df['IP Address'].values
        ports = df['Port'].astype('int').values
        driver.quit()
        proxies = list()
        for i in range(len(ips)):
            proxies.append('{}:{}'.format(ips[i], ports[i]))
        i = random.randint(0, len(proxies)-1)
        return proxies[i]
    except Exception:
        driver.close()
        driver.quit()
        raise


if __name__ == "__main__":
    main()
