import concurrent.futures
import time

# Função que demora para executar
def tarefa_demorada(n):
    print(f"Iniciando tarefa {n}")
    time.sleep(2)  # Simula uma tarefa que demora
    print(f"Terminando tarefa {n}")
    return f"Resultado da tarefa {n}"

# Lista de tarefas a serem executadas
tarefas = [1, 2, 3, 4, 5]
resultados = []

# Usando ProcessPoolExecutor para executar tarefas em paralelo
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Submete todas as tarefas ao executor
    futures = [executor.submit(tarefa_demorada, tarefa) for tarefa in tarefas]

    # Espera até que todas as tarefas terminem
    for future in concurrent.futures.as_completed(futures):
        resultados.append(future.result())

print(resultados)