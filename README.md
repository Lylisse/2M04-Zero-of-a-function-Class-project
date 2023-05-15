# 2M04-Zero-of-a-function-Class-project

## Description
Le projet consiste à approximer les zeros d'une fonction aussi précisément que possible.
Les librairires utilisées sont: mpmath, numpy, matplotlib, tkinter      

## Setup
Pour installer les librairies il faut utiliser pip sur le fichier requirements avec les commandes suivante:
> cd {votre path}\2M04-Zero-of-a-function-Class-project-main
> 
> pip install -r requirements.txt

## Utilisation
Pour lancer les programme il faut lancer le fichier *main* en double cliquant dessus, ou en utilisant la commande:
> cd {votre path}\2M04-Zero-of-a-function-Class-project-main
> 
> python main.py

## Guide pour lire le code
Pour éviter de rendre les noms de variables trop longs, certaines conventions ont été mises en place : 
* Une fonction dont le nom commence par "t0f" (pour "Trouver les 0 d'une Fonction") trouve les zéros d'une fonction. Elle prends comme arguments _obligatoires_: 
  * f : c'est une fonction réelle. Elle doit être donnée comme une fonction python (type "callable")
  * a : c'est un float. Il démarque le début de l'intervalle sur lequel on cherchera les zéros de f
  * b : float également. Démarque cette fois la fin de l'intervalle
  
  D'autres arguents optionels peuvent exister.
  
  La fonction commençant par "t0f" retournera une liste de zéros de la fonction.
  
* Une fonction dont le nom commence par "ti1z" (pour "trouver des intervalles avec 1 zéro") trouve des intervalles dans lesquels la fonction a exactement 1 zéro. Elle prends les mêmes arguments obligatoire que les fonction de type "t0f", et peut également prendre des arguments optionels.

  Les fonctions "ti1z" servent de fonction intermédiaire pour trouver les zéros.

* Une fonction dont le nom commence par "t0i" (pour "trouver le 0 dans l'intervalle") trouvent le zéro dans un intervalle qui n'a qu'un zéro, et qui aurait été trouvé par une fonction "ti1z". Elle prends de nouveau les arguments de la même manière que les deux types de fonctions précédentes.


## Sources
Bouton tkinter :

[TKinter tutorial](https://realpython.com/python-gui-tkinter/) , 27/02/2023

[Another TKinter tutorial](https://tkdocs.com/tutorial/firstexample.html) , 27/02/2023

[A third TKinter tutorial](https://tkdocs.com/tutorial/firstexample.html) , 27/02/2023

[Forum help for TKinter](https://stackoverflow.com/questions/46026782/changing-entry-box-background-colour-in-tkinter) , 20/03/2023

Librairies : 

[documentation numpy](https://numpy.org/doc/stable/reference/) , 15/05/2023

[documentation mpmath](https://mpmath.org/doc/current/) , 15/05/2023

[documentation matplotlib](https://matplotlib.org/stable/index.html), 15/05/2023


Méthodes pour trouver les zéros : 

[pdf contenant des idées de méthodes transmi pas M. Mroczeck](https://github.com/Lylisse/2M04-Zero-of-a-function-Class-project/files/11479282/zeros_DM.pdf)

[méthode de Halley](https://fr.wikipedia.org/wiki/Méthode_de_Halley), 15/05/2023









