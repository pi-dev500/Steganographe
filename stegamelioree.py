from tkinter import IntVar, DISABLED, NORMAL, filedialog, END
from customtkinter import (CTkButton as Button,
                           CTk as Tk, 
                           CTkEntry as Entry,
                           CTkFrame as Frame,
                           CTkTextbox as Text,
                           CTkLabel as Label,
                           CTkCheckBox as Checkbutton,
                           CTkTabview as Tabview,
                           CTkImage,
                           CTkScrollableFrame,
                           CTkInputDialog
                           )
from PIL import Image
import json
import pystega

class Checkbox(Checkbutton): # J'avais un bug étrange sur l'utilisation des IntVar, ce qui explique cette classe
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = IntVar(self)
        self.configure(variable=self.variable)

    def checked(self):
        return self.variable.get() # récupère la variable interne

    def set_value(self,value):
        self.variable.set(value) # Coche ou décoche selon la valeur
class Console(Text):
    def __init__(self,*args, **kwargs):
        self.buffer=False
        super().__init__(*args, **kwargs)
        self.configure(state=DISABLED)
    def log(self,message):
        self.configure(state=NORMAL)
        if self.buffer:
            self.insert(1.0,"\n")
        self.insert(1.0,"Message: "+message)
        self.configure(state=DISABLED)
        self.buffer=True
class App_Settings():# paramètres de l'app
    xyinvert=0   ## variables contenant les paramètres
    xdir=0
    ydir=0
    rgb=(1,1,1)
    charbits=8
    creturn="CR"
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
        
        #-Entrée du retour chariot personalisé---------------------------------
        self.creturn_frame=Frame(self.window)
        self.entry_creturn=Entry(self.creturn_frame)
        self.entry_creturn.bind("<Return>",self.update)
        self.creturn_frame.label=Label(self.creturn_frame,text="Caractères de retour chariot")
        
        #-Affichage des paramètres actuels-------------------------------------
        self.xyinvert_box.set_value(self.xyinvert) # affichage des paramètres actuels
        self.xdir_box.set_value(self.xdir)
        self.ydir_box.set_value(self.ydir)
        self.checkR.set_value(self.rgb[0])
        self.checkG.set_value(self.rgb[1])
        self.checkB.set_value(self.rgb[2])
        self.entry_charbits.insert(0,self.charbits)
        self.entry_creturn.insert(0,self.creturn)
        
        #-Affichage des widgets------------------------------------------------
        self.entry_charbits.pack(side="left",expand=True, fill="x")
        self.charbits_frame.label.pack(side="right",expand=True, fill="both")
        self.entry_creturn.pack(side="left",expand=True, fill="x")
        self.creturn_frame.label.pack(side="right",expand=True, fill="both")
        self.xyinvert_box.pack(expand=True,fill='both')
        self.xdir_box.pack(expand=True,fill='both')
        self.ydir_box.pack(expand=True,fill='both')
        self.rgb_label.pack(expand=True,fill='both')
        self.rgbframe.pack(expand=True,fill='both')
        self.charbits_frame.pack(expand=True,fill="both")
        self.creturn_frame.pack(expand=True,fill="both")
        #-Protocoles de fermeture----------------------------------------------
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.shown=True # Permet aux paramètres de se réouvrir uniquement si ils sont fermés
        self.window.mainloop()
    def update(self,default=None):
        #-Mise à jour des variables contenant les paramètres-------------------
        self.xyinvert=self.xyinvert_box.checked()
        self.xdir=self.xdir_box.checked()
        self.ydir=self.ydir_box.checked()
        self.rgb=(self.checkR.checked(),self.checkG.checked(),self.checkB.checked())
        self.charbits=int(self.entry_charbits.get())
        self.creturn=self.entry_creturn.get()
    def close_window(self):
        #-Actions lors de la fermeture de la fenètre---------------------------
        self.update() # Dans le cas impossible où la mise à jour des variables ne se serait pas effectuée avant ☻
        self.window.destroy()
        self.shown=False # Permet aux paramètres de se réouvrir uniquement si ils sont fermés
        

