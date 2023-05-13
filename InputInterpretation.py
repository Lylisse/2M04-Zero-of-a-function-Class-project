from copy import deepcopy
from random import *

FuncTypes=["+","*","/","^","sin","cos","tan","const","x","ln","exp","arcsin","arccos","arctan"]
BasicFunctionsNames=["sin","cos","tan","arcsin","arccos","arctan","exp","ln"]
mpMathFunctionNames=["mp.sin","mp.cos","mp.tan","mp.asin","mp.acos","mp.atan","mp.exp","mp.ln"]
numpyFunctionNames=["np.sin","np.cos","np.tan","np.arcsin","np.arccos","np.arctan","np.exp","np.log"]
FuncStr="sincostanarccosarctanexpln"
operatorStr="-+*/^"
class Function: #on définit les propriétés de l'object fonction
    def __init__(self,atype,funcVars):
        self.type=atype # on définit le type de fonction parmi ces types"+","*","/","^","sin","cos","tan","const","x","ln","exp","arcsin","arccos","arctan"
        self.vars=funcVars # une chaine contenant les variables de la fonction, à noter que les fonctionx et const en ont pas
        #(par exemple pour 5x + 13 on a vars=[5x,13] et type="+")
        if(atype in ["+","/","^","-"] and len(funcVars)<2):
            print("invalid number of args!",atype)# il faut au moins deux variable pour définire une addition, division, etc...
    def __str__(self):#on définit ce qu'il va arriver lorsque on utilise la fonction str(<notre object fonction>) dans le code
        return SimplifyEasyParenth(self.toString())#on retourne la fonction en la transformant en une chaine de caractère (avec la fonction qu'on définit juste après) et on utilise la fonction qui simplifie les parenthèses pour que ça soit propre
    def __mul__(self, other):# ici on definit la multiplication
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
    def __pow__(self, other):# ici on definit la puissance
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

def getCharTypes(text):
    charTypesArray=[]
    for index in range(len(text)):#pour chaque index de caractère du texte
        char=text[index]
        if(char==")"):
            charTypesArray.append(")")
        elif(char=="("):
            charTypesArray.append("(")
        elif(char=="x"):
            charTypesArray.append("var")
        elif(char.isnumeric() or char=="."):
            charTypesArray.append("numb")
        elif(char in FuncStr):
            charTypesArray.append("func")
        elif(char in operatorStr):
            charTypesArray.append("operator")
        else:
            raise Exception("texte invalide!")
    return charTypesArray

def getParenthEndIndex(text):
    if(text[0]!="("):
        print("wrong input")

    parenthDepth=1
    index=1
    while parenthDepth!=0:
        if(index==len(text)):
            print("invalid input!")
        if(text[index]=="("):
            parenthDepth+=1
        if(text[index]==")"):
            parenthDepth-=1
        index +=1
    return index
        

def getLenOfMult(text, charTypes):
    index=0
    while index<len(text) and charTypes[index] not in ["operator",")"] :
        if(charTypes[index]=="("):
            index += getParenthEndIndex(text[index:])+index
        else:
            index+=1
    return index


def addUsefullParenths(initialText,triggerChar,chartypes=None):
    if(chartypes==None):
        chartypes=getCharTypes(initialText)

    newText=""
    lastIndex=0
    index=initialText.find(triggerChar)
    while index !=-1:
        newText+=initialText[lastIndex:index+1]
        multLen=getLenOfMult(initialText[index+1:],chartypes[index+1:])
        if(multLen!=0):
            newText+="("+initialText[index+1:index+multLen+1]+")"
        lastIndex=index+multLen+1
        if(initialText[index+1+multLen:].find(triggerChar)!=-1):
            index=initialText[index+1+multLen:].find(triggerChar)+index+1+multLen
        else:
            index=-1
    newText+=initialText[lastIndex:]


    return newText


