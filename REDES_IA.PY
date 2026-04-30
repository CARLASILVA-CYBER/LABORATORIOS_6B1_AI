import networkx as nx
import matplotlib.pyplot as plt

# ===============================
# 1. CRIAR GRAFOS
# ===============================

G_shortest = nx.DiGraph()   # Dijkstra, Bellman-Ford, Floyd-Warshall
G_mst = nx.Graph()          # Prim e Kruskal

for row in in_data:
    origem = str(row["origem"])
    destino = str(row["destino"])
    peso = float(row["peso"])
    usar_para = str(row["usar_para"])

    if usar_para == "mst":
        G_mst.add_edge(origem, destino, weight=peso)
    else:
        G_shortest.add_edge(origem, destino, weight=peso)

# ===============================
# 2. ANALISAR PESOS NEGATIVOS
# ===============================

has_negative = any(
    data["weight"] < 0
    for u, v, data in G_shortest.edges(data=True)
)

print("====================================")
print("ANÁLISE DO GRAFO")
print("====================================")
print("Nós no grafo de caminhos:", G_shortest.number_of_nodes())
print("Arestas no grafo de caminhos:", G_shortest.number_of_edges())
print("Existem pesos negativos?", has_negative)

if has_negative:
    algoritmo = "Bellman-Ford"
else:
    algoritmo = "Dijkstra"

print("Algoritmo recomendado:", algoritmo)

# ===============================
# 3. MOSTRAR ARESTAS NEGATIVAS
# ===============================

print("\n====================================")
print("ARESTAS COM PESO NEGATIVO")
print("====================================")

for u, v, data in G_shortest.edges(data=True):
    if data["weight"] < 0:
        print(u, "->", v, "| peso =", data["weight"])

# ===============================
# 4. CAMINHO MÍNIMO LISBOA -> FARO
# ===============================

origem = "Lisboa"
destino = "Faro"

print("\n====================================")
print("CAMINHO MÍNIMO:", origem, "->", destino)
print("====================================")

caminho_faro = None

try:
    if algoritmo == "Bellman-Ford":
        caminho_faro = nx.bellman_ford_path(
            G_shortest, origem, destino, weight="weight"
        )
        custo_faro = nx.bellman_ford_path_length(
            G_shortest, origem, destino, weight="weight"
        )
    else:
        caminho_faro = nx.dijkstra_path(
            G_shortest, origem, destino, weight="weight"
        )
        custo_faro = nx.dijkstra_path_length(
            G_shortest, origem, destino, weight="weight"
        )

    print("Caminho:", caminho_faro)
    print("Custo total:", custo_faro)

except Exception as e:
    print("Erro:", e)

# ===============================
# 5. CAMINHO MÍNIMO LISBOA -> BRAGANCA
# ===============================

origem = "Lisboa"
destino = "Braganca"

print("\n====================================")
print("CAMINHO MÍNIMO:", origem, "->", destino)
print("====================================")

caminho_braganca = None

try:
    if algoritmo == "Bellman-Ford":
        caminho_braganca = nx.bellman_ford_path(
            G_shortest, origem, destino, weight="weight"
        )
        custo_braganca = nx.bellman_ford_path_length(
            G_shortest, origem, destino, weight="weight"
        )
    else:
        caminho_braganca = nx.dijkstra_path(
            G_shortest, origem, destino, weight="weight"
        )
        custo_braganca = nx.dijkstra_path_length(
            G_shortest, origem, destino, weight="weight"
        )

    print("Caminho:", caminho_braganca)
    print("Custo total:", custo_braganca)

except Exception as e:
    print("Erro:", e)

# ===============================
# 6. FLOYD-WARSHALL
# ===============================

print("\n====================================")
print("FLOYD-WARSHALL")
print("Caminhos mínimos entre todos os pares")
print("====================================")

try:
    distancias = dict(nx.floyd_warshall(G_shortest, weight="weight"))

    print("Lisboa -> Porto:", distancias["Lisboa"]["Porto"])
    print("Lisboa -> Faro:", distancias["Lisboa"]["Faro"])
    print("Lisboa -> Braganca:", distancias["Lisboa"]["Braganca"])

except Exception as e:
    print("Erro no Floyd-Warshall:", e)

# ===============================
# 7. PRIM
# ===============================

print("\n====================================")
print("PRIM")
print("Árvore Geradora Mínima")
print("====================================")

try:
    mst_prim = nx.minimum_spanning_tree(
        G_mst, algorithm="prim", weight="weight"
    )

    custo_prim = 0

    for u, v, data in mst_prim.edges(data=True):
        print(u, "--", v, "| peso =", data["weight"])
        custo_prim += data["weight"]

    print("Custo total Prim:", custo_prim)

