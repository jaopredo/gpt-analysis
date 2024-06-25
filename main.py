import pandas as pd
from functions.analytics.scale import analyse_comments
from functions.analytics.tables import generate_help_tables, update_table_with_indexes
from functions.analytics.requisites import generate_requisites_analysis
from scraping import *

def main():
    # Realizando a raspagem de dados
    # scrap_from_web()

    # Passando os dados
    dataset_steam = pd.read_csv('data/steam_games.csv', on_bad_lines="skip", sep=";")
    games_dataset = pd.read_csv('data/imdb_game_company.csv', on_bad_lines="skip", sep=";")
    # dataset_imdb = pd.read_csv('data/steam.csv', on_bad_lines="skip", sep=";")
    
    generate_requisites_analysis(games_dataset)
    # analyse_comments(dataset_steam)

    # Gerando o novo dataset
    games_dataset.to_csv('data/imdb_games_company.csv', sep=";", index=False)
    dataset_steam.to_csv('data/steam.csv', sep=';', index=False)


if __name__ == "__main__":
    main()
