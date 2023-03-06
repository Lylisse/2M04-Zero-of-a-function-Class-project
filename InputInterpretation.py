from copy import deepcopy
BasicFunctionsNames=["sin","cos","tan","arcsin","arccos","arctan","exp","ln"]
class Function: #on définit les propriétés de l'object fonction
    def __init__(self,atype,funcVars):
        self.type=atype # parmi ces types"+","*","/","^","sin","cos","tan","const","x","ln","exp","arcsin","arccos","arctan" #on veut que la fonction soit simple pour ensuite l'analyser
        self.vars=funcVars # une chaine contenant les variables de la fonction 
        #(par exemple pour 5x + 13 on a vars=[5x,13] et type="+")
        if(atype in ["+","/","^","-"] and len(funcVars)<2):
            print("invalid number of args!",atype)# example 5 il y a juste une partie a droite et pas a gauche, il manque ducoup la variable a gauche
    def __str__(self):#on définit ce qu'il va arriver lorsque on utilise la fonction str(<notre object fonction>)
        return SimplifyEasyParenth(self.toString())#on retourne la fonction en la transformant en une chaine de caractère (avec la fonction qu'on définit juste après) et on utilise la fonction qui simplifie les parenthèses pour que ça soit propre
    def __mul__(self, other):#  ici on  implote les operations arithmetiques binaire (+,-,*,/,**,) ici on definit la multiplication
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return Function("*",[self,other])
    def __rmul__(self, other):# ici on definit la proprietée de la multiplication a droite et a gauche example "2*x" a droite et "x*2" a gauche
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return Function("*",[self,other])
    def __truediv__(self, other):# ici on definit la division
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return Function("/",[self,other])
    def __add__(self, other):#ici on definit l'addition
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return simplifyUselessSubFuncs(Function("+",[self,other]))
    def __sub__(self, other):# ici on definit la soustraction
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return Function("-",[self,other])
    def __pow__(self, other):
        if(type(other)==int or type(other)== float):
            other=Function("const", other)
        return Function("^",[self,other])
    def __eq__(self,other):
        if(not isinstance(other,Function)):
            return False
        if(self.type=="x" and other.type=="x"):
            return True
        if(self.type!=other.type):
            return False
        if(isinstance(self.vars,list) and isinstance(other.vars,list)):
            for var in self.vars:
                if var not in other.vars:
                    return False
            for var in other.vars:
                if var not in self.vars:
                    return False
        elif(self.vars!=other.vars):
            return False
        return True
    def deepcopy(self):
        return deepcopy(self)
    def toString(self):
        if(self.type=="x"):
            return "x"
        elif(self.type=="const"):
            return str(self.vars)
        elif(self.type in ["-","+","*","/","^"]):
            returnText=""
            for aFunc in self.vars:
                returnText+=aFunc.toString()
                returnText+=self.type
            return "("+returnText[:-1]+")"
        elif(self.type in BasicFunctionsNames):
            return self.type+"("+self.vars.toString()+")"
        else:
            print("impossible to convert func to str!")
            return ""
def cf(number):
    return Function("const",number)
def standardizeFunc(text): #fonction qui par exemple renvoie 2*x pour 2x
    newText=text
    for index in range(len(text)):
        reverseIndex=len(text)-index-1
        if text[reverseIndex] in [")","x"] and reverseIndex+1<len(text):
            if text[reverseIndex+1].isnumeric() or text[reverseIndex+1]in["(","x"]:
                newText=newText[:reverseIndex+1]+"*"+newText[reverseIndex+1:]

        if text[reverseIndex] in ["(","x"] and reverseIndex-1>=0:
            if text[reverseIndex-1].isnumeric():
                newText=newText[:reverseIndex]+"*"+newText[reverseIndex:]
    return SimplifyEasyParenth(newText)


