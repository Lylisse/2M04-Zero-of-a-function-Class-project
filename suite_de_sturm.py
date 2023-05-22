"""Utilisation des suites de sturm pour trouver le nombre de zéros
d'une fonction polynomiale
"""
import numpy as np
Polynomial = np.polynomial.Polynomial

def suite_de_Sturm(P0: Polynomial):  # Ici on utilise le théoreme de Sturm pour trouver une suite de polynomes dont on baisse le degré à chaque itération
    P1 = P0.deriv()  # Dérivée du polynome de base

    suite_de_polynome = [P0, P1]
    Pn = P1

    while Pn.degree() > 0:
        P_n_moins_2 = suite_de_polynome[-2]  # Avant dernier élément de la suite
        P_n_moins_1 = suite_de_polynome[-1]  # Dernier élément de la suite

        # Le "%" donne le reste de la division euclidienne
        # Pour trouver Pn on doit prende l'opposé du reste de la division euclidienne de Pn-2 par Pn-1
        Pn = -P_n_moins_2 % P_n_moins_1

        suite_de_polynome.append(Pn)

    return suite_de_polynome


# Fonction qui donne 1 si le nombre et positif, -1 si il est négatif et 0 si il est nul
def signe(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    else:
        return 0


def nb_changements_de_signe(liste_de_nombres):  # Fonction qui permet de trouver le nombre de changments de signe dans une liste de nombres
    nombre_de_changements = 0
    signe_precedent = 0
    for nb in liste_de_nombres:
        if nb != 0:  # Attention il faut ignorer les zéros pour les changements de signe avec la suite du code
            if signe(nb) * signe_precedent == -1:  # Si le signe est différent du précédent le le résultat de leur multiplication sera négatif
                nombre_de_changements += 1  # Dans ce cas on ajoute 1 au nombre total de changements de signe
            signe_precedent = signe(nb)
    return nombre_de_changements


def evaluation_suite_polynome_en_x(suite_de_polynome, x):  # Fonctiom qui sert a remplacer les x dans une suite de polyôme par un nb donné
    liste_retour = []
    for polynome in suite_de_polynome:
        liste_retour.append(polynome(x))  # Cette fonction permet simplement de remplacer les x par un nb donné
    return liste_retour


# ATTENTION : Il s'agit bien de racines *simples*
def nombre_de_racines_simples(suite_polynome, a, b):  # on cherche le nombre de racines simples du polynome dans l'intervalle [a, b]
    # suite_polynome = suite_de_Sturm(polynome)

    suite_eval_a = evaluation_suite_polynome_en_x(suite_polynome, a)  # Evalue la suite de polynomes en a
    suite_eval_b = evaluation_suite_polynome_en_x(suite_polynome, b)  # Evalue la suite de polynomes en b

    # pour trouver le nombre de racines simples, on fait la différence entre le nombre de changements de signe de la suite
    # évaluée en a et en b (voir formule de Sturm)
    return nb_changements_de_signe(suite_eval_a) - nb_changements_de_signe(suite_eval_b)


def ti1z_suite_sturm(suite_polynome, a, b, intervalle_minimum=10 ** -5):  # Cette fonction permet d'avoir dans un intervalle donné une seule racine
    """Cette fonction nous permet de séparer l'intervalle [a, b] en intervalles plus petit qui n'ont qu'une seule racine
    Si on a plus que 1 racine on spépare notre intervalle en intervalles plus petits de sorte qu'il n'ait que une racine simple

    "intervalle_minimum" est là comme mesure de sécurisé, au cas où il y aurait une racine non simple"""

    if abs(a - b) < intervalle_minimum:
        return (a, b),  # si l'intervalle est très petit, mais apparaît avoir plus qu'une racine,
        # on part du principe que c'est une racine double (ou plus) et on la compte comme une seule

    nb_de_racines_simples_suite = nombre_de_racines_simples(suite_polynome, a, b)
    if nb_de_racines_simples_suite == 1:  # Ici on return l'intervalle ayant une racine simple
        return (a, b),
    elif nb_de_racines_simples_suite == 0:  # Si l'intervalle n'a pas de racine alors on le "néglige"
        return tuple()
    else:
        return ti1z_suite_sturm(suite_polynome, a, (2 * a + b) / 3, intervalle_minimum=intervalle_minimum) + \
               ti1z_suite_sturm(suite_polynome, (2 * a + b) / 3, (a + 2 * b) / 3, intervalle_minimum=intervalle_minimum) + \
               ti1z_suite_sturm(suite_polynome, (a + 2 * b) / 3, b, intervalle_minimum=intervalle_minimum)
    # Ici on sépare l'intervalle [a, b] en trois intervalles plus petits
    # Utiliser 3 plutot que 2 a enlevé des bugs


def ti1z_polynome(polynome, a, b, intervalle_minimum=10 ** -3):  # Cette fonction permet d'avoir dans un intervalle donné une seule racine
    """Cette fonction nous permet de séparer l'intervalle [a, b] en intervalles plus petit qui n'ont qu'une seule racine
    Si on a plus que 1 racine on spépare notre intervalle en intervalles plus petits de sorte qu'il n'ait que une racine simple"""

    suite_polynome = suite_de_Sturm(polynome)

    intervalles_1_zero = ti1z_suite_sturm(suite_polynome, a, b, intervalle_minimum)

    return intervalles_1_zero


if __name__ == '__main__':
    # exemples de bonne utilisation des fonctions
    
    # Polynomial([0, 1]) = 0 + x
    # Polynomial([-1, 1]) = -1 + x
    # Polynomial([-3, 1, 9]) = -3 + x + 9x^2
    fonction_polynomiale1 = Polynomial([0, 1]) * Polynomial([-1, 1]) * Polynomial([-2, 1]) * Polynomial([3, 1]) * Polynomial([2, 1])
    # Polynome dont les racines sont 0, 1, 2, -3 et -2
    print(f'{fonction_polynomiale1 = }')

    exemple1 = ti1z_polynome(fonction_polynomiale1, -5, 5)
    print(f'{exemple1 = }')
    # -> exemple1 = ((-3.888888888888889, -2.777777777777778), (-2.777777777777778, -1.6666666666666667), (-0.5555555555555556, 0.5555555555555556), (0.5555555555555556, 1.6666666666666667), (1.6666666666666667, 5))
    # chacun des intervalles contient 1 zéro
    
    print()
    
    fonction_polynomiale2 = Polynomial([0, 1]) * Polynomial([-1, 1]) * Polynomial([-1, 1]) * Polynomial([3, 1]) * Polynomial([2, 1])
    print(f'{fonction_polynomiale2 = }')


    exemple2 = ti1z_polynome(fonction_polynomiale2, -5, 5)
    print(f'{exemple2 = }')
    # -> exemple2 = ((-3.888888888888889, -2.777777777777778), (-2.777777777777778, -1.6666666666666667), (-1.6666666666666667, 1.6666666666666667))
    # chacun des intervalles contient 1 zéro













