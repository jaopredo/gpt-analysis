import pandas as pd

from functions.analytics.scale import *
from functions.analytics.dates import *


def generate_analytics(dataset: pd.DataFrame):
    """
        Função que gera as análises necessárias para criação de gráficos específicos
    """
    # analyse_comments(dataset)

    generate_timeline(dataset)