def simplifyUselessSubFuncs(aFunc):
    if(aFunc.type in ["+","*"]):
        newVars=[]
        for anArg in aFunc.vars:
            if(anArg.type==aFunc.type):
                newVars+=anArg.vars
            else:
                newVars.append(anArg)
        return Function(aFunc.type,newVars)
    else:
        return aFunc

def getValuesStacks(intArray):#fonction qui pour une liste donnée retourne une liste contenant pour chaque element la liste des indexes des éléments adjacents qui ont une valeur proche, par exemple pour [1,2,3,7,8] on retourne [(0,1,2),(0,1,2),(0,1,2),(3,4),(3,4)]
    stacksArray=[]
    lastNumb=intArray[0]
    for numb in intArray:
        if(abs(numb-lastNumb)==1):
            stacksArray[-1]+=1
        else:
            stacksArray.append(1)
        lastNumb=numb
    returnArray = [set()]*len(intArray)

    parenthIndex=0
    for stackLength in stacksArray:
        stackArrayOfIndexs=set()
        for i in range(stackLength):
            stackArrayOfIndexs.add(parenthIndex+i)
        for i in range(stackLength):
            returnArray[parenthIndex+i]=stackArrayOfIndexs
        parenthIndex+=stackLength
    return returnArray

def verifParenthCoherence(text):#fonction qui verifie la coherence des parenthèses, par exemple "()" retourne vrai mais ")((","())(()"ou")(" retourne faux
    parenthDepth=0
    for char in text:
        if char=="(":
            parenthDepth+=1
        if char==")":
            parenthDepth-=1
            if parenthDepth<0: # la profondeur de parenthèse ne doit pas être négative par ex: "(2x+1)x+2)" ne doit pas être accepté 
                return False
    return True

def GetOpenAndCloseParenthIndexs(text):#fonction qui va indexer les parenthèses d'une notation suivant leur ordre d'ouverture et qui va retourner une liste avec l'endroit de la chaine ou elles s'ouvrent et une liste avec l'endroit de la chaîne où elles se ferment par ex pour "(12+x)*3*(3-(4-x))" elle retourne:[0,9,12] et [5,16,17]
    openedParenthsArray=[]
    lastOpenedParenth=0
    OpenIndexofParenths=[None]*text.count("(")
    CloseIndexofParenths=[None]*text.count(")")
    for index in range(len(text)):
        char = text[index]
        if char=="(":
            OpenIndexofParenths[lastOpenedParenth]=index
            openedParenthsArray.append(lastOpenedParenth)
            lastOpenedParenth+=1
        
        elif char==")":
            CloseIndexofParenths[openedParenthsArray[-1]]=index
            openedParenthsArray.pop()
    return OpenIndexofParenths,CloseIndexofParenths
    

def SimplifyEasyParenth(text):#fonction qui simplifie les parenthèses ouvertes deux fois par exemple pour"3*((2+3))" elle retourne 3*(2+3)
    if(type(text)!=str):
        print("impossible d'interpréter la fonction! #112")
        return ""
    if(text.count("(")==0):
        return text
    
    
    if(text[0]=="(" and text[-1]==")"):
        if(verifParenthCoherence(text[1:-1])):
            return SimplifyEasyParenth(text[1:-1])

    
    OpenIndexofParenths,CloseIndexofParenths=GetOpenAndCloseParenthIndexs(text)

    OpenStacks=getValuesStacks(OpenIndexofParenths)
    CloseStacks=getValuesStacks(CloseIndexofParenths)

    parenthsToDelete=set()
    for index in range(len(OpenIndexofParenths)):
        if(index not in parenthsToDelete):
            for parenthIndex in OpenStacks[index].intersection(CloseStacks[index]):
                if(parenthIndex!=index):
                    parenthsToDelete.add(parenthIndex)

    indexsToRemove=[]
    for parenthIndex in parenthsToDelete:
        indexsToRemove.append(OpenIndexofParenths[parenthIndex])
        indexsToRemove.append(CloseIndexofParenths[parenthIndex])
    editedText=""
    for index in range(len(text)):
        if index not in indexsToRemove:
            editedText+=text[index]
    return editedText

