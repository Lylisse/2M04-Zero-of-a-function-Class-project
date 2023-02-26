from InputInterpretation import *

def Derivate(aFunc):
    if(aFunc.type=="const"):
        return Function("const",0)
    elif(aFunc.type=="x"):
        return Function("const",1)
    elif(aFunc.type=="sin"):
        return Function("cos",aFunc.vars)*Derivate(aFunc.vars)
    elif(aFunc.type=="cos"):
        return -1*Function("sin",aFunc.vars)*Derivate(aFunc.vars)
    elif(aFunc.type=="tan"):
        return Function("const",1)/(Function("cos",aFunc.vars)^2)*Derivate(aFunc.vars)
    elif(aFunc.type=="+"):
        return Function("+",[Derivate(eachFunc) for eachFunc in aFunc.vars])
    elif(aFunc.type=="*"):
        if(len(aFunc.vars)==2):
            return Derivate(aFunc.vars[0])*aFunc.vars[1]+aFunc.vars[0]*Derivate(aFunc.vars[1])
        else:
            leftFunc=Function("*",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc*rightFunc)
    elif(aFunc.type=="/"):
        if(len(aFunc.vars)==2):
            return (Derivate(aFunc.vars[0])*aFunc.vars[1]-aFunc.vars[0]*Derivate(aFunc.vars[1]))/aFunc.vars[1]**2
        else:
            leftFunc=Function("/",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc/rightFunc)
    elif(aFunc.type=="^"):
        if(len(aFunc.vars)==2):
            return Derivate(Function("exp",aFunc.vars[1]*Function("ln",aFunc.vars[0])))
        else:
            leftFunc=Function("^",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc**rightFunc)
    elif(aFunc.type=="exp"):
        return aFunc*Derivate(aFunc.vars)
    elif(aFunc.type=="ln"):
        return Function("const",1)/aFunc.vars*Derivate(aFunc.vars)
    elif(aFunc.type=="arccos"):
        return Function("const",-1)/((cf(1)-Function("x",None)**cf(2)))**(cf(0.5))*Derivate(aFunc.vars)
    elif(aFunc.type=="arcsin"):
        return Function("const",1)/((cf(1)-Function("x",None)**cf(2)))**(cf(0.5))*Derivate(aFunc.vars)
    elif(aFunc.type=="arctan"):
        return Function("const",1)/(cf(1)+Function("x",None)**cf(2))*Derivate(aFunc.vars)

if __name__ =="__main__":
    while True:
        inputFunc=textToFunc(input())
        print(inputFunc)
        print(Derivate(inputFunc))
