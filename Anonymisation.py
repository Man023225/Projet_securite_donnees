import cryptocode
import re
from faker import Faker
import datetime
import numpy as np
from ipywidgets import interact

options = [
    "Hachage", 
    "Masquage de mot(s)", 
    "Masquage des chiffres",
    "Randomisation", 
    "Substitution/Pseudonomisation", 
    "Substitution nom de personnes",
    "Suppression", 
    "Date substitution", 
    "Date Généralisation"
    ]

"""
Ce fichier est une bibliothèque Python qui permet d'encoder du texte contenu dans une variable de type string (mot, groupe de mots, paragraphe, etc.) ainsi que le contenu d'un fichier texte d'extension .txt.
Si vous voulez anonymiser un fichier texte, il vous faudra entrer en argument le chemin d'accès du fichier. 
Il faut aussi choisi la méthode d'anomysation des données parmi les méthodes suivantes : 
- "Hachage" : Il permet de faire du hachage du contenu entré en argument de type "CH-1234".
- "Masquage des chiffres"  : Il permet de masquer les chiffres du texte à encrypter en les remplaçant par "X".
- "Masquage de mot(s)" : Il permet de substituer des mots par "X". 
- "Randomisation" : Il permet de remplacer des nombres par d'autres nombres générés aléatoirement.
- "Substitution/Pseudonomisation" : A partir d'un dictionnaire entré en argument il remplace des valeurs clés par sa valeur.
- "Substitution nom de personnes" : Elle consiste à remplacer le nom d’une personne ou d’une liste de noms de personnes entré en argument. Elle peut être appliquée pour des noms autres que ceux de personnes ou des chiffres mais ramènera systématiquement le nom d’une personne. Pour cette fonction, il faudra faire attention de ne pas mettre de signe de ponctuation « ; » à la fin de la séquence de noms au risque que la fonction remplace la chaine de caractères vide ‘’’’ par des noms comme on peut le voir dans le deuxième exemple.
- "Suppression" : Il supprime les éléments rentrés dans une liste par l'utilisateur du texte à encrypter.
- "Date substitution" : Ce code permet de remplacer des dates de formats jour.mois.année, jour/mois/année, jour-mois-année et mois-jour-année, mois/jour/année, mois.jour.année en renvoyant l'année par une date aléatoire.
- "Date Généralisation" : Ce code permet de généraliser des dates de formats jour.mois.année, jour/mois/année, jour-mois-année et mois-jour-année, mois/jour/année, mois.jour.année en renvoyant l'année.

En cochant, la case txt, la variable « txt » prend la valeur True. Si la valeur True est renseigné, le texte entré dans la varaible « input_inf » est considéré comme un chemin d’accès. Il faut que le fichier texte soit trouvé dans le même dossier que le fichier de la bibliothèque pour la procédure d’anonymisation du fichier d’extension .txt fonctionne correctement. On ne peut traiter qu’un seul fichier à la fois.

"""

fake = Faker(locale = "fr_FR")


## Liste des méthodes à implémenter : "Hachage", "Masquage", "Randomisation", "Substitution/Pseudonomisation", "Suppression", "Date substitution", "Date Généralisation"

