import pandas as pd
from functions.analytics.scale import analyse_comments
from functions.analytics.requisites import generate_requisites_analysis
from scraping import *

def main():
    """
    The main program
    """

    # Scraping the informations from the WEB
    # scrap_from_web()

    # Getting the generated DATA and sending to get the analysis
    dataset_steam = pd.read_csv('data/steam_games.csv', on_bad_lines="skip", sep=";")
    games_dataset = pd.read_csv('data/steam_game_company.csv', on_bad_lines="skip", sep=";")
    
    generate_requisites_analysis(games_dataset)
    analyse_comments(dataset_steam)

    # Generating new CSV Files
    games_dataset.to_csv('data/imdb_game_company.csv', sep=";", index=False)
    dataset_steam.to_csv('data/steam.csv', sep=';', index=False)


if __name__ == "__main__":
    main()
