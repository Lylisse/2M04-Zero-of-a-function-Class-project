from InputInterpretation import *
from AlgebraicAnalysis import *
#from bouton_tkinter import *
from fonctions_utiles import *
from random import *

#des trucs pour tester des trucs
while True:
    randFunc=getOnexRandomFunc(maxDepth=2,maxLength=3,types=["-","+","*","/","^","sin","cos","tan","const","ln","exp"])
    print(randFunc)
    print(t0f_Algebriquement(randFunc))
    input()
while True:
    aFunc=0
    simplifiedFunc=0
    while aFunc==simplifiedFunc:
        aFunc=getRandomFunc(maxDepth=5)
        print(aFunc)
        simplifiedFunc = developAndSimplifyFunc(aFunc)
        print(simplifiedFunc)
    for _ in range(50):
        randomTest=random()*1000000
        print(aFunc.getValue(randomTest))
        print(simplifiedFunc.getValue(randomTest))
    print(aFunc)
    print(simplifiedFunc)
    input()
