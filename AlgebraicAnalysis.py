from InputInterpretation import *
#les commentaires présents dans ce code paraiterons longs pour ceux qui conaissent bien le phyton, ces commentaires sont pour les "paumés en phyton". Donc si cela ne vous sert par ne les regardez pas. Je vais donner des comms pour toutes les lignes
def Derivate(aFunc): #On définit la fonction qui va dériver une fonction. La fct initiale va etre aFunc.
    if(aFunc.type=="const"): #On vérifie si la fonction est une fct constante
        return Function("const",0) #Si c'est le cas on retourne la fonction constante 0
    elif(aFunc.type=="x"):  #si la fct c'est x
        return Function("const",1)  #on retourne la dérivée qui est 1
    elif(aFunc.type=="sin"):  #On fait la meme chose mais avec le sin, donc on fait sa dérivée, et pareil pour les autres jusqu'a la ligne 13
        return Function("cos",aFunc.vars)*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="cos"):
        return -1*Function("sin",aFunc.vars)*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="tan"):
        return Function("const",1)/(Function("cos",aFunc.vars)^2)*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="+"): #Dérivée d'une fonction composée avec addition
        return Function("+",[Derivate(eachFunc) for eachFunc in aFunc.vars]) #On retourne la fonction + avec comme variables chaque varibales dérives de la fct initiale.
    elif(aFunc.type=="*"): #Dérivée d'une fonction composée avec multiplication
        if(len(aFunc.vars)==2): 
            return Derivate(aFunc.vars[0])*aFunc.vars[1]+aFunc.deepcopy().vars[0]*Derivate(aFunc.deepcopy().vars[1]) #On retourne la dérive de F(x)*g(x) #.vars veut dire on regarde les variables de la fonction de base, quand on met les crochet c'est pour dire la combientième variable que on regarde. Genre f(x)*g(x), aFunc.vars[0] c'est f(x) et [1] c'est g(x) aDunc.deepcopy c'est une copie de la fonction de base 
        else:
            leftFunc=Function("*",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc*rightFunc)
    elif(aFunc.type=="/"):
        if(len(aFunc.vars)==2):
            return (Derivate(aFunc.vars[0])*aFunc.vars[1]-aFunc.deepcopy().vars[0]*Derivate(aFunc.deepcopy().vars[1]))/aFunc.deepcopy().vars[1]**2  
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
        return aFunc*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="ln"):
        return Function("const",1)/aFunc.vars*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="arccos"):
        return Function("const",-1)/((cf(1)-aFunc.vars**cf(2)))**(cf(0.5))*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="arcsin"):
        return Function("const",1)/((cf(1)-aFunc.vars**cf(2)))**(cf(0.5))*Derivate(aFunc.deepcopy().vars)
    elif(aFunc.type=="arctan"):
        return Function("const",1)/(cf(1)+aFunc.vars**cf(2))*Derivate(aFunc.deepcopy().vars)



def developFunc(aFunc):
    """
    à utiliser avec précaution
    """
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
                        multVars.append(aFunc.vars[index].deepcopy())
                    else:
                        multVars.append(aFunc.vars[index].vars[value].deepcopy())
                addVars.append(simplifyUselessSubFuncs(Function("*",multVars)))
            return Function("+",addVars)
    if(aFunc.type=="^"):
        if(aFunc.vars[-1].type=="+"):
            multVars=[]
            for aVar in aFunc.vars[-1].vars:
                multVars.append(Function("^",aFunc.deepcopy().vars[:-1]+[aVar]))
            return Function("*",multVars)
        else:
            if(len(aFunc.vars)>2):
                aFunc.vars[-2]*=aFunc.vars[-1]
                return developFunc(Function("^",aFunc.vars[:-1]))
            else:
                return aFunc
    if(aFunc.type=="/"):
        multVars=[aFunc.vars[0]]
        for aVar in aFunc.vars[1:]:
            multVars.append(Function("^",[aVar,cf(-1)]))
        return Function("*",multVars)
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
    """
    à utiliser avec précaution
    """
    if(aFunc.type=="const" or aFunc.type=="x"):
        return aFunc
    if(type(aFunc.vars)==list):
        aFunc.vars=[simplifyFunc(aVar) for aVar in aFunc.vars]
    else:
        aFunc.vars=simplifyFunc(aFunc.vars)

    if(aFunc.type=="+"): # on additionne les constantes et on laisse le reste pareil, par exemple 2*x+3*x+2+3 -->2*x+3*x + 5 
        newVars=[]
        constVar=0
        for aVar in aFunc.vars:
            if(aVar.type!="const"):
                newVars.append(aVar)
            else:
                constVar+=aVar.vars
        if(constVar!=0):
            newVars.append(cf(constVar))
        if(len(newVars)==0):
            return cf(0)
        elif(len(newVars)==1):
            return newVars[0]
        else:
            return Function("+",newVars)
    elif(aFunc.type=="*"):# si il y a un 0 on retourne la fonction constante 0, on regroupe les coefficient constants et si on a au moins deux variables on applique la distributivité
        newVars=[]
        constVar=1
        for aVar in aFunc.vars:
            if(aVar.type!="const"):
                newVars.append(aVar)
            else:
                constVar*=aVar
        if(constVar==0):
            return cf(0)
        if(constVar!=1):
            newVars.append(cf(constVar))
        if(len(newVars)==0):
            return cf(1)
        elif(len(newVars)==1):
            return newVars[0]
        else:
            return ApplyMultDistributivity(Function("*",newVars))
    elif(aFunc.type=="exp"):
        if(aFunc.vars.type=="const" and aFunc.vars.vars==0):
            return cf(1)
        if(aFunc.vars.type=="*"):
            for multVarIndex,aMultVar in enumerate(aFunc.vars.vars):
                if(aMultVar.type=="ln"):
                    del aFunc.vars.vars[multVarIndex]
                    if(len(aFunc.vars.vars)<2):
                        return Function("^",[aMultVar.vars,aFunc.vars.vars[0]])

                    return Function("^",[aMultVar.vars,aFunc.vars])
    elif(aFunc.type=="^"):
        if(len(aFunc.vars)!=2):
            print("Fonction mal développée!")
        if(aFunc.vars[1].type=="const"):
            if(aFunc.vars[1].vars==0):
                return cf(1)
            elif(aFunc.vars[1].vars==1):
                return aFunc.vars[0]
    return aFunc

