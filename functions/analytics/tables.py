import pandas as pd
import numpy as np


def generate_help_tables(df: pd.DataFrame):
    """This function generate som help tables, like one with games and unique id's for them, and the same
    with a companies table
    :param df: The dataframe of the games
    """

    # Create the dataframes
    game_companies_table = pd.DataFrame(columns=[ 'COMPANY NAME' ])
    games_table = pd.DataFrame(columns=[ 'GAME NAME', 'COMPANY ID' ])

    # Creating the games companies table
    game_companies_table['COMPANY NAME'] = df['GAME STUDIO'].unique()
    game_companies_table.to_csv('data/game_companies.csv', index_label='id', sep=';')  # Export to csv


    # Creating the games table
    games_table['GAME NAME'] = df['GAME NAME'].unique()
    # for i, company in enumerate(df['GAME STUDIO']):
    #     if 
        
    games_table.to_csv('data/games.csv', index_label='id', sep=';')  # Export to csv

    return game_companies_table, games_table


def update_table_with_indexes(df: pd.DataFrame, **kwargs):
    games_table = kwargs['games_table']
    games_companies_table = kwargs['games_companies_table']

    # for companie
