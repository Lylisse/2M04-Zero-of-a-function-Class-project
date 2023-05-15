import mpmath as mp
import matplotlib.pyplot as plt
import numpy as np
if(True):#si on utilise le bonus mettre True sinon False
    from InputInterpretation_bonus import textToPythonInterpretable


def plot_function(f, x_values, *args, **kwargs):
    y_values = []
    for x_value in x_values:
        y_values.append(f(x_value))
    plt.plot(x_values, y_values, *args, **kwargs)


def make_function_from_string(str_func, variable_name='x',lib="numpy"):
    """Permet de transformer le string d'une fonction (str_func) en fonction python qui retourne le résultat de la valeur entrée
    Le paramètre optionel "variable_name" correspond au nom de la variable que l'on souhaite.
    Par exemple,
    f = make_function_from_string('y ** 2', 'y')
    print(f(3))
    -> 9"""
    if(True): #si on utilise le bonus mettre True sinon False
        return eval(f'lambda {variable_name}: {textToPythonInterpretable(str_func,lib)}')
    else:
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




