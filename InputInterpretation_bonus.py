from copy import deepcopy
from random import *
import mpmath as mp
import numpy as np

FuncTypes=["-","+","*","/","^","sin","cos","tan","const","x","ln","exp","arcsin","arccos","arctan"]
BasicFunctionsNames=["sin","cos","tan","arcsin","arccos","arctan","exp","ln"]
BasicFunctionsNamesInverted=["arcsin","arccos","arctan","sin","cos","tan","ln","exp"] #pour chaque nom de fonction cette liste contient son opposé, selon son index, par exemple BasicFunctionsNames[2]=tan et BasicFunctionsNamesInverted[2]=arctan; son inverse
mpMathFunctionNames=["mp.sin","mp.cos","mp.tan","mp.asin","mp.acos","mp.atan","mp.exp","mp.ln"]
numpyFunctionNames=["np.sin","np.cos","np.tan","np.arcsin","np.arccos","np.arctan","np.exp","np.log"]
FuncStr="sincostanarccosarctanexpln"
operatorStr="-+*/^"
class Function: #on définit les propriétés de l'object fonction
    def __init__(self,atype,funcVars):
        self.type=atype # on définit le type de fonction parmi ces types"+","*","/","^","sin","cos","tan","const","x","ln","exp","arcsin","arccos","arctan"
        self.vars=funcVars # une chaine contenant les variables de la fonction, à noter que les fonction de type x n'en ont pas
        #(par exemple pour 5x + 13 on a vars=[5x,13] et type="+")
        if(atype in ["+","/","^","-","*"] and len(funcVars)<2):
            print("invalid number of args!",atype)# il faut au moins deux variable pour définire une addition, division, etc...
    def __str__(self):#on définit ce qu'il va arriver lorsque on utilise la fonction str(<notre object fonction>) dans le code
        return SimplifyEasyParenth(self.toString())#on retourne la fonction en la transformant en une chaine de caractère (avec la fonction qu'on définit juste après) et on utilise la fonction qui simplifie les parenthèses pour que ça soit propre
    
    def __mul__(self, other):# ici on definit la multiplication à droite et à gauche example "2*x" a droite et "x*2" a gauche
        if(type(other)==int or type(other)== float):
            other=Function("const", other)#si on a utilisé un nombre dans la multiplication, on le convertit en fonction constante
        return Function("*",[self,other])
    def __rmul__(self, other):# on definit la multiplication à droite 
        if(type(other)==int or type(other)== float):
            other=Function("const", other)#si on a utilisé un nombre dans la multiplication, on le convertit en fonction constante
        return Function("*",[other,self])
    
    def __truediv__(self, other):# on definit la division
        if(type(other)==int or type(other)== float):#si on a utilisé un nombre de l'autre côté de la division, on le convertit en fonction constante
            other=Function("const", other)
        return Function("/",[self,other])
    def __rtruediv__(self, other):# on definit la division à droite
        if(type(other)==int or type(other)== float):#si on a utilisé un nombre de l'autre côté de la division, on le convertit en fonction constante
            other=Function("const", other)
        return Function("/",[other,self])
    
    def __add__(self, other):#ici on definit l'addition
        if(type(other)==int or type(other)== float):#si on a utilisé un nombre de l'autre côté de l'addition, on le convertit en fonction constante
            other=Function("const", other)
        return simplifyUselessSubFuncs(Function("+",[self,other]))
    def __radd__(self, other):#ici on definit l'addition
        if(type(other)==int or type(other)== float):#si on a utilisé un nombre de l'autre côté de l'addition, on le convertit en fonction constante
            other=Function("const", other)
        return simplifyUselessSubFuncs(Function("+",[other,self]))
    
    def __sub__(self, other):# ici on definit la soustraction
        if(type(other)==int or type(other)== float):#si on a utilisé un nombre de l'autre côté de la soustraction, on le convertit en fonction constante
            other=Function("const", other)
        return Function("-",[self,other])
    def __rsub__(self, other):# ici on definit la soustraction
        if(type(other)==int or type(other)== float): #si on a utilisé un nombre de l'autre côté de la soustraction, on le convertit en fonction constante
            other=Function("const", other)
        return Function("-",[other,self])
    
    def __pow__(self, other):# ici on definit la puissance
        if(type(other)==int or type(other)== float): #si on a utilisé un nombre de l'autre côté de la puissance, on le convertit en fonction constante
            other=Function("const", other)
        return Function("^",[self,other])
    def __rpow__(self, other):# ici on definit la puissance
        if(type(other)==int or type(other)== float): #si on a utilisé un nombre de l'autre côté de la puissance, on le convertit en fonction constante
            other=Function("const", other)
        return Function("^",[other,self])
    
    def __eq__(self,other):#on définit la valeur à retourner lorsque l'on compare deux fonctions en utilisant "==" par exemple ( cf(1)==cf(2) ) = False, on essaie de pouvoir repondre par True le plus possible, mais l'important est de ne jamais répondre True si elle ne sont pas égales.
        if(not isinstance(other,Function)): #si l'autre element (other) n'est pas un objet fonction alors on retourne False
            return False
        if(self.type!=other.type): #si les deux types de fonctions ne sont pas égales alors on retourne Faux
            return False
        if(self.type=="x" and other.type=="x"): #si les deux sont de type x on retourne True car ce sont les mêmes fonctions
            return True
        if(isinstance(self.vars,list) and isinstance(other.vars,list)):#si les variables des deux fonctions sont des listes
            if(self.type in ["*","+"]): #si ce sont des fonctions commutatives
                for var in self.vars:
                    if var not in other.vars: #si il y a une variable d'une fonction qui n'est pas variable de l'autre alors ce sont deux fonctions différentes
                        return False
                for var in other.vars:
                    if var not in self.vars:#si il y a une variable d'une fonction qui n'est pas variable de l'autre alors ce sont deux fonctions différentes
                        return False
            elif(self.type in ["-","/","^"]):#si ce sont des fonction partiellement commutatives (par ex: a-b-c = a-c-b != b-a-c)
                if(self.vars[0]!=other.vars[0]):#si leur première variable n'est pas la même alors ce sont des fonctions différentes
                    return False
                for var in self.vars[1:]:
                    if var not in other.vars[1:]:#si il y a une variable d'une fonction qui n'est pas variable de l'autre en excluant leurs premières variables alors ce sont deux fonctions différentes
                        return False
                for var in other.vars[1:]:
                    if var not in self.vars[1:]:#si il y a une variable d'une fonction qui n'est pas variable de l'autre en excluant leurs premières variables alors ce sont deux fonctions différentes
                        return False
        elif(self.vars!=other.vars):#si la variable des fonctions n'est pas une liste alors il suffit de regarder si leur variable est identique
            return False
        return True
    def deepcopy(self):
        return deepcopy(self)#fonction servant à retourner une copie de la fonction qui soit totalement détaché d'elle, car par exemple si on fait var1=cf(0), var2=var1, var2.vars=1 alors on aura aussi 1=var1.vars au lieu de 0 car lorsqu'on utilise var2=var1 les deux variables "stockent" ou "pointent" vers le même objet fonction, pour ne pas avoir se problème on utilisera var2 = var1.deepcopy()
    def toString(self):#fonction qui retourne une chaine de caractères pour une fonction, à noter que ce n'est pas la fonction qui sera appelée directement par str(<objet Function>)
        if(self.type=="x"):
            return "x" #si la fonction est de type "x" on retourne "x"; trivial
        elif(self.type=="const"): #si la fonction est constante
            return str(self.vars)#on retourne sa variable qui contient un nombre en le transformant en chaine de caractères avec str()
        elif(self.type in ["-","+","*","/","^"]):#si la fonction est un opérateur "&" et que ses variables sont [a,b,c,d] alors on retourne a.toString()+ "&" + b.toString()+ "&" + c.toString()+ "&" + d.toString()
            returnText=""
            for aFunc in self.vars: #pour chaque fonction (aFunc) parmi les variables de notre fonction (self)
                returnText+=aFunc.toString()#on rajoute aFunc.toString()
                returnText+=self.type#on rajoute le type de la fonction qui est normalement un des opérateurs "-","+","*","/","^"
            return "("+returnText[:-1]+")"#on met la fonction entre parenthèses car on est peut-être dans le cas (a + b) * c où les parenthèses sont importantes
        elif(self.type in BasicFunctionsNames):# si le type de la fonction est parmi les fonction basiques ("sin","cos","tan","arcsin","arccos","arctan","exp","ln") alors on retourne: le nom de la fonction(type)+"("+ sa variable en chaine de caractères+")", cela donnera par exemple "ln" +"("+"x"+")"= "ln(x)"
            return self.type+"("+self.vars.toString()+")"
        else:#si le type de fonction n'est pas parmi ceux ci-dessus on ne sait pas comment convertir la fonction en chaine de caractères
            print("impossible to convert func to str!")
            return ""
        
    def getValue(self,n):#fonction qui retournera la valeur de la fonction en n, par exemple si notre fonction f est x+1 alors f.getValue(2)=3
        if(self.type=="x"):
            return n
        elif(self.type=="const"):
            return self.vars
        elif(self.type =="+"):
            returnValue=0
            for aVar in self.vars:
                if(aVar.getValue(n)==None):
                    return None
                returnValue+=aVar.getValue(n)
            return returnValue
        elif(self.type =="-"):
            if(self.vars[0].getValue(n)==None):
                return None
            returnValue=self.vars[0].getValue(n)
            for aVar in self.vars[1:]:
                if(aVar.getValue(n)==None):
                    return None
                returnValue-=aVar.getValue(n)
            return returnValue
        elif(self.type =="*"):
            returnValue=1
            for aVar in self.vars:
                if(aVar.getValue(n)==None):
                    return None
                returnValue*=aVar.getValue(n)
            return returnValue
        elif(self.type =="/"):
            if(self.vars[0].getValue(n)==None):
                return None
            returnValue=self.vars[0].getValue(n)
            for aVar in self.vars[1:]:
                if(aVar==0):
                    return None
                if(aVar.getValue(n) in [None,0]):
                    return None
                returnValue/=aVar.getValue(n)
            return returnValue
        elif(self.type =="^"):
            if(self.vars[0].getValue(n)==None):
                return None
            returnValue=self.vars[0].getValue(n)
            for aVar in self.vars[1:]:
                if(aVar.getValue(n)==None):
                    return None
                if(returnValue==0 and aVar.getValue(n)<0):
                    return None
                returnValue**=aVar.getValue(n)
            return returnValue
        elif(self.type in BasicFunctionsNames):
            index=BasicFunctionsNames.index(self.type)
            if(self.vars.getValue(n)==None):
                return None
            try:
                return eval(numpyFunctionNames[index]+f"({self.vars.getValue(n)})")
            except:
                #print("exception! l.169", numpyFunctionNames[index]+f"({self.vars.getValue(n)})")
                return None


        
        
