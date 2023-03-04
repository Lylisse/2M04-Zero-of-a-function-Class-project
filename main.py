from InputInterpretation import *
from AlgebraicAnalysis import *

while True:#setup pour tester la dérivation de fonction

    inputFunc=textToFunc(input())

    derivateFunc=Derivate(inputFunc)

    simplifiedFunc=developAndSimplifyFunc(derivateFunc)

    print(simplifiedFunc)

