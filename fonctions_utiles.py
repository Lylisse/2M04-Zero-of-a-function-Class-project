import matplotlib.pyplot as plt
import numpy as np

def plot_function(f, x_values_list, zeros, *args, **kwargs):
    x_values = np.array(x_values_list)
    y_values = np.array([])
    holelist= []
    for x in x_values:
        try:
            y_values = np.append(y_values, f(x))
        except:
            y_values = np.append(y_values, np.nan)
            holelist.append(x)
    plt.plot(x_values, y_values, *args, **kwargs)
    for z in zeros:
        zy = [0]*len(zeros)
    try:
        plt.plot(z, zy, linestyle='none', marker='*', markersize=16)
        plt.plot(holelist, zy, linestyle='none', marker='O', markersize=16)
    except:
        pass

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

def derivee_seconde(f, h=10 ** -5):
    def f_double_prime(x):
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

    return f_double_prime


if __name__ == '__main__':
    # rien de particulier à écrire
    # 😃
    pass





