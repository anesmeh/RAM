import RAM as rm
import tkinter as tk
import os

''' Passage du Makefile au fichier sous format Python '''
def readfile(argument):
    try :
        instructs = rm.makefile(argument+".txt") 
        affiche_instruction(instructs)
    except FileNotFoundError:
        print(f"Fichier '{argument}' introuvable.")
        return {}

def update_ram_display(ram):
    instructions_text.delete(1.0, tk.END)
    for index, (instruction, args) in ram.instructs.items():
        instructions_text.insert(tk.END, f"{index}: {instruction}({', '.join(str(arg) for arg in args)})\n")

    registers_text.delete(1.0, tk.END)
    for i, value in enumerate(ram.registers):
        registers_text.insert(tk.END, f"r{i}: {value}\n")

    input_text.delete(1.0, tk.END)
    input_text.insert(tk.END, ", ".join(str(value) for value in ram.input))

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, ", ".join(str(value) for value in ram.output))

def affiche_instruction (dict):
    for key, val in dict.items() :
        if key != 0 :
            instructions_text.insert(float(key)+1,val+"\n")
        else:
            liste = val.split(",")
            for i in range(len(liste)) :
                print(liste)
                input_text.insert(float(i)+1,"i"+str(i)+" : "+str(liste[i]) +"\n")
    r = rm.Ram(dict)
    print("raaa", r)
    registers_text.insert(float('0'),r.get_register())

def execute_instruction(ram):
    try:
        instruction, args = ram.instructions[ram.pos]
        getattr(ram, instruction)(*args)
        ram.pos += 1
        update_ram_display(ram)
        status_text.config(text=f"Instruction '{instruction}({', '.join(str(arg) for arg in args)})' exécutée avec succès.")
    except IndexError as e:
        status_text.config(text=f"Erreur : {e}")
    except TypeError as e:
        status_text.config(text=f"Erreur : {e}")
    except Exception as e:
        status_text.config(text=f"Erreur inattendue : {e}")

def execute_step_by_step(ram):
    execute_instruction(ram)
    if ram.pos <= len(ram.instructions):
        step_by_step_button.config(text="Continuer")
    else:
        step_by_step_button.config(text="Terminé")

def reset_ram(ram):
    ram.reset()
    update_ram_display(ram)
    status_text.config(text="RAM réinitialisée.")

# Initialisation de l'interface

window = tk.Tk()
window.title("Machine RAM")

# Chargement du fichier texte

file_entry = tk.Entry(window)
file_entry.pack(pady=10)

load_button = tk.Button(window, text="Charger", command=lambda: readfile(file_entry.get()))
load_button.pack(pady=5)

# Affichage des instructions

instructions_frame = tk.Frame(window)
instructions_frame.pack(pady=10)

instructions_label = tk.Label(instructions_frame, text="Instructions:")
instructions_label.pack()


instructions_text = tk.Text(instructions_frame, width=50, height=10, wrap=tk.WORD)
instructions_text.pack()

# Affichage des registres, entrée et sortie

ram_state_frame = tk.Frame(window)
ram_state_frame.pack(pady=10)

registers_label = tk.Label(ram_state_frame, text="Registres:")
registers_label.grid(row=0, column=0)

registers_text = tk.Text(ram_state_frame, width=20, height=5, wrap=tk.WORD)
registers_text.grid(row=1, column=0)

input_label = tk.Label(ram_state_frame, text="Entrée:")
input_label.grid(row=0, column=1)

input_text = tk.Text(ram_state_frame, width=20, height=5, wrap=tk.WORD)
input_text.grid(row=1, column=1)

output_label = tk.Label(ram_state_frame, text="Sortie:")
output_label.grid(row=0, column=2)

output_text = tk.Text(ram_state_frame, width=20, height=5, wrap=tk.WORD)
output_text.grid(row=1, column=2)

# Champ de saisie pour modifier les registres

register_entry_label = tk.Label(window, text="Modifier registre:")
register_entry_label.pack(pady=10)

register_entry = tk.Entry(window)
register_entry.pack()

register_value_entry = tk.Entry(window)
register_value_entry.pack()

modify_register_button = tk.Button(window, text="Modifier", command=lambda: modify_register(ram, register_entry.get(), register_value_entry.get()))
modify_register_button.pack(pady=5)

# Boutons d'exécution

control_frame = tk.Frame(window)
control_frame.pack(pady=10)

execute_button = tk.Button(control_frame, text="Exécuter", command=execute_instruction)
execute_button.pack(side=tk.LEFT, padx=10)

step_by_step_button = tk.Button(control_frame, text="Pas à pas", command=execute_step_by_step)
step_by_step_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(control_frame, text="Réinitialiser", command=lambda: reset_ram(ram))
reset_button.pack(side=tk.LEFT, padx=10)

# Zone de texte pour les messages d'état

status_text = tk.Label(window, text="")
status_text.pack(pady=10)


window.mainloop()