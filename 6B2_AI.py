import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# ===============================
# 1. CRIAR GRAFO
# ===============================

G = nx.DiGraph()

for row in in_data:
    origem = str(row["origem"])
    destino = str(row["destino"])
    peso = float(row["peso"])
    usar_para = str(row["usar_para"])

    if usar_para != "mst":
        G.add_edge(origem, destino, weight=peso)

nodes = list(G.nodes())
n = len(nodes)

# ===============================
# 2. MATRIZ INICIAL
# ===============================

D = nx.to_numpy_array(
    G,
    nodelist=nodes,
    weight="weight",
    nonedge=np.inf
)

np.fill_diagonal(D, 0)

print("Nós:", nodes)

# ===============================
# 3. FUNÇÃO PARA DESENHAR MATRIZ
# ===============================

def show_matrix(matrix, title):
    display_matrix = matrix.copy()

    # Substituir infinito por valor grande só para desenhar
    temp = display_matrix.copy()
    temp[np.isinf(temp)] = np.nan

    plt.figure(figsize=(10, 8))
    plt.imshow(temp, aspect="auto")
    plt.colorbar(label="Distância mínima")

    plt.xticks(range(n), nodes, rotation=90)
    plt.yticks(range(n), nodes)

    for i in range(n):
        for j in range(n):
            value = matrix[i][j]

            if np.isinf(value):
                text = "∞"
            else:
                text = str(int(value))

            plt.text(j, i, text, ha="center", va="center")

    plt.title(title)
    plt.tight_layout()
    plt.show()

# ===============================
# 4. MOSTRAR MATRIZ INICIAL
# ===============================

show_matrix(D, "Matriz inicial D0 — Floyd-Warshall")

# ===============================
# 5. ANIMAÇÃO DO FLOYD-WARSHALL
# ===============================

for k in range(n):
    intermediario = nodes[k]

    houve_melhoria = False

    print("\n====================================")
    print("Iteração k =", k)
    print("Nó intermédio:", intermediario)
    print("====================================")

    for i in range(n):
        for j in range(n):

            if D[i][k] + D[k][j] < D[i][j]:

                print(
                    "Melhorou:",
                    nodes[i], "->", nodes[j],
                    "| antes =", D[i][j],
                    "| novo =", D[i][k] + D[k][j],
                    "| via", intermediario
                )

                D[i][j] = D[i][k] + D[k][j]
                houve_melhoria = True

    if houve_melhoria:
        show_matrix(
            D,
            "Floyd-Warshall | usando " + intermediario + " como nó intermédio"
        )
        time.sleep(1)
    else:
        print("Não houve melhorias nesta iteração.")

# ===============================
# 6. MATRIZ FINAL
# ===============================

show_matrix(D, "Matriz final — menores distâncias entre todos os pares")

df_final = pd.DataFrame(D, index=nodes, columns=nodes)

print("\n====================================")
print("MATRIZ FINAL")
print("====================================")
print(df_final)