def ApplyMultDistributivity(aFunc): #fonction qui pour 2*x*x*sin(x)*sin(x)*sin(x) renvoie 2*x^2*sin(x)^3
    """
    à utiliser avec précaution
    """
    argPows=[] # liste qui enregistre les arguments et la puissance auxquels les arguments sont par exemple pour: 2xsin(x)sin(x) on aura {Function(x,None),cf(1),Function("sin",Function("x",None)),cf(2)}
    constArg=1
    for aVar in aFunc.vars:
        if aVar.type=="const":
            constArg*=aVar.vars
        elif aVar.type=="^":
            if(len(aVar.vars)!=2):
                print("Fonction mal développée!")
                print(VerifyVarsCoherence(aFunc))
                exit()
            else:
                if(aVar.vars[0] not in argPows):
                    argPows.append(aVar.vars[0])
                    argPows.append(aVar.vars[1])
                else:
                    argPows[argPows.index(aVar.vars[0])+1].vars+=aVar.vars[1].vars
        elif(aVar not in argPows):
            argPows.append(aVar)
            argPows.append(cf(1))
        else:
            argPows[argPows.index(aVar)+1].vars+=1
    multVars=[cf(constArg)]
    for index in range(len(argPows)//2):
        argPows[index*2+1]=simplifyFunc(argPows[index*2+1])
        multVars.append(simplifyFunc(Function("^",argPows[index*2:(index+1)*2])))
    return Function("*",multVars)


        
def developAndSimplifyFunc(aFunc):
    """
    à utiliser avec précaution
    """
    aFunc=developFunc(aFunc)
    aFunc=simplifyFunc(aFunc)
    if(verifReferencesDuplicity(aFunc,[])):
        print("Certaines références dans la fonctions sont dupliquées!")
    return aFunc

def isPolynomial(aFunc):
    aFunc=developAndSimplifyFunc(aFunc)
    if(isMonomial(aFunc)):
        return True
    if(aFunc.type=="+"):
        for anArg in aFunc.vars:
            if(not isMonomial(anArg)):
                return False
        return True
    return False
def isMonomial(aFunc):
    if(isConst(aFunc)):
        return True
    if(aFunc.type=="x"):
        return True
    if(aFunc.type=="*"):
        for anArg in aFunc.vars:
            if(not isConst(anArg) and not isMonomial(anArg)):
                return False
        return True
    if(aFunc.type=="^"):
        if(len(aFunc.vars)!=2):
            raise ValueError("La fonction doit être simplifiée!")
        if(aFunc.vars[0].type=="x" and isConst(aFunc.vars[1])):
            return True
    return False
            
def isConst(aFunc):
    if(aFunc.type=="const"):
        return True
    if(aFunc.type=="x"):
        return False
    if(aFunc.type in BasicFunctionsNames):
        if(not isConst(aFunc.vars)):
            return False
        else:
            return True
    for anArg in aFunc.vars:
        if(not isConst(anArg)):
            return False
    return True






if __name__ =="__main__":
    while True:
        print(getAllCombinations([5,2,2]))
        input()
