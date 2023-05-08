from bracketing import t0f_bracketing
from fonctions_utiles import derivee, make_function_from_string

def newton(f: callable, zeros_approx: list):
    """Cette fonction prends en paramètre une fonction (dans le sens mathématique, une fonction réelle), et une liste
    contenant des valeurs qui sont proches de certains de ses zéros.
    Par exemple, si la fonction vaut f = sin, alors on pourrait avoir zeros_approx = [-3.2, 0.05, 3.1, 6.2], car toutes
    ces valeurs sont relativement proches de vrais zéros de la fonction.

    Le but de cette fonction est de "raffiner" cette approximation : on passerait par exemple de
    [-3.2, 0.05, 3.1, 6.2] à [-3.141526..., -4.1708374...e-05, 3.141616..., 6.283377...]
    ce qui nous donnerait de biens meilleures approximations des vrais zéros de f.

    Pour arriver à ce but, nous utiliseront ici la méthode de "Newton" (ou "Newton-Raphson").

    Supposons que l'on ait le point z se trouvant dans "zeros_approx".
    On calcule alors la droite (donnée par ax + b = y) tangente au point (z, f(z)). On trouve donc :
    a = f'(z)
    b = f(z) - a*z
    De sorte que la pente soit de f'(z) et que (z, f(z)) soit sur la droite.

    Pour continuer avec la méthode, nous calculons l'intersection de cette droite avec l'axe des x.
    On pose donc :
    az' + b = 0
    Ce qui nous donne z' = -b/a

    La théorie nous dit ensuite que, normalement, z' devrait être plus proche du zéro recherché que z.

    Voici comment nous obtenons le code suivant : """

    f_prime = derivee(f)  # on doit définir la dérivée de la fonction
    nouveaux_zeros = []  # cette liste contiendra l'approximation plus précise des zéros

    for z in zeros_approx:  # pour chacun des zéros approximatifs
        a = f_prime(z)  # on calcule la valeur de a
        b = f(z) - a * z  # et celle de b comme décrites dans le commentaire au début de la fonction

        z_prime = -b/a  # on calcule donc la nouvelle valeur de z

        nouveaux_zeros.append(z_prime)  # et on l'ajoute à notre liste

    return nouveaux_zeros  # on retourne nos nouvelles approximations

def t0f_newton(f: callable, a, b, nb_de_valeurs_a_calculer=10**4, nb_d_itterations=10):
    zeros = t0f_bracketing(f, a, b, nb_de_valeurs_a_calculer)

    for _ in range(nb_d_itterations):
        zeros = newton(f, zeros)

    return zeros


if __name__ == '__main__':  
    """__name__ c'est le nom que python va donner au programme quand il va être lancé, 
    donc si __name__ == '__main__' ça veut dire que ce programme est le programme principal.
    Comme ce bout de code est un exemple d'utilisation, il va être exécuté que si on lance ce fichier python.
    Si on lance le fichier global de recherche de zéros, cet exemple sera pas exécuté."""
    
    # exemples de bonne utilisation des fonctions

    from math import sin

    def fonction(x):
        return sin(x ** 2)

    exemple1 = t0f_newton(fonction, -3, 3)
    print(f'{exemple1 = }')
    # -> exemple1 = [-2.5066282746310007, -1.7724538509055163, 1.7724538509055163, 2.5066282746310007]









