import matplotlib.pyplot as plt
import numpy as np


def numerical_derivative(f, h=10 ** -6):
    def f_prime(x):
        return (f(x + h) - f(x - h)) / (2 * h)

    return f_prime


def second_derivative(f, h=10 ** -5):
    def f_double_prime(x):
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

    return f_double_prime


def hayley_method(f: callable, a, b, precision, max_depth=100):
    f_prime = numerical_derivative(f)
    f_double_prime = second_derivative(f)
    guess = (a + b) / 2
    recursion_depth = 0
    while abs(f(guess)) >= precision and recursion_depth < max_depth:
        f_guess = f(guess)
        f_prime_guess = f_prime(guess)
        f_double_prime_guess = f_double_prime(guess)
        guess = guess - (2 * f_guess * f_prime_guess) / (2 * f_prime_guess ** 2 - f_guess * f_double_prime_guess)
        recursion_depth += 1
    return guess


def secant_method(f: callable, a, b, precision, max_depth=100):
    depth = 0
    while abs(f(a)) >= precision and depth < max_depth:
        memory = a
        a = a - ((a - b) / (f(a) - f(b))) * f(a)
        b = memory
    return a


if __name__ == '__main__':
    dim = 10 ** 3

    x_axis = np.arange(0, dim, 10 ** -2)
    arr = [np.sin(x) for x in x_axis]

    guess = secant_method(np.sin, 8, 11, 10 ** -10)
    plt.plot(guess, np.sin(guess), 'ro')

    plt.plot(x_axis, arr)
    plt.show()
