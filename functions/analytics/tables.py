import pandas as pd


def generate_help_tables(df: pd.DataFrame):
    # Create the dataframes
    game_companies_table = pd.DataFrame(columns=[ 'COMPANY NAME' ])
    games_table = pd.DataFrame(columns=[ 'GAME NAME' ])

    # Creating the games table
    games_table['GAME NAME'] = df['GAME NAME'].unique()
    
    games_table.to_csv('data/games.csv', index_label='id', sep=';')  # Export to csv

    # Creating the games companies table
    game_companies_table['COMPANY NAME'] = df['GAME STUDIO'].unique()

    game_companies_table.to_csv('data/game_companies.csv', index_label='id', sep=';')  # Export to csv
