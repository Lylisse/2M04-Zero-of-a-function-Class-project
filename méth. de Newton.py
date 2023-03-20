def derivee(f, h=10**-5):
    def f_prime(x):
        return (f(x+h)-f(x-h))/(2*h)
    return f_prime



x = 0
funct = "x**2 + 2*x + (x - 6)"

def newton(funct):
    listdepoint = []
    for x in range (-100, 100):
        fonction = eval(funct)
        listdepoint.append((fonction))
    
    print(listdepoint)
    zero = []
    j = 10**10
    for i in listdepoint:
        if j - i > abs(j): 
            zero.append(j)
        j = i
    return zero


for i in range(10):
    point = newton(funct)
    print(derivee(funct(point)))
    funct = str(derivee(funct(point))) + "*x"

print(point)


print(newton(funct))