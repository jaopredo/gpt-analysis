import pandas as pd
import numpy as np

from functions.analytics import *


def generate_analytics(dataset):
    """
        Função que gera as análises necessárias para criação de gráficos específicos
    """
    analyse_comments(dataset)
