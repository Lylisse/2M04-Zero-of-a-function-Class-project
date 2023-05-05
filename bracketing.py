import numpy as np

def i1z_bracketing(f: callable, a: float, b: float, nb_de_valeurs_a_calculer=10 ** 4) -> (list, list):
    """
    Le but de cette fonction est, pour une fonction "f" et un intervalle (a, b) donnés, calculer un très grand nombre
    de valeurs dans cet intervalle, dans l'idée que si on calcule beaucoup de valeurs, on devrait bien, à un moment,
    tomber complètement par hazard sur une valeur proche d'un zéro. On considère que l'on a trouvé une valeur proche
    d'un zéro lors qu'on change de signe ; si par exemple f(1.232) < 0 < f(1.233), alors 1.232 et 1.233 sont proche d'un
    zéro de f. Plus spécifiquement, en supposant que f est continue, il existe un zéro dans l'intervalle (1.232, 1.233).

    La fonction "bracketing" retourne une liste d'intervalles tels que décris ci-dessus, dans lesquels on a observé un
    changement de signe ; et une liste (qui sera très surement vide) contenant les accidentels zéros qui auraient été
    trouvés. Par exemple si on vérifie f(1.232) et on trouve que f(1.232) == 0, alors on l'ajoutera à cette liste.

    La fonction "bracketing" prend comme paramètres:
    la fonction réelle "f"
    l'intervalle (a, b)
    le nombre de valeurs que l'on souhaite calculer, i.e. si on demande 100 valeurs sur l'intervalle (0, 1),
    on calculera f(0), f(0.01), f(0.02), ..., f(0.99), f(1) (oui ça fait 101 valeurs au total je sais, on s'en fout un peu)

    """

    delta_x = (b - a) / nb_de_valeurs_a_calculer  # c'est le "saut" à faire entre chaque valeur qu'on calcule
    list_de_x_a_verifier = np.arange(a, b + delta_x, delta_x)  # https://numpy.org/doc/stable/reference/generated/numpy.arange.html

    liste_de_y = map(f, list_de_x_a_verifier)  # on calcule f à toutes les valeurs x
    # https://docs.python.org/3/library/functions.html#map

    zeros_approx = []
    y_precedent = 0  # ignorez pour l'instant
    x_precedent = a  # ignorez pour l'instant

    solutions_trouvees_par_hazard = []  # liste des zéros qu'on aura peut être accidentellement trouvé

    for x, y in zip(list_de_x_a_verifier, liste_de_y):  # "zip" itère dans les deux liste en même temps
        if y == 0:  # si y == 0, on a juste trouvé un zéro
            solutions_trouvees_par_hazard.append(x)

        if y * y_precedent < 0:  # c'est à dire si on a observé un changement de signe
            """on a du définir y_precedent = 0 avant afin de ne pas avoir de problèmes à cette étape, qui compare le y
            actuel avec le y précédent.
            À noter que l'on arrivera jamais ici à la première itération, ce qui est une bonne chose, car 
            y * y_precedent sera égal à zéro, puisqu'on a défini y_precedent = 0 au début."""
            zeros_approx.append((x_precedent, x))  # on ajoute le x à la liste d'zeros_approx

        # finalement, on change les valeurs de y et x precedents pour leurs valeurs actuelles pour l'itération suivante.
        y_precedent = y
        x_precedent = x

    return solutions_trouvees_par_hazard, zeros_approx

def t0f_bracketing(f: callable, a: float, b: float, nb_de_valeurs_a_calculer=10 ** 4) -> list:
    zeros_accidentellement_trouves, intervalles_1_zero = i1z_bracketing(f, a, b, nb_de_valeurs_a_calculer)

    valeurs_proche_d_un_zero = []
    for intervalle_1_zero in intervalles_1_zero:
        valeurs_proche_d_un_zero.append(sum(intervalle_1_zero) / 2)  # c'est juste la moyenne de l'intervalle

    return zeros_accidentellement_trouves + valeurs_proche_d_un_zero


if __name__ == '__main__':
    # exemples de bonne utilisation des fonctions

    from math import sin

    def fonction(x):
        return sin(x ** 2)

    exemple1 = i1z_bracketing(fonction, -3, 3)
    print(f'{exemple1 = }')
    # -> exemple1 = ([], [(-2.5068000000000543, -2.5062000000000544), (-1.7730000000001351, -1.7724000000001352), (1.7723999999994744, 1.7729999999994739), (2.506199999999394, 2.5067999999993935)])
    # chacun des intervalles dans la 2ème liste contient 1 zéro
    # la première liste est vide, on n'est tombé sur aucun zéro

    exemple2 = t0f_bracketing(fonction, -3, 3)
    print(f'{exemple2 = }')
    # -> exemple2 = [-2.506500000000054, -1.7727000000001352, 1.7726999999994741, 2.5064999999993938]
    # cela correspond *à peu près* au zéros de la fonction sur l'intervalle

    # Notons qu'il n'a pas trouvé le point fonction(0) = 0 car sin(x**2) ne croise pas l'axe des x en 0.
    # Ceci est scinificatif car toutes les méthodes qui se basent sur le bracketing (beaucoup) ne trouverons pas ce zéro
    # Plus généralement, ce genre de zéro est très dur à trouver pour à peu près toutes les méthodes, car il y a très peu
    # de moyen de les prédire