except Exception as e:
    print("Erro no Prim:", e)

# ===============================
# 8. KRUSKAL
# ===============================

print("\n====================================")
print("KRUSKAL")
print("Árvore Geradora Mínima")
print("====================================")

try:
    mst_kruskal = nx.minimum_spanning_tree(
        G_mst, algorithm="kruskal", weight="weight"
    )

    custo_kruskal = 0

    for u, v, data in mst_kruskal.edges(data=True):
        print(u, "--", v, "| peso =", data["weight"])
        custo_kruskal += data["weight"]

    print("Custo total Kruskal:", custo_kruskal)

except Exception as e:
    print("Erro no Kruskal:", e)

# ===============================
# 9. GRÁFICO 1 — GRAFO DE CAMINHOS
# ===============================

plt.figure(figsize=(14, 10))

pos = nx.spring_layout(G_shortest, seed=42)

nx.draw(
    G_shortest,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=1800,
    font_size=8,
    arrows=True
)

labels = nx.get_edge_attributes(G_shortest, "weight")

nx.draw_networkx_edge_labels(
    G_shortest,
    pos,
    edge_labels=labels,
    font_size=7
)

plt.title("Grafo dirigido — caminhos mínimos")
plt.show()

# ===============================
# 10. GRÁFICO 2 — CAMINHO LISBOA -> FARO
# ===============================

if caminho_faro is not None:

    plt.figure(figsize=(14, 10))

    nx.draw(
        G_shortest,
        pos,
        with_labels=True,
        node_color="lightgrey",
        node_size=1800,
        font_size=8,
        arrows=True
    )

    edges_path = list(zip(caminho_faro, caminho_faro[1:]))

    nx.draw_networkx_edges(
        G_shortest,
        pos,
        edgelist=edges_path,
        edge_color="red",
        width=3,
        arrows=True
    )

    nx.draw_networkx_edge_labels(
        G_shortest,
        pos,
        edge_labels=labels,
        font_size=7
    )

    plt.title("Caminho mínimo Lisboa -> Faro")
    plt.show()

# ===============================
# 11. GRÁFICO 3 — CAMINHO LISBOA -> BRAGANCA
# ===============================

if caminho_braganca is not None:

    plt.figure(figsize=(14, 10))

    nx.draw(
        G_shortest,
        pos,
        with_labels=True,
        node_color="lightgrey",
        node_size=1800,
        font_size=8,
        arrows=True
    )

    edges_path = list(zip(caminho_braganca, caminho_braganca[1:]))

    nx.draw_networkx_edges(
        G_shortest,
        pos,
        edgelist=edges_path,
        edge_color="red",
        width=3,
        arrows=True
    )

    nx.draw_networkx_edge_labels(
        G_shortest,
        pos,
        edge_labels=labels,
        font_size=7
    )

    plt.title("Caminho mínimo Lisboa -> Braganca")
    plt.show()

# ===============================
# 12. GRÁFICO 4 — PRIM
# ===============================

plt.figure(figsize=(14, 10))

pos_mst = nx.spring_layout(G_mst, seed=42)

nx.draw(
    G_mst,
    pos_mst,
    with_labels=True,
    node_color="lightgrey",
    node_size=1800,
    font_size=8
)

nx.draw_networkx_edges(
    mst_prim,
    pos_mst,
    edge_color="green",
    width=3
)

labels_mst = nx.get_edge_attributes(G_mst, "weight")

nx.draw_networkx_edge_labels(
    G_mst,
    pos_mst,
    edge_labels=labels_mst,
    font_size=7
)

plt.title("Árvore Geradora Mínima — Prim")
plt.show()

# ===============================
# 13. GRÁFICO 5 — KRUSKAL
# ===============================

plt.figure(figsize=(14, 10))

nx.draw(
    G_mst,
    pos_mst,
    with_labels=True,
    node_color="lightgrey",
    node_size=1800,
    font_size=8
)

nx.draw_networkx_edges(
    mst_kruskal,
    pos_mst,
    edge_color="orange",
    width=3
)

nx.draw_networkx_edge_labels(
    G_mst,
    pos_mst,
    edge_labels=labels_mst,
    font_size=7
)

plt.title("Árvore Geradora Mínima — Kruskal")
plt.show()

# ===============================
# 14. CONCLUSÃO
# ===============================

print("\n====================================")
print("CONCLUSÃO INTELIGENTE")
print("====================================")

print("Caminho mínimo com pesos negativos:", algoritmo)
print("Caminhos mínimos entre todos os pares: Floyd-Warshall")
print("Rede mínima para ligar todas as cidades: Prim ou Kruskal")
