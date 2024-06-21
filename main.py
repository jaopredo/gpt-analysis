import pandas as pd
from analytics import *

def main():
    # Realizando a raspagem de dados
    ...
    
    # Executando a limpeza dos dados
    ...

    # Passando os dados
    dataset = pd.read_csv('data/steam.csv', on_bad_lines="skip", sep=";")
    
    generate_analytics(dataset)

    # Gerando o novo dataset
    dataset.to_csv('data/new_steam.csv', sep=';')


if __name__ == "__main__":
    main()
