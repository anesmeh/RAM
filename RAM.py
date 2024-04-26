# a faire : si il n' a pas de input mettre erreur 

import argparse

''' Passage du Makefile au fichier sous format Python '''
def makefile(argument):
    instructs, index = {}, 0
    with open(argument, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
        for ligne in lignes:
            instructs[index] = ligne.replace("\n", "").replace(" ", "")
            index += 1
    print ("instruct :", instructs)
    return instructs

def positionne_element(a, b, c):
  """
  Fonction qui insère l'élément c à la position a de la liste b.

  Si la position a est supérieure à la longueur de la liste b, la fonction ajoute des 0 à la liste b jusqu'à ce que la position a soit accessible, puis insère l'élément c à cette position.

  Args:
      a (int): La position souhaitée pour l'élément c.
      b (list): La liste dans laquelle l'élément c doit être inséré.
      c (int): L'élément à insérer dans la liste b.

  Returns:
      list: La liste b modifiée avec l'élément c inséré à la position a.
  """
  if a >= len(b):
    # Si la position est supérieure à la longueur de la liste, 
    # on ajoute des 0 jusqu'à ce qu'elle soit accessible
    for i in range(len(b), a + 1):
      b.append(0)
  b[a] = c
  return b

"""
Machine RAM simple avec instructions ADD, SUB, DIV, MULT, JUMP, JE, JL.

Lit les instructions d'un fichier et les exécute.
"""

class Ram:
    ''' Construit une Ram.
    Elle sera composée d'une bande input que l'utilisateur rentre ainsi qu'une suite d'instructions sous forme de dictionnaire.
    '''
    def __init__(self, instructs):
        ''' Creation de notre structure Ram '''
        self.pos = 1
        self.input = [len(instructs[0].split(','))]
        input_list = []
        # Passage d'une liste de chaine de characteres à une liste d'entiers relatifs
        for element in instructs[0].split(','):
            input_list.append(int(element))
        self.input += input_list
        self.register = []
        self.output = []
        # Attention le dictionnaire commence par la clé 1
        del instructs[0]
        self.instructs = instructs
        print("000000000000000000000000", self.instructs)

    def get_register(self):
        return self.register
    
    def recuperer_element(self,element, registre, input, output):
        """
        Fonction qui récupère un élément et retourne sa valeur en fonction de son type.

        Si l'élément est un entier, la fonction retourne ,l'entier lui-même.
        Si l'élément est une chaîne de caractères et commence par "r", la fonction retourne l'élément à la position spécifiée par le nombre qui suit le "r".
        Par exemple, si l'élément est "r2", la fonction retourne le deuxième élément de la liste fournie comme argument.

        Args:
            element (int ou str): L'élément à récupérer.

        Returns:
            int ou str: La valeur de l'élément en fonction de son type.
        """
        if type(element) == int:
        # Si l'élément est un entier, on le retourne directement
            return element
        elif type(element) == str and element.startswith("r"):
        # Si l'élément est une chaîne de caractères et commence par "r",
        # on récupère l'élément à la position spécifiée par le nombre qui suit le "r"
            try:
                position = int(element[1:])
                return registre[position]
            except (ValueError, IndexError):
                # Si le nombre après le "r" n'est pas un entier ou si la position est hors limites,
                # on retourne une erreur
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        elif type(element) == str and element.startswith("i"):
        # Si l'élément est une chaîne de caractères et commence par "i",
        # on récupère l'élément à la position spécifiée par le nombre qui suit le "i"
            try:
                position = int(element[1:]) +1
                return input[position]
            except (ValueError, IndexError):
                # Si le nombre après le "i" n'est pas un entier ou si la position est hors limites,
                # on retourne une erreur
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        elif type(element) == str and element.startswith("o"):
        # Si l'élément est une chaîne de caractères et commence par "i",
        # on récupère l'élément à la position spécifiée par le nombre qui suit le "i"
            try:
                position = int(element[1:]) +1
                return output[position]
            except (ValueError, IndexError):
                # Si le nombre après le "i" n'est pas un entier ou si la position est hors limites,
                # on retourne une erreur
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        elif element == "tr":
        # Si l'élément est"tr",
        # on récupère nombre d'entrees
            return len(input)
        else:
            # Si l'élément n'est ni un entier ni une chaîne de caractères commençant par "r",
            # on retourne une erreur
            raise TypeError(f"Le type de l'élément {element} n'est pas pris en charge.")


    def __str__(self):
        """
        Affiche une représentation textuelle de la RAM.
        """
        res = "Position du pointeur : " + str(self.pos) + "\n"
        res += "Input : " + str(self.input) + "\n"
        res += "Registre : " + str(self.register) + "\n"
        res += "Output : " + str(self.output) + "\n"
        for key, value in self.instructs.items():
            if key != 0:
                res +=  "Instruction " + str(key) + " : " + value + "\n"
        res += "*********************************"
        return res

    def lecture(self, instruction):
        ''' Lecture d'une instruction dans le dictionnaire de la Ram puis execute la fonction avec le bon argument '''
        commands = ("ADD", "SUB", "DIV", "MULT", "JUMP", "JE", "JL", "LOAD", "NEXT")
        commands_starts, commands_end = tuple([element + "(" for element in commands]), ")"
        if instruction.startswith(commands_starts) and instruction.endswith(commands_end):
            buffer = instruction.split("(")[1].replace(")", "").split(',')
            registre = list()
            for element in buffer:
                try: 
                    int(element)
                except ValueError:
                    registre.append(element)
                    continue
                registre.append(int(element))
            func = getattr(Ram, instruction.split("(")[0])
            func(self, registre)


    def execute(self):
        """
        Exécute toutes les instructions de la RAM dans l'ordre.
        """
        print("Execution des instructions de la Ram...")
        while self.pos <= len(self.instructs.keys()):
            print("Instruction en cours... " + self.instructs[self.pos])
            self.lecture(self.instructs[self.pos])
        print("*********************************")
    
    def ADD(self, arg):

        if len(arg) < 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il manque un/des argument(s): " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,c,d) avec a,b,c et d des ints ou registres
        if len(arg) > 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il y a trop d'arguments: " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,4) avec a et b des ints ou registres
        if type(arg[2]) == int:
            raise TypeError(str(arg[0]) + " et " + str(arg[1]) + "sont stockées dans l'int " + str(arg[2]) + ".")

        if type(arg[2]) == str and arg[2][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")
        res = self.recuperer_element(arg[0], self.register,self.input) + self.recuperer_element(arg[1], self.register,self.input)
        positionne_element(int(arg[2][1:]),self.register, res)
        print(self.register)
        self.pos += 1


    def SUB(self, arg):

        # Exemple: ADD(a) avec a un int ou registre
        if len(arg) < 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il manque un/des argument(s): " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,c,d) avec a,b,c et d des ints ou registres
        if len(arg) > 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il y a trop d'arguments: " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,4) avec a et b des ints ou registres
        if type(arg[2]) == int:
            raise TypeError(str(arg[0]) + " et " + str(arg[1]) + "sont stockées dans l'int " + str(arg[2]) + ".")
        if type(arg[2]) == str and arg[2][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")

        res = self.recuperer_element(arg[0], self.register,self.input, self.output) - self.recuperer_element(arg[1], self.register,self.input, self.output)
        positionne_element(int(arg[2][1:]),self.register, res)
        print(self.register)
        self.pos += 1


    def MULT(self, arg):
  
        # Exemple: ADD(a) avec a un int ou registre
        if len(arg) < 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il manque un/des argument(s): " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,c,d) avec a,b,c et d des ints ou registres
        if len(arg) > 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il y a trop d'arguments: " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,4) avec a et b des ints ou registres
        if type(arg[2]) == int:
            raise TypeError(str(arg[0]) + " et " + str(arg[1]) + "sont stockées dans l'int " + str(arg[2]) + ".")
        if type(arg[2]) == str and arg[2][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if type(arg[1]) == str and arg[1][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        res = self.recuperer_element(arg[0], self.register,self.input, self.output) * self.recuperer_element(arg[1], self.register,self.input, self.output)
        positionne_element(int(arg[2][1:]),self.register, res)
        print(self.register)
        self.pos += 1

    def DIV(self, arg):

        # Exemple: ADD(a) avec a un int ou registre
        if len(arg) < 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il manque un/des argument(s): " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,c,d) avec a,b,c et d des ints ou registres
        if len(arg) > 3:
            raise IndexError("La ligne " + str(self.pos+1) + " contient une instruction invalide, il y a trop d'arguments: " + self.instructs[self.pos] + ".")
        # Exemple: ADD(a,b,4) avec a et b des ints ou registres
        if type(arg[2]) == int:
            raise TypeError(str(arg[0]) + " et " + str(arg[1]) + "sont stockées dans l'int " + str(arg[2]) + ".")
        if type(arg[2]) == str and arg[2][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if type(arg[1]) == str and arg[1][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")

        res = self.recuperer_element(arg[0], self.register,self.input, self.output) / self.recuperer_element(arg[1], self.register,self.input, self.output)
        positionne_element(int(arg[2][1:]),self.register, res)
        print(self.register)
        self.pos += 1

    def JUMP(self, arg):
        if (type(arg) is list) and (len(arg)==1):
            self.pos += arg[0]
            print("poiteur decale de ", arg[0])


    def JE(self, arg):
        equal = self.recuperer_element(arg[0], self.register,self.input, self.output) == self.recuperer_element(arg[1], self.register,self.input, self.output)
        if equal :
            self.pos += arg[2]
            print("poiteur decale de ", arg[2])
        else:
            self.pos += 1


    def JL(self, arg):
        less = self.recuperer_element(arg[0], self.register,self.input, self.output) < self.recuperer_element(arg[1], self.register,self.input, self.output)
        if less :
            self.pos += arg[2]
            print("poiteur decale de ", arg[2])
        else:
            self.pos += 1      

    def LOAD(self, arg):
        """
        Cette fonction permet de charger une valeur dans un registre.

        Args:
            arg (list): Une liste contenant deux éléments:
                - Le premier élément est la valeur à charger (un entier ou une référence à une valeur dans le registre ou l'entrée).
                - Le second élément est le numéro de registre où la valeur doit être stockée.
        """
        if type(arg[1]) == str and arg[1][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if len(arg) != 2:
            raise IndexError(f"L'instruction LOAD attend exactement deux arguments, mais {len(arg)} ont été fournis.")
        value = self.recuperer_element(arg[0], self.register, self.input, self.output)
        if arg[1][0] == "r" :
            positionne_element(int(arg[1][1:]), self.register, value)
        elif arg[1][0] == "o" :
            positionne_element(int(arg[1][1:]), self.output, value)
        self.pos += 1
        print(self.register)

    def NEXT(self, arg) :
        liste = arg[0][0]
        position = arg[0][1:]
        suivant = int(position) + 1
        res = liste + str(suivant)
        positionne_element(int(arg[1][1:]),self.register,res)
        self.pos += 1



if __name__ == "__main__":
    # On recupere les arguments afin de lancer notre programme
    parser = argparse.ArgumentParser(description="Script running a RAM")
    parser.add_argument("File_RAM", help="An argument for a file that describes a RAM")
    args = parser.parse_args()
    instructions = makefile(args.File_RAM)

    # Lancement 
    r = Ram(instructions)
    print(r)
    print('jj', r.input)
    r.execute()
    print('output :', r.output)
    