class Table(CTkScrollableFrame):
    data=dict()
    def __init__(self,masterw,dictionary={"Nom": "","Prénom":"","Date de Naissance dd/mm/aaaa":"","Poids (kg)":"","Taille (m)":"","Sexe (M/F/I)":""},*args, **kwargs):
        super().__init__(masterw,*args, **kwargs)
        self.add_btn=Button(self,text="Ajouter un nouveau champ...", command=self.new)
        for name, value in dictionary.items():
            self.data[name]=self.create_row(name,value)
        self.add_btn.pack(pady=5)
    def create_row(self,name,value):
        self.add_btn.pack_forget() # éviter que le nouveau champ se retrouve après le bouton
        rframe=Frame(self)
        rlabel=Label(rframe,text=name)
        rentry=Entry(rframe)
        rentry.insert(0,value)
        rlabel.pack(side="left")
        rentry.pack(side="right")
        rframe.pack(fill="both",pady=5) # le padding améliore l'apparence
        self.add_btn.pack(pady=5)
        return {"frame": rframe, "label": rlabel, "entry": rentry}
    def get_data(self):
        result=dict()
        for name,value in self.data.items():
            result[name]=value["entry"].get()
        print(result)
        return result
    def new(self):
        dialog=CTkInputDialog(text="Veuillez entrer le nom du nouveau champ:",title="Nouveau champ pour medistega")
        name=dialog.get_input()
        if name:
            self.data[name]=self.create_row(name,"")
