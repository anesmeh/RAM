import networkx as nx
import matplotlib.pyplot as plt
import re
import RAM as rm
import argparse

def saut_inconditionnel(chaine):
    """
    Extrait la valeur de n de la chaîne JUMP(n).

    Args:
        chaine (str): La chaîne d'entrée contenant l'instruction.

    Returns:
        str: La valeur de n, ou None si le format de la chaîne est invalide.
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
    if opcode == 0 :
      pass
    else:
      next_instruction = instructions_dico.get(opcode + 1, None)
      if instruction.startswith("JE") or instruction.startswith("JL"):
          # Instructions conditionnelles
          saut = saut_conditionnel(instruction)
          next_instructions2 = instructions_dico.get(opcode + int(saut[2]), None)
          if next_instructions2 is None :
            next_instructions = []
          else:
              next_instructions = [next_instruction, next_instructions2]
      elif instruction.startswith("JUMP"):
          saut = saut_inconditionnel(instruction)
          next_instructions3 = instructions_dico.get(opcode + int(saut), None)
          if next_instructions3 is None :
            next_instructions = []
          else:
              next_instructions = [next_instructions3]
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

  def recursion(noeud):
    visites.add(noeud)
    for adjacent in graphe[noeud]:
      if adjacent not in visites:
        recursion(adjacent)
  first_key = next(iter(graphe))
  recursion(first_key)

  # Supprime les nœuds non visités du dictionnaire du graphe
  graphe_filtre = {noeud: adjacents for noeud, adjacents in graphe.items() if noeud in visites}

  return graphe_filtre

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

parser = argparse.ArgumentParser(description="Script running a RAM")
parser.add_argument("File_RAM", help="An argument for a file that describes a RAM")
args = parser.parse_args()
instructions = rm.makefile(args.File_RAM)
graphe = create_instruction_dict(instructions)
graphe_filtre = supprimer_noeuds_inatteignables(graphe)
# print("graphe connexe", graphe_filtre) donne {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B'], 'E': ['C']}
r = rm.Ram(instructions)
r.set_instructs(suppression_instructs(graphe_filtre))
plt.figure()
ax = plt.subplot()

# Visualiser le graphe
dict2 = create_instruction_dict(r.get_instructs())
res = creer_graphe_instructions(dict2)
nx.draw(res, with_labels=True)
r.set_instructs(suppression_instructs(graphe_filtre))
plt.show()