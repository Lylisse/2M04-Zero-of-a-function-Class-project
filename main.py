from InputInterpretation import *
from AlgebraicAnalysis import *


def testFuncDevelopment():
    return developFunc(textToFunc(input()))
def testFuncInterpretation():
    return textToFunc(input())
def testFuncDevAndSimpl():
    return developAndSimplifyFunc(textToFunc(input()))
def testFuncDerivative():
    return Derivate(textToFunc(input()))


while True:
    print(developAndSimplifyFunc(testFuncDerivative()))

