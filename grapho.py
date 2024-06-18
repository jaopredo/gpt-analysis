import networkx as nx
import matplotlib.pyplot as plt
def grafico():    
    G = nx.Graph()
    ja_postos = set()
    
    with open('conexoes.csv', 'r',encoding= 'utf-8') as arquivo:
        for line in arquivo:
            try:
                a, b = line.strip().split('|||||')
                if (a, b) not in ja_postos and (b, a) not in ja_postos:
                    G.add_edge(a, b)
                    ja_postos.add((a, b))
            except:
                continue
    # Desenhar o grafo sem os nomes dos nós
    nx.draw(G)
    plt.savefig('grafo.png', dpi = 100)
    plt.show()
