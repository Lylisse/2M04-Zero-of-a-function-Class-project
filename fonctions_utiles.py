import matplotlib.pyplot as plt

def plot_function(f, x_values, *args, **kwargs):
    y_values = []
    for x in x_values:
        y_values.append(f(x))
    plt.plot(x_values, y_values, *args, **kwargs)

def make_function_from_string(str_func, variable_name='x'):
    """Permet de transformer le string d'une fonction (str_func) en fonction python qui retourne le résultat de la valeur entrée
    Le paramètre optionel "variable_name" correspond au nom de la variable que l'on souhaite.
    Par exemple,
    f = make_function_from_string('y ** 2', 'y')
    print(f(3))
    -> 9"""

    return eval(f'lambda {variable_name}: {str_func}')

def derivee(f, h=10 ** -6):
    def f_prime(x):
        return (f(x + h) - f(x - h)) / (2 * h)  # definition de la dérivée

    return f_prime

if __name__ == '__main__':
    # rien de particulier à écrire
    # 😃
    pass




