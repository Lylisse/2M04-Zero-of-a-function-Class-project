
class Function:
    def __init__(self,atype,funcVars):
        self.type=atype # "+","*","/","^","sin","cos","tan","const","x" 
        self.vars=funcVars # une chaine contenant les variables de la fonction 
        #(par exemple pour 5x + 13 on a vars=[5x,13] et type="+")
    def __str__(self):
        if(self.type=="x"):
            return "x"
        elif(self.type=="const"):
            return str(self.vars)
        elif(self.type=="+"):
            returnText=""
            for aFunc in self.vars:
                returnText+=str(aFunc)
                returnText+="+"
            return "("+returnText[:-1]+")"
        elif(self.type=="*"):
            returnText=""
            for aFunc in self.vars:
                returnText+=str(aFunc)
                returnText+="*"
            return "("+returnText[:-1]+")"
        elif(self.type=="/"):
            returnText=""
            for aFunc in self.vars:
                returnText+=str(aFunc)
                returnText+="/"
            return "("+returnText[:-1]+")"
        elif(self.type=="^"):
            returnText=""
            for aFunc in self.vars:
                returnText+=str(aFunc)
                returnText+="^"
            return "("+returnText[:-1]+")"
        elif(self.type=="sin"):
            return "sin("+str(self.vars)+")"
        elif(self.type=="cos"):
            return "cos("+str(self.vars)+")"
        elif(self.type=="tan"):
            return "tan("+str(self.vars)+")"

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
    return newText



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
    elif(text[0]=="("and text[-1]==")"):
        parenthIndex=1
        for char in text[1:-1]:
            if char==")" and parenthIndex==1:
                print("impossible d'interpréter la fonction!")
            else:
                if char=="(":
                    parenthIndex+=1
                elif char==")":
                    parenthIndex-=1
        return textToFunc(text[1:-1])
    elif(referenceText=="sin"):
        return Function("sin",textToFunc(text[4:-1]))
    elif(referenceText=="cos"):
        return Function("cos",textToFunc(text[4:-1]))
    elif(referenceText=="tan"):
        return Function("tan",textToFunc(text[4:-1]))
    else:
        try:
            return Function("const",float(text))
        except:
            print("impossible d'interpréter la fonction!")


while True:
    print(textToFunc(input()))


def FindZeroOfFunc(func):
    return
