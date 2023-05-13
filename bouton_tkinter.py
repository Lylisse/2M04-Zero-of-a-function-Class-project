from tkinter import *
#on importe le module tkinter qui nous permettra de cliquer sur un bouton pour afficher le graphique et les racines de la fonction
from tkinter import ttk
#On importe un sous-module de tkinter pour pouvoir l'utiliser en dehors de l'objet
from dichotomies import t0i_bracketing_dichotomie

noerror = "no error detected"
fcterror = "La fonction que vous avez entrée n'est pas correcte."
intervalerror = "L'intervalle que vous avez entrée n'est pas correcte. (Les virgules ne sont pas acceptées.)"
nomethodselecterror = "Aucune méthode n'a été sélectionnée."

methods_list = (5, 3, 2, 1)
def calculate_zeros(method, function, interval):
#on choisit quelle méthode utilisée puis envoyons en arguments la fonction et l'intervalle sous la forme suivante:"[{fonction}, {début de l'intervalle},  {fin de l'intervalle}]"
    try:
        if float(interval[1]) > float(interval[0]):
            interval = [float(interval[0]), float(interval[1])]
            errorLabel.config(text=noerror)
        else:
            raise Exception("")
    except:
        errorLabel.config(text=intervalerror)
    if method == "method1":
        global fct_zeros
        fct_zeros = t0i_bracketing_dichotomie(function, interval[0], interval[1])
        errorLabel.config(text=fct_zeros)
    elif method == "method2":
        pass
    else:
        errorLabel.config(text=nomethodselecterror)


window = Tk()
#On définit la fenêtre
window.title = "find roots of a function"
#On donne un titre à la fenêtre

window.bind("<Return>", calculate_zeros)
#Ce morceau de code permet de lancer la fonction calculate_zeros en pressant enter, sans cliquer sur le bouton 'calculate_zeros'

mainframe = ttk.Frame(window, padding="3 3 12 12")
#Dans la fenêtre on crée une frame dont on définit déjà la taille (en cm)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#La fonction grid permet de placer la frame à un certain endroit, en haut à gauche dans notre cas

fonction = StringVar()
#on définit 'fonction' comme une variable sous forme de string
fonction_entry = ttk.Entry(mainframe, textvariable=fonction)
#On définit l'endroit où il faudra insérer la fonction, le texte inséré est la fonction (textvariable), le nombre de caractères qu'on peut insérer avant qu'il décale c'est 12 (width) et il appartient au mainframe
fonction_entry.grid(column=1, row=1, sticky=(W))
#on place l'endroit où il faudra insérer la fonction, grâce à la fonction grid, à un endroit spécifique
ttk.Label(mainframe, text="fonction").grid(column=2, row=1, sticky=W)
#on définit l'emplacement de 'fonction' qui permettra d'indiquer que le rectangle supérieur correspond à la fonction

debut_intervalle = StringVar()
#on définit "debut_intervalle" comme une variable sous forme de String pour le transformer en float
debut_intervalle_entry = ttk.Entry(mainframe, textvariable=debut_intervalle)
#on définit l'entry
debut_intervalle_entry.grid(column=1, row=2, sticky=(W))
#on place l'entry sur dans le frame
ttk.Label(mainframe, text="à").grid(column=2, row=2)
#on définit l'emplacement de 'racines' qui permettra d'indiquer que le rectangle inférieur correspond aux zéros de la fonction
fin_intervalle = StringVar()

fin_intervalle_entry = ttk.Entry(mainframe, textvariable=fin_intervalle)

fin_intervalle_entry.grid(column=3, row=2)

ttk.Label(mainframe, text="Intervalle").grid(column=4, row=2)

methode_1_select = StringVar()

ttk.Checkbutton(mainframe, text="dichotomie", variable=methode_1_select, onvalue="method1").grid(column=1, row=3)


ttk.Checkbutton(mainframe, text="méthode 2", variable=methode_1_select, onvalue="method2").grid(column=2, row=3)


ttk.Button(mainframe, text="calculate_zeros", command=lambda:calculate_zeros(methode_1_select.get(), fonction_entry.get(), [debut_intervalle_entry.get(), fin_intervalle_entry.get()])).grid(column=1, row=4, sticky=W)
#le bouton permettant de lancer le calcul des zéros sera placé à un certain endroit

errorLabel = ttk.Label(mainframe, text=noerror)
errorLabel.grid(row=4, column=5)

fonction_entry.focus()
#ceci permet de faire en sorte que la souris aille directement dans l'entrée reservée à la fonction, pour ne pas avoir à bouger le curseur

mainloop()
#la fonction mainloop initialise tkinter en général
