import pandas as pd
from analytics import *
from scraping import *

def main():
    # Realizando a raspagem de dados
    # scrap_from_web()
    
    # Executando a limpeza dos dados
    ...

    # Passando os dados
    dataset_steam = pd.read_csv('data/steam.csv', on_bad_lines="skip", sep=";")
    dataset_imdb = pd.read_csv('data/steam.csv', on_bad_lines="skip", sep=";")

    
    generate_analytics(dataset_steam)
    generate_analytics(dataset_imdb)


    # Gerando o novo dataset
    dataset_steam.to_csv('data/new_steam.csv', sep=';')
    dataset_imdb.to_csv('data/new_steam.csv', sep=';')



if __name__ == "__main__":
    main()