def cf(number): #on définit la fonction cf pour constant Func (fonction constante) qui nous servira à initialiser plus facilement une fonction constante
    return Function("const",number)

def getCharTypes(text): 
    """fonction qui retourne une liste décrivant le type de caractères d'un texte donné, cette fonction est utilisée pour interpréter des fonctions sous forme de texte et plus précisément pour pouvoir définir la priorité des opération par exemple pour 2x^2x on veut avoir 2*x^(2*x) pour cela on doit savoir que le 2 et le x sont "collés". Pour cela il y a 6 types de caractères différents:
"(",")","var","numb","func","operator"   """

    charTypesArray=[]
    for index in range(len(text)):#pour chaque index de caractère du texte
        char=text[index]
        if(char==")"):
            charTypesArray.append(")")#si le caractère est ")" son type est ")" (trivial)
        elif(char=="("):
            charTypesArray.append("(")#si le caractère est "(" son type est "(" (trivial)
        elif(char=="x"): #si le caractère est "x" son type est "var" car c'est une variable sauf si c'est le x de "exp" de ce cas il est de type "func"
            if(index!=0 and text[index-1]=="e"):
                charTypesArray.append("func")
            else:
                charTypesArray.append("var")
        elif(char.isnumeric() or char=="."):
            charTypesArray.append("numb")#si le caractère est numérique ou bien si c'est un point c'est un nombre, ainsi tous les caractères de "42.69" sont de type "numb"
        elif(char in FuncStr):#si le caractère fait partie des caractères de fonction alors il est de type "func"
            charTypesArray.append("func")
        elif(char in operatorStr):#si le caractère fait partie des caractères d'opérateur ("+-*/^") alors il est de type "operator"
            charTypesArray.append("operator")
        else:
            raise Exception("texte invalide!")#si le caractère n'est rien de tout cela, le texte est invalide; il ne décrit pas une fonction
    return charTypesArray

