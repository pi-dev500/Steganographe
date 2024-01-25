# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:29:19 2024

@author: pi-dev500

@version: 0.1.0 library api
"""
from PIL import Image
from math import ceil

class toSmallImageException(Exception):
    message="L'image donnée est trop petite. Veuillez choisir une image plus grande."
    def __init__(self):
        super().__init__(self.message)
class noTextInImageException(Exception):
    message="Ancun texte n'est encodé dans cette image suivant les options données."
    def __init__(self):
        super().__init__(self.message)
        
def Img(path):
    return Image.open(path)

def doc():
    print("""
funcimage: image utilisée par la fonction
texte    : texte encodé
xyorder  :
    Si 0 : pas d'inversion entre x et y
    Sinon: inversion entre x et y dans l'ordre de balayage des pixels
xdir     : inversion du sens de balayage des abcisses si différent de 0
ydir     : inversion du sens de balayage des ordonnées si différent de 0
rgb      : tuple selectionnant les couleurs dont les LSB sont utilisées
                ex: (1,0,1) utilise les couleurs rouges et bleues pour encoder le message
charbits : Longueur, en bits d'un caractères. Il est tres déconseillé de mettre une valeur
           en dessous de 7 si il n'y as pas d'accentuation des caratères, en dessous de 8
           si usage d'accents et autres caractères ayant une valeur ASCII supèrieure à 127
           
Fonctions:
    Img(path): Même chose que Image.open , instancie une nouvelle image ayant pour chemin path
    encode(funcimage,texte,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8)
    check(funcimage,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8): vérifie si l'image contient du texte selon les paramètres entrés
    decode(funcimage,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8): retourne le texte caché dans l'image si elle en contient
""")

def encode(funcimage,texte,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8,creturn="CR"):
    
    bits=[]
    for letter in creturn+str(texte)+creturn:
        letter=ord(letter)
        for i in range(charbits):  # Simple technique pour transformer un nombre en série LSB first
            bits.append(letter&0b1)
            letter= letter >> 1 
    
    sizex,sizey=funcimage.size
    
    if sizex*sizey<ceil(len(bits)/rgb.count(1)):
        raise toSmallImageException
    if xyorder==0: # vérification de l'inversion de l'ordre balayage x/y
        if xdir==0: # mets le range appliqué pour x en ordre croissant ou décroissant
            xrange=range(sizex)
        else:
            xrange=range(sizex-1,-1,-1)
        if ydir==0:# mets le range appliqué pour y en ordre croissant ou décroissant
            yrange=range(sizey)
        else:
            yrange=range(sizey-1,-1,-1)
    else: # ici, les ordonnées et les abcisses sont inversées, ce qui explique ces inversions étranges
        if ydir==0:# mets le range appliqué pour y en ordre croissant ou décroissant
            xrange=range(sizey)
        else:
            xrange=range(sizey-1,-1,-1)
        if xdir==0:# mets le range appliqué pour x en ordre croissant ou décroissant
            yrange=range(sizex)
        else:
            yrange=range(sizex-1,-1,-1)
    
    posbit=0 # initialisation de la variable contenant la position du bit encodé
    
    for y in yrange: # application des ranges prédéfinis pour balayer les ordonnées et abcisses
        for x in xrange:
            if xyorder==0: # une alternative simple à deux boucles différentes: juste une inversion de x et y dans le getpixel et le putpixel
                q=funcimage.getpixel((x,y))
            else:
                q=funcimage.getpixel((y,x))
            q2=[]
            for i in range(3):
                if rgb[i]==1 and posbit<len(bits): # application du bit uniquement si la position correspondante dans rgb est égale à 1
                    q2.append(( q[i]&0b11111110 )+bits[posbit] )
                    posbit+=1
                else: # sinon, pas de modification de la valeur
                    q2.append(q[i]) 
            q2=tuple(q2)
            if xyorder==0:
                funcimage.putpixel((x,y),q2)
            else:
                funcimage.putpixel((y,x),q2)
            if posbit>=len(bits):
                break # casse les boucles si la position du bit arive au bout de la liste
        if posbit>=len(bits):
            break
    return funcimage

def check(funcimage,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8,creturn="CR"):
    sizex,sizey=funcimage.size
    twofirstletters=[]
    
    if xyorder==0: # same as previous ranges, but only takes the two fist characters of image to check them
        if xdir==0:
            xrange=range(ceil(len(creturn)*charbits/rgb.count(1)))
        else:
            xrange=range(sizex-1,sizex-ceil(len(creturn)*charbits/rgb.count(1))-1,-1)
        if ydir==0:
            y=0
        else:
            y=sizey-1
    else:
        if ydir==0:
            xrange=range(ceil(len(creturn)*charbits/rgb.count(1)))
        else:
            xrange=range(sizey-1,sizey-ceil(len(creturn)*charbits/rgb.count(1))-1,-1)
        if xdir==0:
            y=0
        else:
            y=sizex-1
            
    for x in xrange:
        if xyorder==0:
            pix=funcimage.getpixel((x,y))
        else:
            pix=funcimage.getpixel((y,x))
        for i in range(3):
            if rgb[i]==1:
                twofirstletters.append(pix[i]%2)
                
    state=True
    for lid in range(len(creturn)):
        if not chr(sum(val*(2**i) for i, val in enumerate(twofirstletters[charbits*lid:charbits*(lid+1)])))==creturn[lid]:
               state=False
    return state

def decode(funcimage,xyorder=0,xdir=0,ydir=0,rgb=(1,1,1),charbits=8,creturn="CR"):
    
    if not check(funcimage,xyorder,xdir,ydir,rgb,charbits,creturn):
        raise noTextInImageException
    sizex,sizey=funcimage.size
    bits=[]
    text=""
    if xyorder==0:
        if xdir==0:
            xrange=range(sizex)
        else:
            xrange=range(sizex-1,-1,-1)
        if ydir==0:
            yrange=range(sizey)
        else:
            yrange=range(sizey-1,-1,-1)
    else:
        if ydir==0:
            xrange=range(sizey)
        else:
            xrange=range(sizey-1,-1,-1)
        if xdir==0:
            yrange=range(sizex)
        else:
            yrange=range(sizex-1,-1,-1)
            
    for y in yrange:
        for x in xrange:
            if xyorder==0:
                pix=funcimage.getpixel((x,y))
            else:
                pix=funcimage.getpixel((y,x))
            for i in range(3):
                if rgb[i]==1:
                    bits.append(pix[i]%2)
                    if len(bits)%charbits==0:
                        char_bit_list=(bits[-1*charbits:])
                        text+=chr(sum(val*(2**i) for i, val in enumerate(char_bit_list)))
                        if text[-1*len(creturn):]==creturn and len(text)>2*len(creturn):
                            return text[len(creturn):-1*len(creturn)]