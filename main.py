
class Function:
    def __init__(self,atype,funcVars):
        self.type=atype # "+","*","/","^","sin","cos","tan","const","x" 
        self.vars=funcVars # une chaine contenant les variables de la fonction 
        #(par exemple pour 5x + 13 on a vars=[5x,13] et type="+")
    def __str__(self):
        return SimplifyEasyParenth(self.toString())
    def toString(self):
        if(self.type=="x"):
            return "x"
        elif(self.type=="const"):
            return str(self.vars)
        elif(self.type=="+"):
            returnText=""
            for aFunc in self.vars:
                returnText+=aFunc.toString()
                returnText+="+"
            return "("+returnText[:-1]+")"
        elif(self.type=="*"):
            returnText=""
            for aFunc in self.vars:
                returnText+=aFunc.toString()
                returnText+="*"
            return "("+returnText[:-1]+")"
        elif(self.type=="/"):
            returnText=""
            for aFunc in self.vars:
                returnText+=aFunc.toString()
                returnText+="/"
            return "("+returnText[:-1]+")"
        elif(self.type=="^"):
            returnText=""
            for aFunc in self.vars:
                returnText+=aFunc.toString()
                returnText+="^"
            return "("+returnText[:-1]+")"
        elif(self.type in ["sin","cos","tan","arcsin","arccos","arctan"]):
            return self.type+"("+self.vars.toString()+")"
        else:
            print("impossible to convert func to str!")
            return ""

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

def SimplifyEasyParenth(text):
    if(type(text)!=str):
        print("impossible d'interpréter la fonction!")
        return ""
        
    if(len(text)==0):
        return ""
    referenceText=""
    parenthIndex=0
    if(text[0]=="(" and text[-1]==")"):
        for char in text[1:-1]:
            if char=="(":
                parenthIndex+=1
            if parenthIndex==0:
                referenceText+=char
            if char==")":
                parenthIndex-=1
                if parenthIndex<0:
                    print("breaked!")
                    break
        else:
            return SimplifyEasyParenth(text[1:-1])

    actualParenthIndex=0
    OpenedParenths=[]
    lastOpenedParenth=-1
    recentlyParenthChange=0
    fastOpenedParenth=[]
    parenthToDelete=[]
    OpenIndexofParenth=[""]*(len(text.split("(")))
    CloseIndexofParenth=[""]*(len(text.split("(")))
    for index in range(len(text)):
        char = text[index]
        if char=="(":
            lastOpenedParenth+=1
            OpenedParenths.append(lastOpenedParenth)
            OpenIndexofParenth[lastOpenedParenth]=index
            actualParenthIndex=OpenedParenths[-1]
            if(recentlyParenthChange==1):
                fastOpenedParenth.append(lastOpenedParenth-1)
            recentlyParenthChange=1
        elif char==")":
            if(recentlyParenthChange==1):
                parenthToDelete.append(lastOpenedParenth)
            elif(recentlyParenthChange==-1 and actualParenthIndex in fastOpenedParenth):
                parenthToDelete.append(actualParenthIndex)
            recentlyParenthChange=-1
            CloseIndexofParenth[OpenedParenths[-1]]=index
            OpenedParenths.pop()
            if(OpenedParenths!=[]):
                actualParenthIndex=OpenedParenths[-1]
            else:
                actualParenthIndex=-1
        else:
            recentlyParenthChange=0
    indexsToRemove=[]
    for parenthIndex in parenthToDelete:
        indexsToRemove.append(OpenIndexofParenth[parenthIndex])
        indexsToRemove.append(CloseIndexofParenth[parenthIndex])
    returnValue=""
    for index in range(len(text)):
        if index not in indexsToRemove:
            returnValue=returnValue+text[index]
    return returnValue


def textToFunc(text):
    text=standardizeFunc(text)
    textbit=""
    splittedText=[]
    referenceText=""
    parenthIndex=0
    for char in text:
        if char=="(":
            parenthIndex+=1
        if parenthIndex==0:
            referenceText+=char
        if char==")":
            parenthIndex-=1
    print(referenceText)
    if(text=="x"):
        return Function("x",[])
    elif(referenceText.find("+")!=-1):
        parenthIndex=0
        for char in text:
            if char=="+" and parenthIndex==0:
                splittedText.append(textbit)
                textbit=""
            else:
                textbit+=char
                if char=="(":
                    parenthIndex+=1
                elif char==")":
                    parenthIndex-=1
        splittedText.append(textbit)
        return Function("+",[textToFunc(atext) for atext in splittedText])
    elif(referenceText.find("*")!=-1):
        parenthIndex=0
        for char in text:
            if char=="*" and parenthIndex==0:
                splittedText.append(textbit)
                textbit=""
            else:
                textbit+=char
                if char=="(":
                    parenthIndex+=1
                elif char==")":
                    parenthIndex-=1
        splittedText.append(textbit)

        return Function("*",[textToFunc(atext) for atext in splittedText])
    elif(referenceText.find("/")!=-1):
        parenthIndex=0
        for char in text:
            if char=="/" and parenthIndex==0:
                splittedText.append(textbit)
                textbit=""
            else:
                textbit+=char
                if char=="(":
                    parenthIndex+=1
                elif char==")":
                    parenthIndex-=1
        splittedText.append(textbit)

        return Function("/",[textToFunc(atext) for atext in splittedText])
    elif(referenceText.find("^")!=-1):
        parenthIndex=0
        for char in text:
            if char=="^" and parenthIndex==0:
                splittedText.append(textbit)
                textbit=""
            else:
                textbit+=char
                if char=="(":
                    parenthIndex+=1
                elif char==")":
                    parenthIndex-=1
        splittedText.append(textbit)

        return Function("^",[textToFunc(atext) for atext in splittedText])
    elif(referenceText in ["sin","cos","tan","arcsin","arccos","arctan"]):
        return Function(referenceText,textToFunc(text[len(referenceText)+1:-1]))
    else:
        if text.isdigit():
            return Function("const",int(text))
        else:
            try:
                return Function("const",float(text))
            except:
                print("impossible d'interpréter la fonction!")
                return ""


while True:
    print(textToFunc(input()))


def FindZeroOfFunc(func):
    return
