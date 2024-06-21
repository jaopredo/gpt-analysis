from time import time
import tiktoken

def see_execution_time(func, *args):
    def slave(*args, **kwargs):
        initial_time = time()
        func(*args, *kwargs)
        end_time = time()
        
        print(f"A função demorou {end_time - initial_time} segundos")

    return slave
