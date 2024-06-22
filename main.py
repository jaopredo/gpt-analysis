import pandas as pd
from functions.analytics.scale import analyse_comments
from functions.analytics.tables import generate_help_tables, update_table_with_indexes
from scraping import *

def main():
    # Realizando a raspagem de dados
    # scrap_from_web()

    # Passando os dados
    dataset_steam = pd.read_csv('data/steam_copy.csv', on_bad_lines="skip", sep=";")
    # dataset_imdb = pd.read_csv('data/steam.csv', on_bad_lines="skip", sep=";")
    
    # Criando tabelas auxiliares
    game_companies_table, games_table = generate_help_tables(dataset_steam)
    update_table_with_indexes(df=dataset_steam, games_companies_table=game_companies_table, games_table=games_table)
    
    # analyse_comments(dataset_steam)
    # generate_analytics(dataset_imdb)

    # Gerando o novo dataset
    dataset_steam.to_csv('data/new_steam.csv', sep=';', index=False)
    # dataset_imdb.to_csv('data/new_steam.csv', sep=';')



if __name__ == "__main__":
    main()
