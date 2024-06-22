import pandas as pd
from datetime import datetime


def sort_dates(dataframe: pd.DataFrame) -> list[dict]:
    dataframe['COMMENT_DATE'] = dataframe['DATA DE PUBLICAÇÃO DO COMENTÁRIO'].apply(
        lambda date: datetime.strptime(date, "%d/%m/%Y").timestamp()
    )  # 


def generate_timeline(dataframe: pd.DataFrame):
    raise NotImplementedError
    # # Pego a menor e a maior data
    # minimum_date = datetime.strptime(dataframe['DATA DE PUBLICAÇÃO DO COMENTÁRIO'].min(), "%d/%m/%Y")
    # maximum_date = datetime.strptime(dataframe['DATA DE PUBLICAÇÃO DO COMENTÁRIO'].max(), "%d/%m/%Y")
    
    # # Vou organizar as datas para que fiquem da menor para a maior
    # sorted_dates = sort_dates(dataframe['DATA DE PUBLICAÇÃO DO COMENTÁRIO'])

    # print(sorted_dates['dates'])
