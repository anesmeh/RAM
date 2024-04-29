import argparse

class Ram:
    def __init__(self, instructs):
        self.pos = 1
        self.input = [len(instructs[0].split(','))]
        input_list = []
        for element in instructs[0].split(','):
            input_list.append(int(element))
        self.input += input_list
        self.register = []
        self.output = []
        # Attention le dictionnaire commence par la clé 1
        del instructs[0]
        self.instructs = instructs

    def __str__(self):
        res = "*********************************" + "\n"
        res += "Position du pointeur : " + str(self.pos+1) + "\n"
        res += "Input : " + str(self.input) + "\n"
        res += "Registre : " + str(self.register) + "\n"
        res += "Output : " + str(self.output) + "\n"
        # for key, value in self.instructs.items():
        #     res +=  "Instruction " + str(key) + " : " + value + "\n"
        res += "*********************************"
        return res

    def recuperer_element(self, element):
        if type(element) == int:
            return element
        if type(element) == str and element.startswith("r"):
            try:
                position = int(element[1:])
                return self.register[position]
            except (ValueError, IndexError):
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        if type(element) == str and element.startswith("i"):
            try:
                position = int(element[1:])
                return self.input[position]
            except (ValueError, IndexError):
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        if type(element) == str and element.startswith("o"):
            try:
                position = int(element[1:])
                return self.output[position]
            except (ValueError, IndexError):
                raise ValueError(f"Impossible de récupérer l'élément à la position {position} de la liste.")
        else:
            raise TypeError(f"Le type de l'élément {element} n'est pas pris en charge.")

    def lecture(self, instruction):
        commands = ("ADD", "SUB", "DIV", "MULT", "JUMP", "JE", "JL", "LOAD")
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

    def step(self):
        self.lecture(self.instructs[self.pos])

    def LOAD(self, arg):
        if type(arg[1]) == str and arg[1][0] == "i" :
            raise TypeError ("vous ne pouvez pas stocker dans le input")
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if len(arg) != 2:
            raise IndexError(f"L'instruction LOAD attend exactement deux arguments, mais {len(arg)} ont été fournis.")
        value = self.recuperer_element(arg[0])
        pos = int(arg[1][1:])
        if arg[1][0] == "r" :
            if pos >= len(self.register):
                for _ in range(len(self.register), pos+1):
                    self.register.append(0)
            self.register[pos] = value 
        elif arg[1][0] == "o" :
            if pos >= len(self.output):
                for _ in range(len(self.output), pos+1):
                    self.output.append(0)
            self.output[pos] = value
        else:
            raise IndexError("Erreur dans l'instruction LOAD")
        self.pos += 1

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
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if type(arg[1]) == str and arg[1][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        # pos : Position souhaitée/voulu
        pos = int(arg[2][1:])
        if pos >= len(self.register):
            for _ in range(len(self.register), pos+1):
                self.register.append(0)
        self.register[pos] = self.recuperer_element(arg[0]) + self.recuperer_element(arg[1])
        print(self.instructs[self.pos])
        print("HERE !" , self.register[pos], arg[0], arg[1])
        print(self.recuperer_element(arg[0]))
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
        if type(arg[0]) == str and arg[0][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        if type(arg[1]) == str and arg[1][0] == "o" :
            raise TypeError ("vous ne pouvez pas recuperer de l'output")
        pos = int(arg[2][1:])
        if pos >= len(self.register):
            for _ in range(len(self.register), pos+1):
                self.register.append(0)
        self.register[pos] = self.recuperer_element(arg[0]) - self.recuperer_element(arg[1])
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
        pos = int(arg[2][1:])
        if pos >= len(self.register):
            for _ in range(len(self.register), pos+1):
                self.register.append(0)
        self.register[pos] = self.recuperer_element(arg[0]) * self.recuperer_element(arg[1])
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
        pos = int(arg[2][1:])
        if pos >= len(self.register):
            for _ in range(len(self.register), pos+1):
                self.register.append(0)
        self.register[pos] = self.recuperer_element(arg[0]) // self.recuperer_element(arg[1])
        self.pos += 1

    def JUMP(self, arg):
        if (type(arg) is list) and (len(arg)==1):
            self.pos += arg[0]

    def JE(self, arg):
        if self.recuperer_element(arg[0]) == self.recuperer_element(arg[1]):
            self.pos += arg[2]
        else:
            self.pos += 1

    def JL(self, arg):
        if self.recuperer_element(arg[0]) < self.recuperer_element(arg[1]) :
            self.pos += arg[2]
        else:
            self.pos += 1
    
    def steps(self):
        print("*********************************")
        print("Execution des instructions de la Ram...")
        while self.pos <= len(self.instructs.keys()):
            print("Instruction en cours... " + self.instructs[self.pos])
            self.step()
            print(self)
            
def makefile(argument):
    instructs, index = {}, 0
    with open(argument, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
        for ligne in lignes:
            instructs[index] = ligne.replace("\n", "").replace(" ", "")
            index += 1
    return instructs

if __name__ == "__main__":
    # On recupere les arguments afin de lancer notre programme
    parser = argparse.ArgumentParser(description="Script running a RAM")
    parser.add_argument("File_RAM", help="An argument for a file that describes a RAM")
    args = parser.parse_args()
    instructions = makefile(args.File_RAM)

    # Lancement 
    r = Ram(instructions)
    print(r)
    r.steps()