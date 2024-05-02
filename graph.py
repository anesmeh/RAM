import networkx as nx
import matplotlib.pyplot as plt
import RAM as rm
import argparse
# Create a directed graph
G = nx.DiGraph()
def fonc(argument) :
    nod = []
    for key, e in argument.items() :
        nod.append(str(e))
    G.add_nodes_from(nod)
    print(nod)
# Add nodes
G.add_nodes_from(["A", "B", "C"])
 # Add directed edges with attributes (weight)
G.add_edge("A", "B", weight=2)
G.add_edge("B", "C", weight=3)
G.add_edge("C", "A", weight=1)  # Self loop allowed in DiGraph

# Print the number of nodes and edges
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Access edge weight
weight = G.get_edge_data("B", "C")["weight"]
print("Weight of edge (B, C):", weight)

# Find shortest path from A to C
shortest_path = nx.shortest_path(G, source="A", target="C")
print("Shortest path from A to C:", shortest_path)

# Création d'une figure et d'un axe
plt.figure()
ax = plt.subplot()

# Dessiner le graphe sur l'axe


# Ajuster la mise en page, les étiquettes et le style
# ... (Options de personnalisation)

# Afficher le graphe


if __name__ == "__main__" :
    # On recupere les arguments afin de lancer notre programme
    parser = argparse.ArgumentParser(description="Script running a RAM")
    parser.add_argument("File_RAM", help="An argument for a file that describes a RAM")
    args = parser.parse_args()
    instructions = rm.makefile(args.File_RAM)
    fonc(instructions)
    nx.draw_networkx(G, pos=nx.spring_layout(G), ax=ax)
    plt.show()