def getParenthEndIndex(text):#fonction qui nous donne le moment oû les parenthèses se ferment pour des textes qui commencent par une ouverture de parenthèse par exemple pour "(123(567)(012))(678)" elle retourne 14
    if(text[0]!="("):
        print("wrong input") #si le texte ne commence pas par une ouverture de parenthèse, le texte est invalide

    parenthDepth=1#on utilise une variable pour enregistrer la "profondeur" de parenthèse dans laquelle on est, par exemple (ici la profondeur est 1(ici 2(ici 3(ici 4, en fait c'est simplement le nombre de parenthèses qu'il me reste à fermer: 4)3)2)1)0
    charIndex=0#on définit l'index de caractère du texte
    while parenthDepth!=0:#tant que l'on est pas sorti de toutes les parenthèses (quand la profondeur est 0 c'est que c'est le cas)
        charIndex +=1#on passe au prochain caractère; charIndex commencera en étant 1 et non 0 car on sait que le premier caractère est "(" c'est aussi pour cela qu'on commence avec parenthDepth=1
        if(charIndex==len(text)):#si on a atteind la fin du texte et que l'on est toujours pas sorti de nos parenthèses c'est que le texte était invalide
            print("invalid input!")
        if(text[charIndex]=="("):#si le caractère correspondant ouvre une parenthèse il faut incrémenter parenthDepth car on s'enfonce dans les parenthèses 
            parenthDepth+=1
        if(text[charIndex]==")"):#si le caractère correspondant ferme une parenthèse il faut soustraire 1 à parenthDepth car on sort des parenthèses 
            parenthDepth-=1

    return charIndex # on retourne l'index qui nous a permis de sortir de toute nos parenthèses
        

