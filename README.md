# Steganographie
 
Simple projet python permettant d'encoder du texte dans une image bmp 24 bits
Différents paramètres sont disponibles dans l'interface graphique **steganographe_ui.py**
La bibliothèque **pystega.py** contient 4 fonctions:
Img(path) : retourne un objet image PIL contenant l'image dont le chemin est spécifié.
encode(funcimage,text,xyinvert=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8) : encode le texte **text** dans l'image funcimage en respectant les paramètres donnés
check(funcimage,xyinvert=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8) : vérifie la présence de texte dans l'image selon les indications données
decode(funcimage,xyinvert=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8) : décode le texte de l'image funcimage selon les indications données si la fonction check est vérifiée

**Plus de détails dans pystega.py**

## Dépendances:
Python 3.8+
PILow

## Exemples:
### Original:
![Original](exemple/python.bmp)
### Final:
encodé avec les paramètres par défaut et contenant le début de ce Readme:
![Final](exemple/pythonfinal.bmp)
