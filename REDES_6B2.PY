import networkx as nx
import numpy as np
import pandas as pd

# ===============================
# 1. CRIAR GRAFO DIRIGIDO
# ===============================

G = nx.DiGraph()

for row in in_data:
    origem = str(row["origem"])
    destino = str(row["destino"])
    peso = float(row["peso"])
    usar_para = str(row["usar_para"])

    # Só usamos os dados de caminhos mínimos
    if usar_para != "mst":
        G.add_edge(origem, destino, weight=peso)

# ===============================
# 2. LISTA DE NÓS
# ===============================

nodes = list(G.nodes())

print("====================================")
print("NÓS DO GRAFO")
print("====================================")
print(nodes)

# ===============================
# 3. MATRIZ DE ADJACÊNCIA SIMPLES
# ===============================

adj_matrix = nx.to_numpy_array(
    G,
    nodelist=nodes,
    weight="weight",
    nonedge=0
)

df_adj = pd.DataFrame(
    adj_matrix,
    index=nodes,
    columns=nodes
)

print("\n====================================")
print("MATRIZ DE ADJACÊNCIA")
print("0 significa: sem ligação")
print("====================================")
print(df_adj)

# ===============================
# 4. MATRIZ PARA FLOYD-WARSHALL
# ===============================
# Regra:
# diagonal = 0
# ligação existente = peso
# sem ligação = infinito

fw_matrix = nx.to_numpy_array(
    G,
    nodelist=nodes,
    weight="weight",
    nonedge=np.inf
)

np.fill_diagonal(fw_matrix, 0)

df_fw_initial = pd.DataFrame(
    fw_matrix,
    index=nodes,
    columns=nodes
)

print("\n====================================")
print("MATRIZ INICIAL D0 PARA FLOYD-WARSHALL")
print("inf significa: não existe ligação direta")
print("====================================")
print(df_fw_initial)

# ===============================
# 5. APLICAR FLOYD-WARSHALL MANUALMENTE
# ===============================

D = fw_matrix.copy()
n = len(nodes)

print("\n====================================")
print("ITERAÇÕES DO FLOYD-WARSHALL")
print("====================================")

for k in range(n):
    intermediario = nodes[k]

    print("\nA considerar o nó intermédio:", intermediario)

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

# ===============================
# 6. MATRIZ FINAL
# ===============================

df_fw_final = pd.DataFrame(
    D,
    index=nodes,
    columns=nodes
)

print("\n====================================")
print("MATRIZ FINAL DO FLOYD-WARSHALL")
print("Menor distância entre todos os pares")
print("====================================")
print(df_fw_final)

# ===============================
# 7. COMPARAÇÃO DE ALGUNS CAMINHOS
# ===============================

print("\n====================================")
print("EXEMPLOS DE RESULTADOS")
print("====================================")

pares = [
    ("Lisboa", "Porto"),
    ("Lisboa", "Faro"),
    ("Lisboa", "Braganca"),
    ("Coimbra", "Porto"),
    ("Faro", "Evora")
]

for origem, destino in pares:
    if origem in nodes and destino in nodes:
        i = nodes.index(origem)
        j = nodes.index(destino)

        print(
            origem, "->", destino,
            "| distância mínima =", D[i][j]
        )

# ===============================
# 8. DETETAR PESOS NEGATIVOS
# ===============================

print("\n====================================")
print("PESOS NEGATIVOS")
print("====================================")

tem_negativos = False

for u, v, data in G.edges(data=True):
    if data["weight"] < 0:
        tem_negativos = True
        print(u, "->", v, "| peso =", data["weight"])

if tem_negativos:
    print("\nConclusão: existem pesos negativos.")
    print("Para origem única, deve usar Bellman-Ford.")
else:
    print("\nConclusão: não existem pesos negativos.")
    print("Para origem única, pode usar Dijkstra.")

print("\nPara todos os pares, usa-se Floyd-Warshall.")