def getLenOfMult(text, charTypes):#fonction qui donne la longueur d'une multiplication abrégée à partir du début d'un texte en fonction des types de caractères et du texte en question, par exemple pour "0x(3+56)*9" il renvoie 8 car après le "*" ce n'est plus une forme abrégée et que "0x(3+56)" contient 8 caractères
    charIndex=0 #on commence au début du texte en prenant comme index de caractère 0
    while charIndex<len(text) and charTypes[charIndex] not in ["operator",")"] : #tant que notre index de caractère est inférieur à la longueur du texte on est encore dans le texte, et on vérifie que le caractère sélectionné ne soit pas un opérateur ou une fin de parenthèse car cela mettrait fin à la séquence en effet pour "2x)x+2" on doit renvoyer 2 et non pas 4 
        if(charTypes[charIndex]=="("):#si le caractère est une ouverture de parenthèse alors ce qu'il se passe dans la parenthèse ne nous interresse pas en effet pour "(1x+45)7+8" on retournera 8 car "(1x+45)7" est de longueur 8
            charIndex = charIndex + getParenthEndIndex(text[charIndex:]) # pour cela on va donc regarder à quel index se ferme la parenthèse qui s'ouvre sur notre index (char index) et on va "déplacer" l'index à cette position. Par exemple si le texte est "0+2x(56+8)0*2": lorque charIndex=4 on remarque que la parenthèse s'ouvre, elle se referme 5 caractères après en 4+5=9
        charIndex+=1 #on passe au prochain index de caractère
    return charIndex #lorsque la multiplication abrégée se termine on retourne l'index du caractère qui nous donnera la longueur de la multiplication, par exemple pour "0x(34+6)8*0" la multiplication abrégée se termine en 9 qui nous donne la longueur en caractères de la multiplication. 


