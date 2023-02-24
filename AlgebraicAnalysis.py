from InputInterpretation import *

def Derivate(aFunc):#pour un objet fonction donné, retourne l'objet fonction dérivé
    if(aFunc.type=="const"):
        return Function("const",0)# pour une constante la dérivée est 0
    elif(aFunc.type=="x"):
        return Function("const",1)# pour x la dérivée est 1
    elif(aFunc.type=="sin"):
        return Function("cos",aFunc.vars)*Derivate(aFunc.vars)#la dérivée de sin est cos
    elif(aFunc.type=="cos"):
        return -1*Function("sin",aFunc.vars)*Derivate(aFunc.vars)#la dérivée de cos est -sin
    elif(aFunc.type=="tan"):
        return Function("const",1)/(Function("cos",aFunc.vars)^2)*Derivate(aFunc.vars)#la dérivée de tan est 1/cos²
    elif(aFunc.type=="+"):
        return Function("+",[Derivate(eachFunc) for eachFunc in aFunc.vars])
    elif(aFunc.type=="*"):
        if(len(aFunc.vars)==2):
            return Derivate(aFunc.vars[0])*aFunc.vars[1]+aFunc.vars[0]*Derivate(aFunc.vars[1])#la dérivée de f+g est f'g+fg'
        else:#si il y a plusieurs termes la dérivée de f+g+h=((f+g)+h)'
            leftFunc=Function("*",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc*rightFunc)
    elif(aFunc.type=="/"):
        if(len(aFunc.vars)==2):
            return (Derivate(aFunc.vars[0])*aFunc.vars[1]-aFunc.vars[0]*Derivate(aFunc.vars[1]))/aFunc.vars[1]**2#la dérivée de f/g est f'g-fg'/g²
        else:#dérivée de f/g/h est ((f/g)/h)'
            leftFunc=Function("/",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc/rightFunc)
    elif(aFunc.type=="^"):
        if(len(aFunc.vars)==2):
            return Derivate(Function("exp",aFunc.vars[1]*Function("ln",aFunc.vars[0])))#f^g=exp(g*log(f))
        else:#f^g^h=(f^g)^h
            leftFunc=Function("^",aFunc.vars[:-1])
            rightFunc=aFunc.vars[-1]
            return Derivate(leftFunc**rightFunc)
    elif(aFunc.type=="exp"):
        return aFunc*Derivate(aFunc.vars)#dérivée de exp(x)=exp(x)
    elif(aFunc.type=="ln"):
        return Function("const",1)/aFunc.vars*Derivate(aFunc.vars)#derivee de ln(x)=1/x
    elif(aFunc.type=="arccos"):
        return Function("const",-1)/((cf(1)-Function("x",None)**cf(2)))**(cf(0.5))*Derivate(aFunc.vars) #dérivée arccos est  -1/√(1-x²)
    elif(aFunc.type=="arcsin"):
        return Function("const",1)/((cf(1)-Function("x",None)**cf(2)))**(cf(0.5))*Derivate(aFunc.vars) #dérivée arccos est  1/√(1-x²)
    elif(aFunc.type=="arctan"):
        return Function("const",1)/(cf(1)+Function("x",None)**cf(2))*Derivate(aFunc.vars) # dérivée de arctan est 1/(1+x²)

if __name__ =="__main__":
    while True:
        inputFunc=textToFunc(input())#on demande à l'utilisateur une fontion et on la traduits en objet fonction
        print(inputFunc)#on affiche l'objet fonction reçu 
        print(Derivate(inputFunc))#on calcule la dérivée et on l'affiche 
