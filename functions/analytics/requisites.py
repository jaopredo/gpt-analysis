import pandas as pd
import concurrent.futures
from ai import client
import openai


def make_requisites_analysis(requisites, recommended):
    try:
        requisites_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please, see this PC components and estipulate how much a computer with this specifications would cost. Return a small text about the components prices too: {requisites}"
                },
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        recommended_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please, see this PC components and estipulate how much a computer with this specifications would cost. Return a small text about the components prices too: {recommended}"
                }
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        print("Informações de requisitos CARREGADA")

        return (
            requisites_response.choices[0].message.content,
            recommended_response.choices[0].message.content
        )

    except openai.OpenAIError as e:  # Se o chatgpt retornar um erro de tokens
        print('\n\n =================================')
        print(f"Erro calculando as informações de especificação, tentando calcular novamente!")
        print(' ================================= \n\n')
        print(e)
        sleep(5)  # Espero 10 segundos
        return make_requisites_analysis(requisites, recommended)  # Tento executar novamente a função


def generate_requisites_analysis(games_df: pd.DataFrame):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_executing = []

        for game in games_df.iterrows():
            threads_executing.append(
                executor.submit(
                    make_requisites_analysis,
                    game[1]["MINIMUM_REQUISITES"],
                    game[1]["RECOMMENDED_SETUP"]
                )
            )
        
        concurrent.futures.wait(threads_executing)

        list_to_put_in_column = []

        for pendding_thread in threads_executing:
            list_to_put_in_column.append(pendding_thread.result())
    
    for linha in list_to_put_in_column:
        print(linha)