def addUsefullParenths(initialText,triggerChar): 
    """fonction qui va rajouter des parenthèses lorsque elles sont utiles, par exemple pour 2^2x on veut 2^(2x) et non pas (2^2)x, pareil pour "2/2x", pour cela on a besoin d'un caractère déclencheur (trigger char) à partir du quel on va rajouter des parenthèses (ce sera normalement soit "^" soit "/")
    À noter que 2^2sin(x) donnera 2^(2sin(x)) et que 2^2(x+1) donnera 2^(2(x+1))"""
    
    chartypes=getCharTypes(initialText) #on utilise getCharTypes pour obtenir les types de caractères de notre texte, par exemple pour "2^2x" on aura ["numb","operator","numb","var"] (var est l'abréviation de variable)
    newText="" #on définit le nouveau texte comme étant une chaine de caractères vide
    lastTermEndIndex=0 #lastTermEndIndex stocke l'index où s'est terminé le dernier terme, par exemple pour "0*2^4x+7^x", si triggerchar est '^', lastTermEndIndex sera d'abord 0 puis 5 puis 9 les termes respectifs seront "", "4x", "x". 
    termStartIndex=initialText.find(triggerChar)#termStartIndex sera à chaque fois l'index de triggerchar, le caractère "déclencheur", par exemple dans "0^2+4^6" si triggerChar est '^' il sera 1 puis 5 puis -1 pour signifier qu'il ne reste plus de '^' dans le texte, à noter que l'index pointe vers le caractère déclencheur, donc le terme commencera sur termStartIndex+1
    while termStartIndex !=-1:#tant que termStartIndex n'est pas -1 cela veut dire que il y a encore des priorités d'opérations à faire valoir
        newText+=initialText[lastTermEndIndex:termStartIndex+1]#on rajoute dans le nouveau texte tout ce qui est entre la fin du dernier terme et le début du nouveau
        multLen=getLenOfMult(initialText[termStartIndex+1:],chartypes[termStartIndex+1:])#on enregistre dans la variable "multLen" la longueur du terme, par exemple si on a "2^xsin(x)" cela nous donnera 7 car "xsin(x)" est de longueur 7
        if(multLen!=0):#si la longueur du terme n'est pas nulle (ce qui devrait toujours être le cas car sinon cela voudrait dire que notre texte est par exemple "2^+" ou "(2/)"  (avec triggerchar "^" et "/" respectivement)
            newText+="("+initialText[termStartIndex+1:termStartIndex+multLen+1]+")"#on rajoute le terme en l'entourant de parenthèses
        lastTermEndIndex=termStartIndex+1+multLen#on enregistre lastTermEndIndex comme étant l'index de début de terme (on rappelle que c'est termStartIndex+1 car termStartIndex pointe sur le triggerChar) plus la longueur du terme. Cela nous donne l'index du charactère suivant la fin du terme, par exemple dans "2^2x+1" le début du terme est le "^" qui est en 1, la longueur du terme "2x" est de 2 ainsi on a 1+1+2= 4 qui est l'index du "+" dans "2^2x+1"
        if(initialText[lastTermEndIndex:].find(triggerChar)!=-1):#si on trouve le charactère déclencheur (triggerChar) dans ce qui reste du texte. ( text.find(char) renvoie -1 si char n'a pas été trouvé dans le texte) 
            termStartIndex=initialText[lastTermEndIndex:].find(triggerChar)+lastTermEndIndex#alors on définit termStartIndex comme étant l'index de triggerChar, par exemple si notre texte initial est "1^2x+3^4x" et que triggerchar="^" on cherche dans "+3^4x" on trouve "^" qui est à l'index 2 auquel on rajoute 3 qui est l'index de la fin du dernier terme ("1^2x"<--ici) pour obtenir 5 qui est bien l'index du deuxième "^" dans "1^2x+3^4x"
        else:
            termStartIndex=-1#si on ne trouve pas le caractère déclencheur, on enregistre -1 dans la variable termStartIndex ce qui causera la fin de la boucle while
    newText+=initialText[lastTermEndIndex:]#on rajoute au texte ce qu'il reste depuis la fin du dernier terme, par exemple dans "0^2x+5" ce sera le "+5"
    
    return newText #on retourne le texte que l'on a généré qui aura normalement des parenthèses entourant les termes de multiplicatifs abrégés, par exemple avec "^" comme triggerChar et "2^2x^2x" comme initialText, newText sera "2^(2x)^(2x)" 