def ignoreParenths(text):#fonction qui ignore le contenu dans les parenthèses par exemple pour "2*(lolmdr des trucs bzr)+12x"renvoie "2*+12x"
    editedText=""
    parenthIndex=0
    for char in text:
        if char=="(":
            parenthIndex+=1
        if parenthIndex==0:
            editedText+=char
        if char==")":
            parenthIndex-=1
    return editedText

def textToFunc(text): # 2^3x = (2^3)*x => la multiplication sans opérateur n'a pas la priorité
    text=standardizeFunc(text)
    splittedText=[]
    
    referenceText=ignoreParenths(text)

    if(text=="x"):
        return Function("x",None)
    for basicOperator in ["+","*","/","^"]:
        if(referenceText.find(basicOperator)!=-1):
            parenthIndex=0
            textbit=""
            for char in text:
                if char==basicOperator and parenthIndex==0:
                    splittedText.append(textbit)
                    textbit=""
                else:
                    textbit+=char
                    if char=="(":
                        parenthIndex+=1
                    elif char==")":
                        parenthIndex-=1
            splittedText.append(textbit)
            return Function(basicOperator,[textToFunc(atext) for atext in splittedText])
    if(referenceText in BasicFunctionsNames):
        return Function(referenceText,textToFunc(text[len(referenceText)+1:-1]))
    else:
        if text.isdigit():
            return Function("const",int(text))
        else:
            try:
                return Function("const",float(text))
            except:
                print("impossible d'interpréter la fonction!#190")
                return ""


#fonction de débuggage non-utilisée en temps normal
#fonction utile pour voir si il n'y a pas de référence dupliquée dans une même fonction, 
# par exemple pour x*2+x*2 si la référence de la fonction "*" est dupliquée alors si on change le premier x*2 en x*2*sin(x) 
# la fonction deviendra x*2*sin(x)+x*2*sin(x) au lieu de x*2*sin(x)+x*2
def verifReferencesDuplicity(aFunc,foundRefs=[]): 
    allReferences=foundRefs
    if(isinstance(aFunc.vars,list)):
        for aVar in aFunc.vars:
            if(id(aVar) in allReferences):
                print("Duplicated func found of type: ",aVar.type)
                return True
            if(verifReferencesDuplicity(aVar,allReferences)):
                return True
            allReferences.append(id(aVar))
        
    elif(aFunc.type not in ["const","x"]):
        if(id(aFunc.vars) in allReferences):
            print("Duplicated func found of type: ",aFunc.vars.type)
            return True
        if(verifReferencesDuplicity(aFunc.vars,allReferences)):
            return True
        allReferences.append(id(aFunc.vars))
    return False
#fonction de débuggage non-utilisée en temps normal
#la fonction vérifie que les fonctions aient un nombre de variables cohérent par exemple "sin"ou"const" doit prendre une et une seule variable tandis ce que "+","*" ou "^" doivent en avoir au moins 2
def VerifyVarsCoherence(aFunc):
    if(aFunc.type=="x"):
        if(aFunc.vars==None):
            return True
    elif(aFunc.type=="const"):
        if(isinstance(aFunc.vars,float) or isinstance(aFunc.vars,int)):
            return True
    else:
        if(isinstance(aFunc.vars,list)):
            for aVar in aFunc.vars:
                if(not VerifyVarsCoherence(aVar)):
                    print("invalid var!#1",aFunc.type)
                    return False
        else:
            if(not VerifyVarsCoherence(aFunc.vars)):
                print("invalid var!#2",aFunc.type)
                return False
    if(aFunc.type in ["+","-","*","/","^"]):
        if(len(aFunc.vars)>1):
            return True
    elif(isinstance(aFunc.vars,Function)):
        return True
    print("invalid var!#3",aFunc.type)
    return False
