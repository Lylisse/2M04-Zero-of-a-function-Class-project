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

def developFunc(aFunc):
    aFunc=simplifyUselessSubFuncs(aFunc)
    if(aFunc.type in ["const","x"]+BasicFunctionsNames):
        return aFunc
    aFunc.vars=[developFunc(aVar) for aVar in aFunc.vars]
    if(aFunc.type=="+"):
        return simplifyUselessSubFuncs(aFunc)
    if(aFunc.type=="*"):#on applique la distributivité
        numbOfAddsPerArg=[1]*len(aFunc.vars)
        numberOfFinalvars=1 #le nombre de developpements que la fonction aura à la fin, par exemple 3*sin(x)*2*ln(3+2) ne peut pas être developpé par distributivité et la valeur restera 2, mais (3x+4)*x oui et la valeur sera 2*1 = 2, pour (a+b)*(c+d+e)*f la valeur sera 2*3*1=6, il y aura 6 arguments additionnés: a*c*f+a*d*f+a*e*f+b*c*f+b*d*f+b*e*f
        for (index,anArg)in enumerate(aFunc.vars):
            if(anArg.type=="+"):
                numbOfAddsPerArg[index]=len(anArg.vars)
                numberOfFinalvars*=len(anArg.vars)
        if(numberOfFinalvars==1):#si on ne peut pas développer par distributivité
            return aFunc
        else:
            combinations=getAllCombinations(numbOfAddsPerArg)
            addVars=[]
            for aCombination in combinations:
                multVars=[]
                for (index,value) in enumerate(aCombination):
                    if(aFunc.vars[index].type!="+"):
                        if(value!=0):
                            print("valeur de l'indexe voulu erronée!")
                        multVars.append(aFunc.vars[index])
                    else:
                        multVars.append(aFunc.vars[index].vars[value])
                addVars.append(simplifyUselessSubFuncs(Function("*",multVars)))
            return Function("+",addVars)
    if(aFunc.type=="^"):
        if(aFunc.vars[-1].type=="+"):
            multVars=[]
            for aVar in aFunc.vars[-1].vars:
                multVars.append(Function("^",aFunc.vars[:-1]+[aVar]))
            return Function("*",multVars)
        else:
            if(len(aFunc.vars)>2):
                aFunc.vars[-2]*=aFunc.vars[-1]
                return developFunc(Function("^",aFunc.vars[:-1]))
            else:
                return aFunc
    return aFunc



def getAllCombinations(arrayOfArraysLengths):
    if(len(arrayOfArraysLengths)==1):
        return [[numb]for numb in range(arrayOfArraysLengths[0])]
    else:
        returnArray=[]
        for i in range(arrayOfArraysLengths[0]):
            for aCombination in getAllCombinations(arrayOfArraysLengths[1:]):
                returnArray.append([i]+aCombination)
        return returnArray
    
def simplifyFunc(aFunc):
    if(aFunc.type=="const" or aFunc.type=="x"):
        return aFunc
    if(aFunc.type not in BasicFunctionsNames): 
        aFunc.vars=[simplifyFunc(aVar) for aVar in aFunc.vars]

    if(aFunc.type=="+"):
        newVars=[]
        for aVar in aFunc.vars:
            if(aVar.type!="const" or aVar.vars!=0):
                newVars.append(aVar)
        if(len(newVars)==0):
            return cf(0)
        elif(len(newVars)==1):
            return newVars[0]
        else:
            return Function("+",newVars)
    if(aFunc.type=="*"):
        newVars=[]
        for aVar in aFunc.vars:
            if(aVar.type!="const"):
                newVars.append(aVar)
            elif(aVar.vars==0):
                return cf(0)
            elif(aVar.vars!=1):
                newVars.append(aVar)
        if(len(newVars)==0):
            return cf(1)
        elif(len(newVars)==1):
            return newVars[0]
        else:
            return Function("*",newVars)
        
    return aFunc

        
def developAndSimplifyFunc(aFunc):
    aFunc=developFunc(aFunc)
    return simplifyFunc(aFunc)





if __name__ =="__main__":
    while True:
        print(getAllCombinations([5,2,2]))
        input()
