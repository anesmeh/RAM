Ce fichier README a été généré le 06/05/2024 par Amine Mohamed et Anes Mehimda.
Dernière mise-à-jour le : 06/05/2024.

# Titre et explication de la structure :

Le dossier contient __pycache__ le code précompilé des modules, prog contenant les fichiers textes de nos programmes RAM, et les fichiers .py contiennent la ram ainsi que l'affichage pour les dernieres questions du projet.

La structure de la Ram se fait dans RAM.py. Elle est basé sur le fonctionnement d'une ram vu en cours et TDs elle même basé sur de l'Assembleur.
L'interface s'affichera grace à interface.py, il nous demandera l'un des fichiers dans le dossier prog.

Le script graph.py permet de générer un graphe d'instructions à partir d'un fichier d'instructions. 
Le graphe représente les dépendances entre les instructions, avec chaque instruction comme nœud et les sauts conditionnels comme arêtes.
Le script utilise les bibliothèques networkx et matplotlib pour créer et visualiser le graphe.

# Installation :

Le projet a été fait sous Python 3.11 sous Windows.
On utilise les libraries installé via pip:
- *networkx* et *matplotlib.pyplot* pour l'affichage d'un graphe
- *re* pour la décomposition en expression reguliere de chaines de characteres
- *tkinter* pour l'affichage de notre Ram
- *os* pour diverses utilisations

# Usage : 

Le programme ne contient pas de Makefile. Les commandes dans le terminal sont :
```bash
    # Lancement de la machine Ram de a^b
    python3 RAM.py ..\PC_MEHIMDA_Anes_MOHAMED_Amine\prog\a^b.txt
    # Lancement de la machine Ram non fini de l'automate à pile dans le terminal
    python3 RAM.py ..\PC_MEHIMDA_Anes_MOHAMED_Amine\prog\nbr_transit.txt

    # L'interface
    python3 interface.py
    # L'affichage du graphe
    python3 graph.py ..\PC_MEHIMDA_Anes_MOHAMED_Amine\prog\nonconnexe.txt
```

## Informations additionnelles : 
- Création de LOAD nous permettant de traquer les erreurs lorsque l'on prend un element et que l'on le met dans un autre registre

## Code et valeurs manquantes / TODO :

- Avec comme entrée un tableau d’entier, écrire le tableau trié dans la sortie (par un tri à bulle)
- Ecrire une machine RAM qui étant donné un automate à pile A et un mot w en entrée écrit 0 en sortie si w est reconnu par A et 1 sinon
- Faire tourner cette machine RAM sur un automate à pile reconnaissant le langage {a^n b^n | n ∈ N}
- Application une optimisation d’élimination du code mort
- Question 10 bonus
- etc.
