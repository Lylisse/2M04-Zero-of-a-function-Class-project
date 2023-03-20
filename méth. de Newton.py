# Fichier ne fonctionnant pas encore, travail en cours

def derivee(f, h=10**-5):
    def f_prime(x):
        return (f(x+h)-f(x-h))/(2*h)
    return f_prime



x = 0
funct = "x**2 + 2*x + (x - 6)"

def make_function_from_string(str_func, variable_name='x'):    # str_func: la fonction sous forme de string
	return eval(f'lambda {variable_name}: {str_func}')    # On applique variable_name comme variable dans str_func grace à la fonction lambda


def newton(funct):
    listdepoint = []
    for x in range (-100, 100):
        fonction = eval(funct)
        listdepoint.append((fonction))
    
    print(listdepoint)
    zero = []
    for index, valeur in enumerate(listdepoints):
        if valeur * listdepoint[index+1] <= 0:    # Il y a un changement de signe entre les deux points
            zeros.append(valeur)
    return zero


for i in range(10):
    point = newton(funct)    # On obtient les zéros approximatifs
    print(derivee(funct(point)))
    funct = str(derivee(funct(point))) + "*x"

print(point)


print(newton(funct))