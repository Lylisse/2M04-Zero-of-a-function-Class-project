import mpmath as mp

mp.mp.prec = 500  # on établi une précision arbitraire, par exemple 500 bits par float

def derivee_n_ieme(f: callable, n: int, h: float) -> callable:  # "callable" veut en gros dire que c'est une fonction
    """Ici, f est la fonction réelle qu'on cherche à dériver.

    On sait que la définition de la dérivée est :
    f'(x) = lim_(h->0) (f(x+h) - f(x))/h

    Cependant, nous ne pouvons pas prendre un h infiniment petit comme la définition nous le demanderai,
    et on est donc contraint de prendre un h très très petit (qu'on spécifie comme paramètre car on pourrait vouloir le changer).

    Pour des raisons de précision de calculs, nous utiliserons en fait la formule :
    f'(x) = lim_(h->0) (f(x+h) - f(x-h))/2h
    plutot que celle du dessus, car elle approche la vraie dérivée plus rapidement lors qu'elle existe.

    Pour finir avec les paramètres, n est simplement l'ordre de la dérivée, c'est à dire que si on veut la dérivée, n = 1,
    si on veut la deuxième dérivée, n = 2, etc.
    _______________________________________________________________________________________________________________________________

    La fonction derivee_n_ieme retournera une fonction réelle, qui sera la n_ieme derivee de f bien évidement.
    _______________________________________________________________________________________________________________________________

    Nous voudrons calculer des dérivées potentiellement de degré très élevé, par exemple n = 50,
    et il est donc utile de pouvoir les calculer rapidement.
    Voyons ce qui se passerai si on cherchait à calculer les dérivées d'ordre n:
    n = 1 : f'(x) ~= (f(x+h) - f(x-h))/2h
    n = 2 : f''(x) ~= (f'(x+h) - f'(x-h))/2h
    ...
    n quelquonque : f(n')(x) ~= (f((n-1)')(x+h) - f((n-1)')(x-h))/2h

    Il y a ici un problème : pour calculer la dérivée d'ordre n, il faut calculer deux dérivées d'ordre n-1.
    Cela veut dire que le temps de calcul en fonction de l'ordre de la dérivée sera exponentiel, ce qui est très mauvais.

    Pour remédier à ce problème, nous allons simplifier les expressions. Par exemple, pour f''(x) :
    f''(x) ~= (f'(x+h) - f'(x-h))/2h = ((f(x+2h) - f(x))/2h - (f(x) - f(x-2h))/2h)/2h = (f(x+2h) - 2f(x) + f(x-2h))/4h^2

    Même avec ce petit exemple, on n'utilise dans le dernier cas (simplifié) que 3 fois la fonction f, plutot que 4
    dans le cas ou on n'avait pas simplifié ; mais cet avantage ne fait que grandir :
    f'''(x) ~= (f(x + 3h) - 3f(x + 1h) + 3f(x - 1h) - f(x - 3h))/8h^3
    n'utilise que 4 fois la fonction f, plutot que 8 sans simplifier.

    Pour représenter la formule qui prends la n_ieme dérivée d'une fonction, nous utiliserons un dictionaire :
    il prendra un coefficient que l'on place devant le h et rendra le coefficient que l'on place devant le f.
    Par exemple, pour
    f''(x) ~= (f(x+2h) - 2f(x) + f(x-2h))/4h^2, on a que 2 -> 1 car f(x + /2/h) a un coefficient 1 devant.
    De même, 0 -> -2 car f(x + /0/h) a un coefficient -2 devant (on a dans la formule -2f(x)).

    Le dictionnaire associé à la dérivée seconde est donc {2: 1, 0: -2, -2: 1},
    et celui associé à la troisième dérivée est {3: 1, 1: -3, -1: 3, -3: -1} (on s'occupera du dénominateur plus tard).
    """

    derivee_simple = {1: 1, -1: -1}
    derivee_n = {0: 1}  # on commence par aucune derivee

    for i in range(n):
        nouvelle_derivee_n = {}
        for coeff_h1, coeff_f1 in derivee_simple.items():
            for coeff_h2, coeff_f2 in derivee_n.items():
                """on combine coeff_f1*f(x + coeff_h1*h) et coeff_f2*f(x + coeff_h2*h) pour donner :
                coeff_f1 * coeff_f2 * f(x + (coeff_h1 + coeff_h2)*h)"""
                
                coeff_h = coeff_h1 + coeff_h2
                coeff_f = coeff_f1 * coeff_f2

                if coeff_h not in nouvelle_derivee_n.keys():  
                    # si on a pas déjà de valeur pour le coeff, il faut la démarrer à 0 
                    nouvelle_derivee_n[coeff_h] = 0
                    
                nouvelle_derivee_n[coeff_h] += coeff_f  # une fois qu'on en a une, on y ajoute le coeff_f
                
        derivee_n = nouvelle_derivee_n.copy()

    h = mp.mpf(h)

    denominateur = (2*h) ** n

    def fonction_derivee_de_f(x):  # c'est cette fonction-là qu'on va return
        x = mp.mpf(x)
        total = 0

        for coeff_h, coeff_f in derivee_n.items():
            total += coeff_f * f(x + coeff_h*h)

        total /= denominateur

        return total

    return fonction_derivee_de_f