def standardizeFunc(text):#fonction qui par exemple renvoie 2*x pour 2x
    if(text==""):
        return "0"
    if(text[0]=="-"):
        text="0"+text #on rajoute un 0 devant le - pour que cela puisse être interprété comme une soustraction
    text=text.replace(" ","")#on enlève les espaces
    text=text.replace("**","^")#on remplace "**" par "^"; le symbole utilisé pour les puissances
    
    text=addUsefullParenths(text,"^")#on rajoute des parenthèses après les simboles de puissances, pour avoir par exemple 2^(2x) au lieu de 2^2x qui risquerait d'être interprété commme (2^2)*x
    text=addUsefullParenths(text,"/")#on rajoute des parenthèses après les simboles de division, pour avoir par exemple 2/(2x) au lieu de 2/2x qui risquerait d'être interprété commme (2/2)*x

    charTypesArray=getCharTypes(text)#on utilise getCharTypes pour obtenir les types de caractères de notre texte, par exemple pour "2^2x" on aura ["numb","operator","numb","var"] (var est l'abréviation de variable)
    newText=""#on initialise une variable contenant le nouveau texte, pour l'instant vide
    for charIndex in range(len(charTypesArray)-1):#pour chaque index de caractère excepté le dernier
        char = text[charIndex]#on définit la variable char comme étant le caractère à l'index donné
        charType=charTypesArray[charIndex]#on définit la variable charType comme étant le type de caractère à l'index donné (le type de notre caractère (char) en gros)
        newText+=char#on rajoute la caractère au nouveau texte
        nextCharType=charTypesArray[charIndex+1]#on définit la variable nextCharType comme étant le type de caractère qui est après le notre pour cela on utilise (charIndex+1)
        if(charType == ")" and nextCharType in ["(","var","numb","func"]):#si notre caractère est une fin de parenthèse et que le suivant est un début de parenthèse, une variable, un nombre ou une fonction, c'est qu'on est dans le cas "....)sin..." "....)x..." "....)n..." "....)(..." et on rajoute donc un symbole de multiplication "*" pour obtenir "....)*sin..." "....)*x..." "....)*n..." "....)*(..."
            newText+="*"
        if(charType == "var" and nextCharType in ["(","var","numb","func"]):#si notre caractère est une variable et que le suivant est un début de parenthèse, une variable, un nombre ou une fonction, c'est qu'on est dans le cas "....xsin..." "....xx..." "....xn..." "....x(..." et on rajoute donc un symbole de multiplication "*" pour obtenir "....x*sin..." "....x*x..." "....x*n..." "....x*(..."
            newText+="*"
        if(charType == "numb" and nextCharType in ["(","var","func"]):#si notre caractère est un nombre et que le suivant est un début de parenthèse, une variable ou une fonction, c'est qu'on est dans le cas "....nsin..." "....nx..." "....n(..." et on rajoute donc un symbole de multiplication "*" pour obtenir "....n*sin..." "....n*x..." "....n*(..."
            newText+="*"
    newText+= text[-1]#on rajoute à notre nouveau texte le dernier son dernier caractère
        
    return SimplifyEasyParenth(newText)#on renvoie la fonction en simplifiant les parenthèses inutiles par exemple si l'utilisateur à mis "((x+1))*2" cela nous donnera (x+1)*2


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
    for basicOperator in ["+","-","*","/","^"]:#il faut suivre la priorité des oprérations
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
                print(f"impossible d'interpréter la fonction!#278 \n{text}")
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
    text=text.replace("**","^")
    text=standardizeFunc(text)
    text=text.replace("^","**")
    if(library=="mpmath"):
        for nameIndex in range(len(BasicFunctionsNames)):
            text=text.replace(BasicFunctionsNames[nameIndex],mpMathFunctionNames[nameIndex])
    elif(library=="numpy"):
        for nameIndex in range(len(BasicFunctionsNames)):
            text=text.replace(BasicFunctionsNames[nameIndex],numpyFunctionNames[nameIndex])
    elif(library!=None):
        print("nom de librarie inconnu!")
    return text


def getRandomFunc(maxDepth=10,depth=0,constFunc=lambda:random()*200-100,types=FuncTypes):
    if(depth==maxDepth):
        FuncType="const"
    else:
        FuncType=types[randrange(0,len(types))]
    if(FuncType=="const"):
        FuncVars=constFunc()
        return Function(FuncType,FuncVars)
    if(FuncType=="x"):
        FuncVars=None
        return Function(FuncType,FuncVars)
    if(FuncType in BasicFunctionsNames):
        FuncVars=getRandomFunc(maxDepth,depth+1,constFunc,types=FuncTypes)
        return Function(FuncType,FuncVars)
    FuncVars=[]
    for _ in range(randrange(2,6)):
        FuncVars.append(getRandomFunc(maxDepth,depth+1,constFunc,types=FuncTypes))
    return Function(FuncType,FuncVars)

def getOnexRandomFunc(maxDepth=10,maxLength=5,types=["-","+","*","/","^","sin","cos","tan","const","ln","exp","arcsin","arccos","arctan"]):
    Func=Function("x",None)
    for i in range(maxDepth):
        randType = types[randrange(0,len(types))]
        while randType in ["const","x"]:
            randType = FuncTypes[randrange(0,len(FuncTypes))]
        if(randType in BasicFunctionsNames):
            Func=Function(randType,Func.deepcopy())
        else:
            randLength=randrange(2,maxLength)
            randIndex=randrange(0,randLength)
            vars=[]
            for index in range(randLength):
                if(index==randIndex):
                    vars.append(Func.deepcopy())
                else:
                    vars.append(getRandomFunc(maxDepth=i+1,types=types))
            Func=Function(randType,vars)
    return Func

