import pandas as pd

tabela_jogos = pd.read_csv("data/imdb_game_company.csv", sep=";")
tabela_requisitos = pd.read_csv("data/requisites_semicolon.csv", sep=";")

tabela_jogos['MINIMUM_REQUISITES'] = tabela_requisitos['MINIMUM_REQUISITES']
tabela_jogos['RECOMMENDED_SETUP'] = tabela_requisitos['RECOMMENDED_SETUP']

tabela_jogos.to_csv('data/imdb_game_company.csv', sep=";")
