import networkx as nx
import matplotlib.pyplot as plt
import re
import RAM as rm
import argparse
file = "file.txt"
instructions = rm.makefile(file)

def saut_inconditionnel(chaine):
    """
    Extrait la valeur de 2 de la chaîne JUMP(2).

    Args:
        chaine (str): La chaîne d'entrée contenant l'instruction.

    Returns:
        str: La valeur de 2, ou None si le format de la chaîne est invalide.
    """
    pattern = r"\(([^)]+)\)"
    match = re.search(pattern, chaine)

    if match:
        return match.group(1)
    else:
        return None
    
def saut_conditionnel(chaine) :
    # Extraire les valeurs entre parenthèses
    pattern = r"\(([^)]+),([^)]+),([^)]+)\)"
    match = re.search(pattern, chaine)

    if match:
        # Récupérer les valeurs des groupes capturés
        r = match.groups()
        return list(r)
    else:
        print("Erreur: Format de chaîne non valide")


def create_instruction_dict(instructions_dico):
  """
  Crée un dictionnaire où chaque instruction est mappée à une liste des instructions suivantes.

  Args:
    instructions_dico: Un dictionnaire contenant les instructions et leurs opcodes.

  Returns:
    Un dictionnaire où chaque instruction est mappée à une liste des instructions suivantes.
  """

  new_dict = {}
  for opcode, instruction in instructions_dico.items():
    next_instruction = instructions_dico.get(opcode + 1, None)
    if instruction.startswith("JE") or instruction.startswith("JL"):
        # Instructions conditionnelles
        s = saut_conditionnel(instruction)
        yug = instructions_dico.get(opcode + int(s[2]), None)
        if yug is None :
           next_instructions = []
        else:
            next_instructions = [next_instruction, yug]
    elif instruction.startswith("JUMP"):
        s = saut_inconditionnel(instruction)
        sol = instructions_dico.get(opcode + int(s), None)
        if sol is None :
           next_instructions = []
        else:
            next_instructions = [sol]
    else:
        # Instructions arithmétiques et JUMP
        if next_instruction is None :
            next_instructions = []
        else :
           next_instructions = [next_instruction]

    new_dict[instruction] = next_instructions

  return new_dict


def creer_graphe_instructions(dictionnaire_instructions):
  """
  Crée un graphe dirigé à partir d'un dictionnaire d'instructions.

  Args:
    dictionnaire_instructions: Un dictionnaire où la clé est une instruction sous forme de chaîne et la valeur est une liste de deux instructions: l'instruction suivante et l'instruction de saut conditionnel (si elle existe).

  Returns:
    Un graphe NetworkX dirigé représentant les dépendances entre les instructions.
  """

  graphe = nx.DiGraph()

  # Ajout des sommets (instructions)
  for instruction in dictionnaire_instructions.keys():
    if instruction != None :
        graphe.add_node(instruction)

  # Ajout des arêtes (liens entre les instructions)
  for instruction, instructions_suivantes in dictionnaire_instructions.items():
    for instruction_suivante in instructions_suivantes:
      if instruction_suivante != None :
        graphe.add_edge(instruction, instruction_suivante)

  return graphe


def supprimer_noeuds_inatteignables(graphe):
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
  first_key = next(iter(graphe))
  dfs(first_key)

  # Supprime les nœuds non visités du dictionnaire du graphe
  graphe_filtre = {noeud: adjacents for noeud, adjacents in graphe.items() if noeud in visites}

  return graphe_filtre

graphe = create_instruction_dict(instructions)
graphe_filtre = supprimer_noeuds_inatteignables(graphe)
print("graphe connexe", graphe_filtre)  # {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B'], 'E': ['C']}
r = rm.Ram(instructions)

def suppression_instructs(d):
  """
  Converti un dictionnaire avec des clés en chaînes en un dictionnaire avec des clés numériques.

  Args:
    d (dict): Le dictionnaire à convertir.

  Returns:
    dict: Le dictionnaire converti avec des clés numériques.
  """
  new_dict = {}
  for i, (key, value) in enumerate(d.items()):
    new_dict[i + 1] = key
  return new_dict
print("in",r.get_instructs())
r.set_instructs(suppression_instructs(graphe_filtre))
plt.figure()
ax = plt.subplot()
# Visualiser le graphe (optionnel)
dict2 = create_instruction_dict(r.get_instructs())
print(dict2)
res = creer_graphe_instructions(dict2)
nx.draw(res, with_labels=True)
r.set_instructs(suppression_instructs(graphe_filtre))
print("heheheh",r.get_instructs())
print("bb",graphe)
plt.show()