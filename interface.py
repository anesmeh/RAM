import RAM as rm
import tkinter as tk
import os

global_ram = 0

''' Passage du Makefile au fichier sous format Python '''
def readfile(argument):
    global global_ram
    status_text.config(text="")
    try:
        instructs = rm.makefile(f"prog\{argument}.txt")
        global_ram = rm.Ram(instructs)
        affiche_instruction(global_ram)
        load_button.config(text="Chargé", state="disabled")
    except FileNotFoundError:
        if argument == "" :
          print("Veuillez ajouter un code RAM")
        else :
          print(f"Fichier '{argument}' introuvable.")
        return {}


def affiche_instruction (ram):
    instructions_text.delete(1.0, tk.END)
    input_text.delete(1.0, tk.END)    
    for key, val in ram.get_instructs().items():
        instructions_text.insert(float(key)+1,val+"\n")
    for i in range(len(ram.get_input()[1:])) :
                    input_text.insert(float(i)+1,"i"+str(i)+" : "+str(ram.get_input()[1:][i]) +"\n")


def affiche_registres(ram):
    output_text.delete(1.0, tk.END)
    registers_text.delete(1.0, tk.END)
    for i in range(len(ram.get_output())) :
                    output_text.insert(float(i)+1,"o"+str(i)+" : "+str(ram.get_output()[i]) +"\n")

    for i in range(len(ram.get_register())) :
                    registers_text.insert(float(i)+1,"r"+str(i)+" : "+str(ram.get_register()[i]) +"\n")


def execute_instruction():
    global global_ram
    while global_ram.pos <= len(global_ram.instructs.keys()):
        global_ram.step()
    execute_button.config(text="Terminé", state="disabled")
    step_by_step_button.config(text="Terminé", state="disabled")
    affiche_registres(global_ram)

def execute_step_by_step():
    global global_ram
    if global_ram.pos <= len(global_ram.instructs.keys()):
        step_by_step_button.config(text="Continuer")
        global_ram.step()
    else:
        step_by_step_button.config(text="Terminé", state="disabled")
        execute_button.config(text="Terminé", state="disabled")
    affiche_registres(global_ram)

def reset_ram():
    global global_ram
    global_ram = 0
    instructions_text.delete(1.0, tk.END)
    registers_text.delete(1.0, tk.END)
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)
    step_by_step_button.config(text="Pas à pas", state="active")
    execute_button.config(text="Exécuter", state="active")
    status_text.config(text="RAM réinitialisée.")
    load_button.config(text="Charger", state="active")

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

# Boutons d'exécution

control_frame = tk.Frame(window)
control_frame.pack(pady=10)

execute_button = tk.Button(control_frame, text="Exécuter", command=execute_instruction)
execute_button.pack(side=tk.LEFT, padx=10)

step_by_step_button = tk.Button(control_frame, text="Pas à pas", command=execute_step_by_step)
step_by_step_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(control_frame, text="Réinitialiser", command=lambda: reset_ram())
reset_button.pack(side=tk.LEFT, padx=10)

# Zone de texte pour les messages d'état

status_text = tk.Label(window, text="")
status_text.pack(pady=10)


window.mainloop()