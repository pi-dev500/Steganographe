# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 21:22:12 2024

@author: Pi-dev500
"""

from tkinter import filedialog, Tk, Frame, Text, Entry, Button, END, IntVar, Label,Checkbutton
import pystega
class Checkbox(Checkbutton): # J'avais un bug étrange sur l'utilisation des IntVar, ce qui explique cette classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = IntVar(self)
        self.config(variable=self.variable)

    def checked(self):
        return self.variable.get() # récupère la variable interne

    def set_value(self,value):
        self.variable.set(value) # Coche ou décoche selon la valeur

class App_Settings():# paramètres de l'app
    xyinvert=0   ## variables contenant les paramètres
    xdir=0
    ydir=0
    rgb=(1,1,1)
    charbits=8
    shown=False
    def show(self): # fenètre qui s'affiche uniquement quand souhaité
        #-initialisation de la fenètre
        if self.shown==True: # Permet aux paramètres de se réouvrir uniquement si ils sont fermés
            return
        self.window=Tk()
        self.window.geometry("500x500")
        self.window.wm_title('Paramètres')
        
        #-Paramètres de balayage-----------------------------------------------
        self.xyinvert_box=Checkbox(self.window,text="Inverser l'ordre de balayage ligne/colonne.",command=self.update)
        self.xdir_box=Checkbox(self.window,text="Inverser le sens de balayage des lignes",command=self.update)
        self.ydir_box=Checkbox(self.window,text="Inverser le sens de balayage des colonnes",command=self.update)
        
        #-Choix des composantes dont le LSB est utilisé------------------------
        self.rgb_label=Label(self.window,text="Utilisation des composantes:")
        self.rgbframe=Frame(self.window)
        self.checkR=Checkbox(self.rgbframe, text="Rouge",command=self.update)
        self.checkG=Checkbox(self.rgbframe, text="Vert",command=self.update)
        self.checkB=Checkbox(self.rgbframe, text="Bleu",command=self.update)
        self.checkR.pack(side="left",expand=True,fill="both")
        self.checkG.pack(side="left",expand=True,fill="both")
        self.checkB.pack(side="left",expand=True,fill="both")
        
        #-Entrée du nombre de bits par caractères------------------------------
        self.charbits_frame=Frame(self.window)
        self.entry_charbits=Entry(self.charbits_frame)
        self.entry_charbits.bind("<Return>",self.update)
        self.charbits_frame.label=Label(self.charbits_frame,text="bits par caractères")
        
        #-Affichage des paramètres actuels-------------------------------------
        self.xyinvert_box.set_value(self.xyinvert) # affichage des paramètres actuels
        self.xdir_box.set_value(self.xdir)
        self.ydir_box.set_value(self.ydir)
        self.checkR.set_value(self.rgb[0])
        self.checkG.set_value(self.rgb[1])
        self.checkB.set_value(self.rgb[2])
        self.entry_charbits.insert(0,self.charbits)
        
        #-Affichage des widgets------------------------------------------------
        self.entry_charbits.pack(side="left",expand=True, fill="x")
        self.charbits_frame.label.pack(side="right",expand=True, fill="both")
        self.xyinvert_box.pack(expand=True,fill='both')
        self.xdir_box.pack(expand=True,fill='both')
        self.ydir_box.pack(expand=True,fill='both')
        self.rgb_label.pack(expand=True,fill='both')
        self.rgbframe.pack(expand=True,fill='both')
        self.charbits_frame.pack(expand=True,fill="both")
        
        #-Protocoles de fermeture----------------------------------------------
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.shown=True # Permet aux paramètres de se réouvrir uniquement si ils sont fermés
    def update(self,default=None):
        #-Mise à jour des variables contenant les paramètres-------------------
        self.xyinvert=self.xyinvert_box.checked()
        self.xdir=self.xdir_box.checked()
        self.ydir=self.ydir_box.checked()
        self.rgb=(self.checkR.checked(),self.checkG.checked(),self.checkB.checked())
        self.charbits=int(self.entry_charbits.get())
    def close_window(self):
        #-Actions lors de la fermeture de la fenètre---------------------------
        self.update() # Dans le cas impossible où la mise à jour des variables ne se serait pas effectuée avant ☻
        self.window.destroy()
        self.shown=False # Permet aux paramètres de se réouvrir uniquement si ils sont fermés
        
class Application(Tk):
    workimage=None
    def __init__(self):
        #-Initialisation de l'objet Tk hérité, la fenètre de l'application-----
        Tk.__init__(self)
        self.settings=App_Settings()
        self.geometry("500x500")
        self.wm_title("Interface de steganographie")
        self.focus_force() # Prends le focus, sinon, elle apparait en arrière-plan
        
        #-Partie de selection d'image------------------------------------------
        self.fileExplorer=Frame(self)
        self.fileExplorer.entry=Entry(self.fileExplorer)
        self.fileExplorer.entry.bind("<Return>",self.setIMGfile)
        self.fileExplorer.button=Button(self.fileExplorer,command=self.Browse,text="Explorer...")
        self.fileExplorer.entry.pack(side="left",expand=True,fill="both")
        self.fileExplorer.button.pack(side="right",fill="both")
        
        self.text=Text(self) # widget pour entrer le texte à coder ou afficher le texte décodé
        
        #-Barre de boutons d'action--------------------------------------------
        self.actions=Frame(self)
        self.actions.encode_button=Button(self.actions,text="Encoder",command=self.Encode)
        self.actions.decode_button=Button(self.actions,text="Decoder",command=self.Decode)
        self.actions.save_button=Button(self.actions,text="Sauvegarder l'image",command=self.SaveAS)
        self.actions.settings_button=Button(self.actions,text="Parametres",command=self.settings.show)
        #-Ajout des boutons à la barre-----------------------------------------
        self.actions.encode_button.pack(side="left",expand=True,fill="both")
        self.actions.decode_button.pack(side="left",expand=True,fill="both")
        self.actions.save_button.pack(side="left",expand=True,fill="both")
        self.actions.settings_button.pack(side='right',expand=True,fill='both')
        #-Affichage------------------------------------------------------------
        self.fileExplorer.pack(fill="both")
        self.text.pack(expand=True,fill="both")
        self.actions.pack(fill="both")
        
    def Browse(self):
        #-Explorateur pour choisir une image-----------------------------------
        filename= filedialog.askopenfilename(title="Select an Image",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
        if filename!="":
            self.fileExplorer.entry.delete(0,END)
            self.fileExplorer.entry.insert(0,filename)
            self.setIMGfile()
    def setIMGfile(self,a=None):
        #-Import de l'image choisie et stockage dans la mémoire vive-----------
        self.workimage=pystega.Img(self.fileExplorer.entry.get())
    def SaveAS(self):
        #-Ouvre un explorateur pour enregistrer l'image------------------------
        filename=filedialog.asksaveasfilename(title="Save Image as",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
        self.workimage.save(filename)
        print("Image saved as:",filename)
    def Encode(self):
        #-Encode du texte dans l'image selectionnée----------------------------
        text=self.text.get(1.0,END)
        pystega.encode(self.workimage,text,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits)
    def Decode(self):
        #-décode le texte de l'image selectionnée------------------------------
        text=pystega.decode(self.workimage,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits)
        self.text.delete(1.0,END)
        self.text.insert(1.0,text)
root=Application()
root.mainloop()