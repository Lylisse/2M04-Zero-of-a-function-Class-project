# Fichier ne fonctionnant pas encore, travail en cours

def derivee(f, h=10**-5):
    def f_prime(x):
        return (f(x+h)-f(x-h))/(2*h)
    return f_prime


function_str = "x**2 + 2*x + (x - 6)"

def make_function_from_string(str_func, variable_name='x'):    # Permet de transformer le string d'une fonction (str_func) en fonction python qui retourne le résultat de la valeur entrée
    return eval(f'lambda {variable_name}: {str_func}')    # On applique variable_name comme variable dans str_func grace à la fonction lambda

funct = make_function_from_string(function_str)

def newton(f):
    listdepoints = []
    for x in range (-100, 100):
        listdepoints.append(int(f(x)))
    
    print(listdepoints)
    zero = []
    for index, valeur in enumerate(listdepoints):
        if valeur * listdepoints[index-1] <= 0:    # Il y a un changement de signe entre les deux points
            zero.append(valeur)
    return zero


for i in range(10):
    point = newton(funct)    # On obtient les zéros approximatifs
    print(point)
    f_prim = derivee(funct)
    print(f_prim(point[0]))
