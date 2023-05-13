import numpy as np
from matplotlib.pyplot import show, plot
from math import ceil
from tkinter import *
# on importe le module tkinter qui nous permettra de cliquer sur un bouton pour afficher le graphique et les racines de la fonction
from tkinter import ttk
# On importe un sous-module de tkinter pour pouvoir l'utiliser en dehors de l'objet
from dichotomies import t0f_bracketing_dichotomie

from fonctions_utiles import make_function_from_string

from fonctions_utiles import plot_function


def calculate_zeros(method, function, interval):
    # on choisit quelle méthode utilisée puis envoyons en arguments la fonction et l'intervalle sous la forme suivante:"[{fonction}, {début de l'intervalle},  {fin de l'intervalle}]"
    try:
<<<<<<< Updated upstream
        fctvariable = 'x'  # detect_variable(function)
=======
        fctvariable = "x"
>>>>>>> Stashed changes
    except:
        errorLabel.config(text=varerror)
    try:
        if float(interval[1]) > float(interval[0]):
            interval = [float(interval[0]), float(interval[1])]
            errorLabel.config(text=noerror)
        else:
            raise Exception("")
    except:
        errorLabel.config(text=intervalerror)
    if method == "method1":
<<<<<<< Updated upstream
        try:
            fct_zeros = t0f_bracketing_dichotomie(make_function_from_string(function, fctvariable), interval[0],
                                                  interval[1])
=======
        fct_zeros = t0f_bracketing_dichotomie(make_function_from_string(function, fctvariable), interval[0], interval[1])
        """try:
            fct_zeros = t0f_bracketing_dichotomie(make_function_from_string(function, fctvariable), interval[0], interval[1])
>>>>>>> Stashed changes
        except:
            errorLabel.config(text=fcterror)"""

    elif method == "method2":
        pass
    else:
        errorLabel.config(text=nomethodselecterror)
    display_graph(make_function_from_string(function, fctvariable), np.linspace(interval[0], interval[1], 10_000), fct_zeros)


def detect_variable(function):
    for i in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"]:
        if i in function:
            return i


def display_graph(f, x_values, zeros):
    graphframe.grid()
    graphframe.tkraise()
    plot_function(f, x_values)
    plot(zeros, [0] * len(zeros), '*')
    show()


noerror = "no error detected"
fcterror = "La fonction que vous avez entrée n'est pas correcte."
intervalerror = "L'intervalle que vous avez entrée n'est pas correcte. (Les virgules ne sont pas acceptées.)"
nomethodselecterror = "Aucune méthode n'a été sélectionnée."
varerror = "Veuillez utiliser les lettres de l'alphabet."

window = Tk()
# On définit la fenêtre
window.title = "find roots of a function"
# On donne un titre à la fenêtre
window.bind("<Return>", calculate_zeros)
# Ce morceau de code permet de lancer la fonction calculate_zeros en pressant enter, sans cliquer sur le bouton 'calculate_zeros'

mainframe = ttk.Frame(window, height=80, width=500)
# Dans la fenêtre on crée une frame dont on définit déjà la taille (en cm)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# La fonction grid permet de placer la frame à un certain endroit, en haut à gauche dans notre cas

graphframe = ttk.Frame(window, height=300, width=500)

fonction = StringVar()
# on définit 'fonction' comme une variable sous forme de string
fonction_entry = ttk.Entry(mainframe, textvariable=fonction)
# On définit l'endroit où il faudra insérer la fonction, le texte inséré est la fonction (textvariable), le nombre de caractères qu'on peut insérer avant qu'il décale c'est 12 (width) et il appartient au mainframe
fonction_entry.grid(column=1, row=1, sticky=(W))
# on place l'endroit où il faudra insérer la fonction, grâce à la fonction grid, à un endroit spécifique
ttk.Label(mainframe, text="fonction").grid(column=2, row=1, sticky=W)
# on définit l'emplacement de 'fonction' qui permettra d'indiquer que le rectangle supérieur correspond à la fonction

debut_intervalle = StringVar()
# on définit "debut_intervalle" comme une variable sous forme de String pour le transformer en float
debut_intervalle_entry = ttk.Entry(mainframe, textvariable=debut_intervalle)
# on définit l'entry
debut_intervalle_entry.grid(column=1, row=2, sticky=(W))
# on place l'entry sur dans le frame
ttk.Label(mainframe, text="à").grid(column=2, row=2)
# on définit l'emplacement de 'racines' qui permettra d'indiquer que le rectangle inférieur correspond aux zéros de la fonction
fin_intervalle = StringVar()

fin_intervalle_entry = ttk.Entry(mainframe, textvariable=fin_intervalle)

fin_intervalle_entry.grid(column=3, row=2)

ttk.Label(mainframe, text="Intervalle").grid(column=4, row=2)

methode_1_select = StringVar()

ttk.Checkbutton(mainframe, text="dichotomie", variable=methode_1_select, onvalue="method1").grid(column=1, row=3)

ttk.Checkbutton(mainframe, text="méthode 2", variable=methode_1_select, onvalue="method2").grid(column=2, row=3)

ttk.Button(mainframe, text="calculate_zeros",
           command=lambda: calculate_zeros(methode_1_select.get(), fonction_entry.get(),
                                           [debut_intervalle_entry.get(), fin_intervalle_entry.get()])).grid(column=1,
                                                                                                             row=4,
                                                                                                             sticky=W)
# le bouton permettant de lancer le calcul des zéros sera placé à un certain endroit

errorLabel = ttk.Label(mainframe, text=noerror)
errorLabel.grid(row=4, column=5)

fonction_entry.focus()
# ceci permet de faire en sorte que la souris aille directement dans l'entrée reservée à la fonction, pour ne pas avoir à bouger le curseur


mainloop()
# la fonction mainloop initialise tkinter en général
