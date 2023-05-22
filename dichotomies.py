from bracketing import ti1z_bracketing
from zeros_avec_taylor import ti1z_sturm_taylor


def t0i_bracketing_dichotomie(f: callable, a: float, b: float, epsilon=10**-10):
    #le epsilon est la marge d'erreur dans laquelle la fonction doit être pour être considérée comme un zéro, pour f(x):x->x et epsilon=1, les zéros sont i appartenant à [-1,1]
    c = (a + b) * 0.5  # moyenne entre a et b
    while abs(f(c)) > epsilon:
        if f(a) * f(c) < 0:  # f(a) et f(c) ont pas le même signe
            b = c
        # elif f(a)*f(c)==0 :
        #    cas ne pouvant pas se présenter à cause de la condition de la boucle while
        else:
            a = c
        c = (a + b) * 0.5  # moyenne entre a et b
    return c

def t0i_bracketing_regula_falsi(f: callable, a: float, b: float, epsilon=10**-10):
    c = a - f(a) * (b-a)/(f(b)-f(a))  # formule regula falsi
    while abs(f(c)) > epsilon:
        if f(a) * f(c) < 0:  # f(a) et f(c) ont pas le même signe
            b = c
        # elif f(a)*f(c)==0 :
        #    cas ne pouvant pas se présenter à cause de la condition de la boucle while
        else:
            a = c
        c = a - f(a) * (b-a)/(f(b)-f(a))  # formule regula falsi
    return c


def t0f_bracketing_dichotomie(f, a, b, epsilon=10 ** -10, nb_de_valeurs_a_calculer=10 ** 4):
    zeros, intervalles_avec_1_zero = ti1z_bracketing(f, a, b, nb_de_valeurs_a_calculer=nb_de_valeurs_a_calculer)
    for intervalle in intervalles_avec_1_zero:
        zeros.append(t0i_bracketing_dichotomie(f, intervalle[0], intervalle[1], epsilon=epsilon))
    return zeros

def t0f_bracketing_regula_falsi(f, a, b, epsilon=10 ** -10, nb_de_valeurs_a_calculer=10 ** 4):
    zeros, intervalles_avec_1_zero = ti1z_bracketing(f, a, b, nb_de_valeurs_a_calculer=nb_de_valeurs_a_calculer)
    for intervalle in intervalles_avec_1_zero:
        zeros.append(t0i_bracketing_regula_falsi(f, intervalle[0], intervalle[1], epsilon=epsilon))
    return zeros

# BONUS :
def t0f_sturm_taylor_dichotomie(f, a, b, epsilon=10 ** -10):
    zeros = []
    intervalles_avec_1_zero = ti1z_sturm_taylor(f, a, b)
    for intervalle in intervalles_avec_1_zero:
        zero = float(t0i_bracketing_dichotomie(f, intervalle[0], intervalle[1], epsilon=epsilon))
        if zero not in zeros:
            zeros.append(zero)
    return zeros


if __name__ == '__main__':
    # exemples de bonne utilisation des fonctions

    from math import sin

    def fonction(x):
        return sin(x ** 2)

    exemple1 = t0f_bracketing_dichotomie(fonction, -3, 3)
    print(f'{exemple1 = }')
    # exemple1 = [-2.5066282746434756, -1.772453850889341, 1.7724538508886802, 2.506628274642815]

    exemple2 = t0f_bracketing_regula_falsi(fonction, -3, 3)
    print(f'{exemple2 = }')
    # -> exemple2 = [-2.506628274630497, -1.772453850904248, 1.772453850904248, 2.506628274630497]


    # BONUS
    import mpmath as mp  # il faut mpmath pour les calculs avec Taylor
    def fonction_mpmath(x):
        return mp.sin(x ** 2)

    exemple3 = t0f_sturm_taylor_dichotomie(fonction_mpmath, -3, 3)
    print(f'{exemple3 = }')
    # -> exemple3 = ([-2.506628274618963, -1.772453850902344, 0.0, 1.772453850902344, 2.506628274618963],
    # la liste des zéros trouvés (ON A LE 0!!! nice)