def cryptage(input_inf = "Maison 225 01/01/2000", method = "Randomisation", txt = False, substituts = "") :

    if (method == "Substitution/Pseudonomisation") :
        if substituts == "":
            print("Vous devez remplir l'objet substitut.")
        else:
            try :
                substituts_1 = substituts
                substituts_1 = substituts_1.split(";")
                substituts = dict()
                for sub in substituts_1:
                    values = sub.split(":")
                    substituts[values[0]] = values[1]
            except:
                print("Vous n'avez pas correctement rempli le champ substituts. Veuillez vous référez à la documentation pour plus de détails.")

    if (method == "Masquage de mot(s)") | (method == "Suppression") | (method == "Substitution nom de personnes") :
        if substituts == "":
            print("Vous devez remplir l'objet substitut.")
        else:
            try :
                substituts =  substituts.split(";")

            except:
                print("Vous n'avez pas correctement rempli le champ substituts. Veuillez vous référez à la documentation pour plus de détails.")


    if txt == True:
        try:
            with open(input_inf, 'r') as fichier:
                # Lire le contenu du fichier
                name = input_inf
                input_inf = fichier.read()

        except:
            print(f"Il n'y a pas de fichier {input_inf} à l'adresse que vous avez entrée. Veuillez vérifer le chemin d'accès")

    # Hachage
    if method == "Hachage" :
        input_encoded = cryptocode.encrypt("CH-1234", input_inf)


    # Masquage des données de mot(s)
    if method == "Masquage de mot(s)" : 
        for value in substituts:
            input_inf = input_inf.replace(value, "X" * len(value))
        input_encoded = input_inf

    # Masquage des données
    if method == "Masquage des chiffres" : 
        input_encoded = re.sub(r"\d", "X", input_inf)


    # Randomisation
    if method == "Randomisation" :
        pattern = re.compile("\d+")
        remplace = pattern.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                input_inf = input_inf.replace(value, str(np.random.randint(10**(len(value)-1), 10**len(value))))
        input_encoded = input_inf
        

    # Substitution/Pseudonomisation
    if method == "Substitution/Pseudonomisation" :
        for key in substituts:
            input_inf = input_inf.replace(key, substituts[key])      
        input_encoded = input_inf


    # Substitution nom de personnes
    if method == "Substitution nom de personnes" :
        for value in substituts:
            input_inf = input_inf.replace(value, fake.name())
        input_encoded = input_inf  
            

    # Suppression
    if method == "Suppression" :
        for value in substituts:
            input_inf = input_inf.replace(value, "")  
        input_encoded = input_inf


    # Date substitution
    if method == "Date substitution" :
        ## Reconnaitre le format date:
        dmydot = re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}")
        dmybar = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")
        dmybar2 = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")
        
        remplace = dmydot.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = fake.date_between_dates(date_start= datetime.datetime(1998, 4, 27, 7, 18, 46, 476697), date_end= datetime.datetime(2020, 4, 27, 7, 18, 46, 476697))
                input_inf = input_inf.replace(value, date.strftime("%d.%m.%Y"))

        remplace = dmybar.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = fake.date_between_dates(date_start= datetime.datetime(1998, 4, 27, 7, 18, 46, 476697), date_end= datetime.datetime(2020, 4, 27, 7, 18, 46, 476697))
                input_inf = input_inf.replace(value, date.strftime("%d/%m/%Y")) 

        remplace = dmybar2.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = fake.date_between_dates(date_start= datetime.datetime(1998, 4, 27, 7, 18, 46, 476697), date_end= datetime.datetime(2020, 4, 27, 7, 18, 46, 476697))
                input_inf = input_inf.replace(value, date.strftime("%d-%m-%Y"))  

        input_encoded = input_inf
        

    # Date Généralisation
    if method == "Date Généralisation" :
        ## Reconnaitre le format date:
        dmydot = re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}")
        dmybar = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")
        dmybar2 = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")
        
        remplace = dmydot.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = datetime.datetime.strptime(value, "%d.%m.%Y")
                input_inf = input_inf.replace(value, str(date.year))

        remplace = dmybar.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = datetime.datetime.strptime(value, "%d/%m/%Y")
                input_inf = input_inf.replace(value, str(date.year)) 

        remplace = dmybar2.findall(input_inf)
        if len(remplace) != 0:
            for value in remplace:
                date = datetime.datetime.strptime(value, "%d-%m-%Y")
                input_inf = input_inf.replace(value, str(date.year)) 

        input_encoded = input_inf

    ## Mise en place de la sortie
    if txt == True:
        name = name[:-4] + "_encrypt.txt"
        with open(name, 'w') as fichier:
            # Écriture de texte dans le fichier
            fichier.write(input_encoded)
            print(f"Un fichier encrypté a été créé dans le répertoire avec le nom :{name}")
    return input_encoded