class Application(Tk):
    workimage=None
    def __init__(self):
        #-Initialisation de l'objet Tk hérité, la fenètre de l'application-----
        Tk.__init__(self)
        self.settings=App_Settings()
        self.geometry("800x500")
        self.wm_title("Interface de steganographie Médicale")
        self.focus_force() # Prends le focus, sinon, elle apparait en arrière-plan
        
        #-Partie de selection d'image------------------------------------------
        self.fileExplorer=Frame(self)
        self.fileExplorer.entry=Entry(self.fileExplorer)
        self.fileExplorer.entry.bind("<Return>",self.setIMGfile)
        self.fileExplorer.button=Button(self.fileExplorer,command=self.Browse,text="Explorer...")
        self.fileExplorer.entry.pack(side="left",expand=True,fill="both")
        self.fileExplorer.button.pack(side="right",fill="both")
        self.ATF = Frame(self)
        self.app_tabs=Tabview(self.ATF)
        self.app_tabs.add("Infos Médicales")
        self.app_tabs.add("Notes")
        self.app_tabs.set("Infos Médicales")
        #-Onglets--------------------------------------------------------------
        self.textlabel=Label(self.app_tabs.tab("Notes"),text="Entrée de notes médicales: ")
        self.app_tabs.pack()
        self.text=Text(self.app_tabs.tab("Notes")) # widget pour entrer le texte à coder ou afficher le texte décodé
        #-Partie formelle (Infos Médicales)------------------------------------
        defimage=Image.open("images/default.png")
        self.M_UPFrame=Frame(self.app_tabs.tab("Infos Médicales"))
        self.M_UPimage=CTkImage(light_image=defimage,dark_image=defimage,size=(defimage.width/defimage.height*70,70)) # images customtkinter différentes
        self.M_UPlabel=Label(self.M_UPFrame,image=self.M_UPimage,text="")#
        self.M_Dbutton=Button(self.M_UPFrame,text="Récupérer les champs par défaut", command=self.medical_rec)
        
        #-Console--------------------------------------------------------------
        self.console=Console(self)
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
        
        # Affichage onglet "Notes"
        self.textlabel.pack()
        self.text.pack(expand=True,fill="both")
        # Affichage onglet "Infos Médicales"
        self.M_UPFrame.pack(side="top", fill="both")
        self.M_UPlabel.pack(side="left")
        # self.M_Dbutton.pack(side="right") # Je ne sais pas si c'est trés utile.
        # Affichage final
        self.fileExplorer.pack(fill="both")
        self.ATF.pack(expand=True, fill="both")
        self.app_tabs.pack(expand=True, fill="both")
        self.console.pack(fill="both")
        self.console.configure(height=2)
        self.actions.pack(fill="both")
        
        
    def medical_rec(self):
        try:
            self.MTable.get_data()
        except:
            pass
    def Browse(self):
        #-Explorateur pour choisir une image-----------------------------------
        try:
            filename= filedialog.askopenfilename(title="Select an Image",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
        except Exception as error:
            if hasattr(error, 'message'):
                self.console.log(error.message)
        if filename!="":
            self.fileExplorer.entry.delete(0,END)
            self.fileExplorer.entry.insert(0,filename)
            self.setIMGfile()
    def setIMGfile(self,a=None):
        #-Import de l'image choisie et stockage dans la mémoire vive-----------
        try:
            self.workimage=pystega.Img(self.fileExplorer.entry.get())
            self.console.log("Image selectionnée: "+ self.fileExplorer.entry.get())
            self.M_UPimage=CTkImage(light_image=self.workimage,dark_image=self.workimage,size=(self.workimage.width/self.workimage.height*70,70))
            self.M_UPlabel.configure(image=self.M_UPimage)
            try:
                self.MTable.pack_forget()
                self.MTable.destroy()
            except:
                pass
            self.MTable=Table(self.app_tabs.tab("Infos Médicales"))
            self.MTable.pack(side="bottom",expand=True,fill="both")
        except Exception as error:
            if hasattr(error, 'message'):
                self.console.log(error.message)
    def SaveAS(self):
        #-Ouvre un explorateur pour enregistrer l'image------------------------
        if not self.workimage:
                self.console.log("Pas d'image dans la mémoire. Veuillez en selectionner une d'abord.")
        else:
            filename=filedialog.asksaveasfilename(title="Save Image as",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
            try:
                self.workimage.save(filename)
                self.console.log("Image sauvegardée sous: "+filename)
            except Exception as error:
                if filename=="":
                    self.console.log("Pas de fichier selectionné")
                elif hasattr(error, 'message'):
                    self.console.log(error.message)
        print("Image saved as:",filename)
    def Encode(self):
        #-Encode du texte dans l'image selectionnée----------------------------
        try:
            jdict=dict()
            jdict["notes"]=self.text.get(0.0,END)
            jdict["donnees"]=self.MTable.get_data()
            text=json.dumps(jdict)
            pystega.encode(self.workimage,text,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits,self.settings.creturn)
            self.console.log("Succès !")
        except Exception as error:
            if not self.workimage:
                self.console.log("Pas d'image dans la mémoire. Veuillez en selectionner une d'abord.")
            elif hasattr(error, 'message'):
                self.console.log(error.message)
    def Decode(self):
        #-décode le texte de l'image selectionnée------------------------------
        try:
            text=pystega.decode(self.workimage,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits,self.settings.creturn)
            jdict=json.loads(text)
            self.text.delete(0.0,END)
            self.text.insert(0.0,jdict["notes"][:-1])#Mettre le texte sans le \n exédent
            try:
                self.MTable.pack_forget()
                self.MTable.destroy()
            except:
                pass
            j2data=jdict["donnees"]
            self.MTable=Table(self.app_tabs.tab("Infos Médicales"),j2data)
            self.MTable.pack(side="bottom",expand=True,fill="both")
            self.textlabel.configure(text="Notes éditables décodées à partir de l'image: ")
            self.console.log("Succès !")
        except Exception as error:
            if not self.workimage:
                self.console.log("Pas d'image dans la mémoire. Veuillez en selectionner une d'abord.")
            elif hasattr(error, 'message'):
                self.console.log(error.message)
        
root=Application()
root.mainloop()