def standardizeFunc(text):#fonction qui par exemple renvoie 2*x pour 2x
    text=text.replace("exp","eep")
    text=text.replace(" ","")#on enlève les espaces
    text=text.replace("**","^")#on remplace "**" par "^"; le symbole utilisé pour les puissances
    
    text=addUsefullParenths(text,"^")
    text=addUsefullParenths(text,"/")
    charTypesArray=getCharTypes(text)
    newText=""
    for charIndex in range(len(charTypesArray)-1):
        char = text[charIndex]
        newText+=char
        charType=charTypesArray[charIndex]
        nextCharType=charTypesArray[charIndex+1]
        if(charType == ")" and nextCharType not in ["operator",")"]):
            newText+="*"
        if(charType == "var" and nextCharType not in ["operator",")"]):
            newText+="*"
        if(charType == "numb" and nextCharType not in ["operator",")","numb"]):
            newText+="*"
    newText+= text[-1]
    newText= newText.replace("eep","exp")
        
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

def GetOpenAndCloseParenthIndexs(text):
    """Fonction qui va indexer les parenthèses d'une notation suivant leur ordre d'ouverture et qui va retourner une liste avec l'endroit de la chaine ou elles s'ouvrent et une liste avec l'endroit de la chaîne où elles se ferment par ex pour:
    "((x)x(x))" elle retourne:[0,1,5] et [8,3,7] en effet voici la liste de caractères selon leurs indexs: 
    0:'(' 1:'(' 2:'x' 3:')' 4:'x' 5:'(' etc. 
    On voit que des parenthèses s'ouvrent en 0, en 1 et en 5 elle se ferment en 3, en 7 et en 8
    Cependant la première parenthèse qui s'ouvre se ferme en dernier c'est pour cela que notre fonction renvoie [8,3,7] comme indexes de fermeture et non pas [3,7,8]"""

    #on veut savoir le numéro de la parenthèse que l'on ouvre, le numéro de la première sera donc 0, celui de la deuxième 1, troisième 2, etc.
    parenthIndex=0
    #pour être en mesure de savoir quelle parenthèse on ferme, on crée une liste où l'on stocke les numéros des parenthèses ouvertes
    openedParenthsIndexes=[]
    #on crée les listes selon le nombre de parenthèses qu'il y a dans le texte, si le texte est correct il devrait y avoir le même nombre de parenthèses ouvertes que de parenthèses fermées

    OpenIndexofParenths=[None]*text.count("(") # [None]*n = [None,None,None,None,None,None, ....n fois] une liste de longueur n dans laquelle chaque valeur est nulle
    # text.count("(") nous donne le nombre de fois qu'il y a de "(" dans le texte, par exemple pour "((xx(xx(" il retourne le nombre 4
    CloseIndexofParenths=[None]*text.count(")")# [None]*n = [None,None,None,None,None,None, ....n fois] une liste de longueur n dans laquelle chaque valeur est nulle
    # text.count(")") nous donne le nombre de fois qu'il y a de ")" dans le texte, par exemple pour ")x))x" il retourne le nombre 3

    #on va parcourir le texte avec un index, si le texte est "bonjour" la valeur de index sera d'abord index=0 puis index=1 puis 2,3,4,5,6
    for charIndex in range(len(text)):
        char = text[charIndex]  #on prend le caractère à l'index donné, si par exemple index=3 et le texte est "bonjour" cela nous donne le "j", si index=0 cela nous donne le "b", si index=6 cela nous donne le "r", etc..
        if char=="(": #si le caractère est une ouverture de parenthèse
            OpenIndexofParenths[parenthIndex]=charIndex #on connait l'index à laquelle s'ouvre la 'n'-ième parenthèse, la variable parenthIndex stocke ce 'n' ainsi ou peut dire qu'on ouvre la parenthIndex-ième parenthèse. Du coup on définit dans la liste 'OpenIndexofParenths' la parenthIndex-ième comme étant l'index du caractère (charIndex)
            openedParenthsIndexes.append(parenthIndex) #puisque on vient d'ouvrir la parenthIndex-ième parenthèse, on la rajoute a notre liste de parenthèses ouvertes
            parenthIndex+=1 #puisque on vient d'ouvrir la parenthIndex-ième parenthèse, la prochaine parenthèse sera parenthIndex+1  (variable+=n  est une abréviation de variable = variable + 1)
        
        elif char==")":#si le caractère est une fermeture de parenthèse
            closedParenthIndex=openedParenthsIndexes[-1] #on sait qu'on est entrain de fermer la dernière parenthèse ouverte, pour obtenir l'index de la dernière parenthèse ouverte on prend la liste 'openedParenthsIndexes' qui stocke les indexes des parenthèses ouvertes et on prends le dernier élément en utilisant '[-1]'
            CloseIndexofParenths[closedParenthIndex]=charIndex #on connait l'index à laquelle se ferme la 'closedParenthIndex'-ième parenthèse. Du coup on définit dans la liste 'OpenIndexofParenths' la 'closedParenthIndex'-ième comme étant l'index du caractère (charIndex)
            openedParenthsIndexes.pop()#puisque on a fermé la parenthèse on peut supprimer son index de la liste des parenthèses ouvertes (openedParenthsIndexes) en utilisant .pop() qui sert à supprimer la dernière valeur d'une liste

    #une fois qu'on est passé à travers tout le texte avec notre "charIndex" on a normalement tous les indexes d'ouverture et de fermeture
    return OpenIndexofParenths,CloseIndexofParenths
    

