import concurrent.futures
from ai import client
import pandas as pd
from functions.utils import *
import unicodedata
import configs
import json
import threading
import openai
from time import sleep


def get_comment_scale(comment: str, n: int) -> None:
    """Função específica para realizar a ponte entre o CHATGPT e a conversão do comentário para uma escala de 0 a 10. Ela pega o comentário, manda pro GPT, retorna o valor e esse valor é adicionado na lista passada
    :param comment: Comentário pedido
    :param comments_on_scale_column: Lista com todas as notas
    """
    try:
        print(f"{n} calculada")
        response: str = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"See the comments and resume them in an scale from 0 to 10, if the comment doesn't make sense, say it's 0, i want you to return only one number, with no text:\n \'{comment}\'"
                },
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        return response.choices[0].message.content  # Adicionando comentários no json
    except openai.OpenAIError as e:
        print("\n\n\n\n\n\n" + "="*20)
        print("DEU BOSTA AQUI Ó")

        sleep(10)
        return get_comment_scale(comment, n)


# Função que transforma a avaliação do comentário em uma escala numérica
@see_execution_time
def analyse_comments(dataframe: pd.DataFrame) -> None:#
    """Função que analisa os comentários
    :param dataframe: Dataframe do pandas que será alterado
    """

    comments_on_scale: list[dict] = []  #  A Lista que vai ter as notas em dicionários
    
    # Mando a coluna com os comentários para a função que vai retornar uma lista separada para que
    # Não envie tantos comentários ao mesmo tempo
    # comments_to_send_to_gpt = minimise_tokens_per_message(dataframe['COMENTARIO'])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_executing: list[concurrent.futures.Future] = []  # Threads executadas

        for i, comment in enumerate(dataframe['COMENTARIO']):  # Pra cada lista de dicionários dentro da lista principal
            threads_executing.append(executor.submit(get_comment_scale, comment, i))

        concurrent.futures.wait(threads_executing)

        for thread in threads_executing:
            # comments_on_scale.append(thread.result())
            comments_on_scale.append(thread.result())
    
    # sorted_comments = sorted(comments_on_scale_to_convert, key=lambda d: d["id"])

    for rate in comments_on_scale:
        print(rate)
    
    dataframe['COMENTARIO_COMO_NOTA'] = comments_on_scale
