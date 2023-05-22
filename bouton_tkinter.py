# BONUS

import numpy as np
from matplotlib.pyplot import show, plot
from math import ceil
from tkinter import *
# on importe le module tkinter qui nous permettra de cliquer sur un bouton pour afficher le graphique et les racines de la fonction
from tkinter import ttk
# On importe un sous-module de tkinter pour pouvoir l'utiliser en dehors de l'objet


from dichotomies import t0f_bracketing_dichotomie, t0f_bracketing_regula_falsi, t0f_sturm_taylor_dichotomie
from bracketing import t0f_bracketing
from methode_halley import t0f_halley
from newton import t0f_newton
if True:#si on utilise le bonus mettre True sinon False
    from AlgebraicAnalysis_bonus import t0f_Algebriquement_bonus
    from InputInterpretation_bonus import textToFunc

from fonctions_utiles import make_function_from_string

from fonctions_utiles import plot_function


toutes_les_methodes = ['t0f_halley', 't0f_newton', 't0f_bracketing', 't0f_bracketing_dichotomie', 't0f_bracketing_regula_falsi', 't0f_sturm_taylor_dichotomie','t0f_Algebriquement_bonus']


def calculate_zeros(method, function, interval):
    # on choisit quelle méthode utilisée puis envoyons en arguments la fonction et l'intervalle sous la forme suivante:"[{fonction}, {début de l'intervalle},  {fin de l'intervalle}]"
    fctvariable = 'x'
    
    if fctvariable in fonction.get():
        try:
            if float(interval[1]) > float(interval[0]):
                interval = [float(interval[0]), float(interval[1])]
                errorLabel.config(text=noerror)
            else:
                raise Exception("")
        except:
            errorLabel.config(text=intervalerror)

        try:
            if method=="t0f_sturm_taylor_dichotomie":
                fct_zeros = t0f_sturm_taylor_dichotomie(make_function_from_string(function, fctvariable,"mpmath"), interval[0], interval[1])
            elif method=="t0f_Algebriquement_bonus":
                fct_zeros = t0f_Algebriquement_bonus(textToFunc(function))
            else:
                fct_zeros = eval(f'{method}(make_function_from_string(function, fctvariable), interval[0], interval[1])')
            display_graph(make_function_from_string(function, fctvariable), np.linspace(interval[0], interval[1], 10_000),
                          fct_zeros)

        except NameError:
            errorLabel.config(text=nomethodselecterror)
    else:
        errorLabel.config(text="Vous n'avez pas mis de 'x' dans votre fonction...")


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
debut_intervalle.set("-100")
#on définit le début de l'intervalle comme étant -100 par défault
debut_intervalle_entry = ttk.Entry(mainframe, textvariable=debut_intervalle)
# on définit l'entry
debut_intervalle_entry.grid(column=1, row=2, sticky=(W))
# on place l'entry sur dans le frame
ttk.Label(mainframe, text="à").grid(column=2, row=2)
# on définit l'emplacement de 'racines' qui permettra d'indiquer que le rectangle inférieur correspond aux zéros de la fonction
fin_intervalle = StringVar()

fin_intervalle.set("100")
#on définit la fin de l'intervalle comme étant 100 par défault

fin_intervalle_entry = ttk.Entry(mainframe, textvariable=fin_intervalle)

fin_intervalle_entry.grid(column=3, row=2)

ttk.Label(mainframe, text="Intervalle").grid(column=4, row=2)

methode_1_select = StringVar()

for i, nom_methode in enumerate(toutes_les_methodes):
    ttk.Checkbutton(mainframe, text=nom_methode.replace('_', ' ').replace('t0f', '', ), variable=methode_1_select,
                    onvalue=nom_methode).grid(row=3, column=i + 1)


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













