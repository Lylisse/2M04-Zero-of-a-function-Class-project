from fonctions_utiles import derivee, derivee_seconde
from bracketing import t0f_bracketing


# ici c'est exactement la même logique que pour newton, mais en utilisant aussi la dérivée seconde
# cette méthode n'est à priori *pas* en bonus

def halley(f: callable, zeros_aprox):
    f_prime = derivee(f)
    f_seconde = derivee_seconde(f)
    nouveaux_zeros = []  # cette liste contiendra l'approximation plus précise des zéros

    for z in zeros_aprox:
        f_z = f(z)
        f_prime_z = f_prime(z)
        f_sec_z = f_seconde(z)
        nouveau_z = z - (2 * f_z * f_prime_z) / (2 * f_prime_z ** 2 - f_z * f_sec_z)
        nouveaux_zeros.append(nouveau_z)

    return nouveaux_zeros

def t0f_halley(f: callable, a, b, nb_de_valeurs_a_calculer=10**4, nb_d_itterations=10):
    zeros = t0f_bracketing(f, a, b, nb_de_valeurs_a_calculer)

    for _ in range(nb_d_itterations):
        zeros = halley(f, zeros)

    return zeros


if __name__ == '__main__':
    # exemples de bonne utilisation des fonctions

    from math import sin


    def fonction(x):
        return sin(x ** 2)


    exemple1 = t0f_halley(fonction, -3, 3)
    print(f'{exemple1 = }')
    # -> exemple1 = [-2.5066282746310007, -1.772453850905516, 1.772453850905516, 2.5066282746310007]

    
    
    
