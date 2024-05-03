def supprimer_noeuds_inatteignables(graphe, noeud_debut):
  """
  Supprime les nœuds inatteignables d'un graphe en commençant par un nœud de départ.

  Args:
    graphe: Un dictionnaire représentant le graphe.
    noeud_debut: Le nœud de départ pour l'exploration.

  Returns:
    Un nouveau dictionnaire représentant le graphe après la suppression des nœuds inatteignables.
  """
  visites = set()  # Ensemble pour stocker les nœuds visités

  def dfs(noeud):
    visites.add(noeud)
    for adjacent in graphe[noeud]:
      if adjacent not in visites:
        dfs(adjacent)

  dfs(noeud_debut)

  # Supprime les nœuds non visités du dictionnaire du graphe
  graphe_filtre = {noeud: adjacents for noeud, adjacents in graphe.items() if noeud in visites}

  return graphe_filtre

graphe ={'2,6,7,3,4,0': ['LOAD(i0,r0)'], 'LOAD(i0,r0)': ['JUMP(5)'], 'JUMP(5)': [], 'LOAD(r1,o0)': ['LOAD(r1,r1)'], 'LOAD(r1,r1)': ['LOAD(i2,r2)'], 'LOAD(i2,r2)': []}
graphe_filtre = supprimer_noeuds_inatteignables(graphe, '2,6,7,3,4,0')
print(graphe_filtre)  # {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B'], 'E': ['C']}
