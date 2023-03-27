from tkinter import *
#on importe le module tkinter qui nous permettra de cliquer sur un bouton pour afficher le graphique et les racines de la fonction
from tkinter import ttk
#On importe un sous-module de tkinter pour pouvoir l'utiliser en dehors de l'objet

x = 6
def calculate(*args):
#on définit la fonction qui permet de calculer les racines d'une fonction
    value = eval(fonction.get())
    zeros.set(value)
#pour l'instant c'est une autre fonction qui est insérée, lorsque une fonction est rentrée (en language python), la fonction remplace x par 6 et calcule 
   

window = Tk()
#On définit la fenêtre
window.title = "find roots of a function"
#On donne un titre à la fenêtre

window.bind("<Return>", calculate)
#Ce morceau de code permet de lancer la fonction calculate en pressant enter, sans cliquer sur le bouton 'calculate'

mainframe = ttk.Frame(window, padding="3 3 12 12")
#Dans la fenêtre on crée une frame dont on définit déjà la taille (en cm)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#La fonction grid permet de placer la frame à un certain endroit, en haut à gauche dans notre cas

fonction = StringVar()
#on définit 'fonction' comme une variable sous forme de string
fonction_entry = ttk.Entry(mainframe, width=12, textvariable=fonction)
#On définit l'endroit où il faudra insérer la fonction, le texte inséré est la fonction (textvariable), le nombre de caractères qu'on peut insérer avant qu'il décale c'est 12 (width) et il appartient au mainframe
fonction_entry.grid(column=2, row=1, sticky=(W))
#on place l'endroit où il faudra insérer la fonction, grâce à la fonction grid, à un endroit spécifique

zeros = StringVar()
#on définit 'Zeros' comme une variable sous forme de string
zeros_affichage = ttk.Entry(mainframe, textvariable=zeros, width=12, state='disabled')
#On définit l'endroit où il faudra insérer la fonction 
#le texte inséré est le string correspondant à 'zeros' (textvariable)
#le nombre de caractères qu'on peut insérer avant qu'il décale est 12 (width) et il appartient au mainframe
#l'entrée est inactive, pour qu'on ne puisse rien y insérer (disabled)
zeros_affichage.grid(column=2, row=2, sticky=(W, E))
#le texte retourné, les zéros de la fonction, seront affichés à un endroit spécifique

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
#le bouton permettant de lancer le calcul des zéros sera placé à un certain endroit

ttk.Label(mainframe, text="fonction").grid(column=3, row=1, sticky=W)
#on définit l'emplacement de 'fonction' qui permettra d'indiquer que le rectangle supérieur correspond à la fonction
ttk.Label(mainframe, text="racines").grid(column=3, row=2, sticky=W)
#on définit l'emplacement de 'racines' qui permettra d'indiquer que le rectangle inférieur correspond aux zéros de la fonction

fonction_entry.focus()
#ceci permet de faire en sorte que la souris aille directement dans l'entrée reservée à la fonction, pour ne pas avoir à bouger le curseur