def SimplifyEasyParenth(text):
    """fonction qui simplifie les parenthèses ouvertes deux fois au lieu d'une par exemple pour "3*((2+3))" elle retourne "3*(2+3)", elle simplifie également "(x)" en "x" """
    if(type(text)!=str):#si le texte n'est pas une chaine de caractères (str) on ne peut pas interpréter ce que la fonction est
        print("impossible d'interpréter la fonction! #174")
        return ""
    if(text.count("(")==0):#si le texte n'a pas d'ouverture de parenthèses alors on ne peut sûrement pas les simplifier
        return text #on retourne donc le texte tel quel
    
    
    if(text[0]=="(" and text[-1]==")"): #si le texte est de la forme texte="('texteinterne')" avec 'texteintene' pouvant être n'importe quelle chaine de caractères
        if(verifParenthCoherence(text[1:-1])): #on regarde si les parenthèses restent cohérentes en prenant uniquement le 'texteinterne' Cela est fait en utilisant [1:-1] qui retourne le texte depuis son deuxième caractère (dont l'index est 1) jusqu'à sa ('n' moins 1)-ième avec n la longueur du texte
            #par exemple si notre texte est "(bonjour)" alors on peut le simplifier en "bonjour" mais si c'est "(x+y)(x-y)" on ne peut pas le simplifier en "x+y)(x-y", la fonction 'verifParenthCoherence' est chargée de nous dire que "x+y)(x-y" n'est pas cohérent
            return SimplifyEasyParenth(text[1:-1]) #si le texte reste cohérent alors on retourne la simplification de 'texteinterne'

    OpenIndexofParenths,CloseIndexofParenths=GetOpenAndCloseParenthIndexs(text)#on obtient les indexes d'ouverture et de fermeture des parenthèses dans le texte, par exemple si le texte est "(()())" on aura OpenIndexofParenths=[0,1,3] et CloseIndexofParenths=[5,2,4] ainsi pour savoir où s'ouvre la première parenthèse on utilise OpenIndexofParenths[0] (=0) et pour savoir où elle se ferme on utilise CloseIndexofParenths[0] (=5). On saura que la première parenthèse s'ouvre en 0 et se ferme en 5

    OpenStacks=getValuesStacks(OpenIndexofParenths) #on obtient pour chaque parenthèse les indexes des parenthèses ouvertes en même temps, par exemple pour "xxx((xxx()))" on aura [(0,1),(0,1),(2)] cela nous indique que la première parenthèse à été ouverte avec la deuxième et que la troisième à été ouverte toute seule.
    CloseStacks=getValuesStacks(CloseIndexofParenths)#on obtient pour chaque parenthèse les indexes des parenthèses fermées en même temps, par exemple pour "xxx((xxx())xxx)" on aura [(0),(2,1),(2,1)] cela nous indique que la première parenthèse ouverte à été fermée toute seule et que la deuxième ouverte à été fermée avec la troisième ouverte.

    parenthsToDelete=set()#on définit un set qui va stocker les indexes des parenthèses inutiles, un set est comme une liste sauf qu'il n'a pas d'ordre, on ne peut donc pas utiliser variable[n] pour obtenir la n-plus-unième valeur du set.

    numbOfParenth=len(OpenIndexofParenths)


    for index in range(numbOfParenth):#on va parcourir les parenthèses avec un index, si il y a 7 parenthèses dans le texte, la valeur de index sera d'abord index=0, puis index=1, puis 2, puis 3, 4, 5,6
        if(index not in parenthsToDelete):#si on n'a pas encore décidé de supprimer cette parenthèse
            newParenthsToDelete=OpenStacks[index].intersection(CloseStacks[index]) #toutes le parenthèses qui s'ouvrent et qui se ferment en même temps que la notre sont à supprimer, à l'exception de notre propre parenthèse (index)
            newParenthsToDelete.discard(index) #on retire donc notre parenthèse (index)
            parenthsToDelete=parenthsToDelete.union(newParenthsToDelete) #on définit les parenthèses à supprimer comme étant celles qu'il fallais déjà supprimer auxquelles on ajoute les nouvelles au moyen d'une union d'ensembles.

    
    indexsToRemove=[]#on va enregistrer chaque index des caractères du texte original à supprimer, par exemple si notre texte est "(123()678)" et que l'on veut enlever toutes le parenthèses, il faudra mettre dans la liste [0,4,5,9]
    
    for parenthIndex in parenthsToDelete:#pour chaque index de parenthèse à supprimer
        indexsToRemove.append(OpenIndexofParenths[parenthIndex]) #on rajoute à notre liste l'index où la parenthèse s'ouvre 
        indexsToRemove.append(CloseIndexofParenths[parenthIndex])#on rajoute à notre liste l'index où la parenthèse se ferme
    editedText=""#on définit 'édited text' comme étant une chain de caractères vide
    for charIndex in range(len(text)): # pour chaque index de caractère dans le texte
        if charIndex not in indexsToRemove: #si l'index n'est pas parmi ceux à supprimer
            editedText+=text[charIndex] #on rajoute le caractère à notre nouveau texte
    #ainsi notre texte est composé uniquement des caractères qui n'étaient pas à supprimer

    return editedText #on retourne le texte édité

