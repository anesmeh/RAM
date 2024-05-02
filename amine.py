def creer_dictionnaire_instructions(dict_instructions):
  """
  Crée un nouveau dictionnaire où chaque instruction du dictionnaire d'instructions d'origine est une clé avec une liste contenant les instructions suivantes.

  Args:
    dict_instructions: Un dictionnaire Python contenant les instructions du programme.

  Returns:
    Un nouveau dictionnaire où chaque instruction est une clé avec une liste contenant les instructions suivantes.
  """
  nouveau_dictionnaire = {}
  instruction_suivante = None
  for instruction in dict_instructions.values():
    if instruction_suivante is not None:
      nouveau_dictionnaire[instruction_suivante].append(instruction)
    instruction_suivante = instruction
  return nouveau_dictionnaire

# Exemple d'utilisation
dict_instructions = {
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

nouveau_dictionnaire = creer_dictionnaire_instructions(dict_instructions)
print(nouveau_dictionnaire)
