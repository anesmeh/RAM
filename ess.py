import networkx as nx
import matplotlib.pyplot as plt


def next_instruction(instructions_dico):
  """
  Fonction qui prend en argument un dictionnaire d'instructions et retourne un nouveau dictionnaire 
  contenant les instructions suivantes pour chaque instruction et condition.

  Args:
    instructions_dico: Un dictionnaire d'instructions où la clé est le numéro de la ligne et la valeur est la chaîne d'instruction.

  Returns:
    Un dictionnaire où la clé est une instruction et la valeur est une liste contenant les instructions suivantes possibles.
  """

  next_instructions_dico = {}
  for ligne, instruction in instructions_dico.items():
    # Instruction suivante sans condition
    if not instruction.startswith("JE") and not instruction.startswith("JL"):
      next_instruction = instructions_dico.get(ligne + 1)
      if next_instruction:
        next_instructions_dico[(instruction.replace(",",""))] = [next_instruction.replace(",", "")]
    # Instruction suivante pour JE (condition vraie et fausse)
    elif instruction.startswith("JE"):
      try:
        condition_vrai, condition_faux = instruction[3:].split(",")
      except ValueError:
        condition_vrai = instruction[3:]
        condition_faux = None
      # Extraire le numéro de ligne de la condition_vrai (si possible)
      try:
        condition_vrai = int(condition_vrai.split(",")[0])
      except ValueError:
        pass  # Ignore si conversion échoue (registre)
      next_instruction_vrai = instructions_dico.get(condition_vrai)
      # Gérer le cas où condition_faux est None
      if condition_faux is not None:
        try:
          next_instruction_faux = instructions_dico.get(int(condition_faux))
        except ValueError:
          pass  # Ignore si conversion échoue (registre)
      else:
        next_instruction_faux = None  # Laisser next_instruction_faux à None
      if next_instruction_vrai and next_instruction_faux:
        next_instructions_dico[(instruction.replace(",",""))] = [next_instruction_vrai.replace(",",""), next_instruction_faux.replace(",", "")]
    # Instruction suivante pour JL (condition vraie uniquement)
    elif instruction.startswith("JL"):
      condition_vrai = instruction[3:].split(",")[0]
      try:
        next_instruction_vrai = instructions_dico.get(int(condition_vrai))
      except ValueError:
        pass  # Ignore si conversion échoue (registre)
      if next_instruction_vrai:
        next_instructions_dico[(instruction.replace(",",""))] = [next_instruction_vrai.replace(",", "")]
  return next_instructions_dico

# Exemple d'utilisation
instructions_dico = {
  0: "LOAD(i0,r0)",
  1: "LOAD(i0,r1)",
  2: "LOAD(i1,r2)",
  3: "JE(r2,1,7)",
  4: "JE(r2,0,5)",
  5: "MULT(r0,r1,r1)",
  6: "SUB(r2,1,r2)",
  7: "JL(r2,5,-2)",
  8: "JUMP(2)",
  9: "LOAD(1,r1)",
  10: "LOAD(r1,o0)",
}


dictionnaire_instructions = {('LOAD(i0,r0)'): ['LOAD(i0,r1)'], ('LOAD(i0,r1)'): ['LOAD(i1,r2)'], ('LOAD(i1,r2)'): ['JE(r2,1,7)'], ('JE(r2,1,7)'): ['JE(r2,0,5)','LOAD(r1,o0)'], ('JE(r2,0,5)'): ['MULT(r0,r1,r1)','LOAD(1,r1)'], ('MULT(r0,r1,r1)'): ['SUB(r2,1,r2)'], ('SUB(r2,1,r2)'): ['JL(r2,5,-2)'], ('JL(r2,5,-2)'): ['JUMP(2)'], ('JUMP(2)'): ['LOAD(1,r1)'], ('LOAD(1,r1)'): ['LOAD(r1,o0)'], ('LOAD(r1,o0)'): []}
print(dictionnaire_instructions)
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
    graphe.add_node(instruction)

  # Ajout des arêtes (liens entre les instructions)
  for instruction, instructions_suivantes in dictionnaire_instructions.items():
    for instruction_suivante in instructions_suivantes:
      graphe.add_edge(instruction, instruction_suivante)

  return graphe


graphe_instructions = creer_graphe_instructions(dictionnaire_instructions)
plt.figure()
ax = plt.subplot()
# Visualiser le graphe (optionnel)
nx.draw(graphe_instructions, with_labels=True)
plt.show()