def ignoreParenths(text):#fonction qui ignore le contenu dans les parenthèses par exemple pour "2*(xxxxxxxxxxx)+12x"renvoie "2*+12x"
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
                print("impossible d'interpréter la fonction!#278")
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

def textToPythonInterpretable(text,library=None):
    text=standardizeFunc(text)
    text=text.replace("^","**")
    if(library=="mpmath"):
        for nameIndex in range(len(BasicFunctionsNames)):
            text=text.replace(BasicFunctionsNames[nameIndex],mpMathFunctionNames[nameIndex])
    if(library=="numpy"):
        for nameIndex in range(len(BasicFunctionsNames)):
            text=text.replace(BasicFunctionsNames[nameIndex],numpyFunctionNames[nameIndex])

    return text


def getRandomFunc(maxDepth=10,depth=0,constFunc=lambda:random()*200-100):
    if(depth==maxDepth):
        FuncType="const"
    else:
        FuncType=FuncTypes[randrange(0,len(FuncTypes))]
    if(FuncType=="const"):
        FuncVars=constFunc()
        return Function(FuncType,FuncVars)
    if(FuncType=="x"):
        FuncVars=None
        return Function(FuncType,FuncVars)
    if(FuncType in BasicFunctionsNames):
        FuncVars=getRandomFunc(maxDepth,depth+1,constFunc)
        return Function(FuncType,FuncVars)
    FuncVars=[]
    for _ in range(randrange(2,6)):
        FuncVars.append(getRandomFunc(maxDepth,depth+1,constFunc))
    return Function(FuncType,FuncVars)

