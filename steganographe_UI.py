# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 21:22:12 2024

@author: Pi-dev500
"""

from tkinter import filedialog, Tk, Frame, Text, Entry, Button, END, IntVar, Label,Checkbutton, BooleanVar
import pystega
class Checkbox(Checkbutton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = IntVar(self)
        self.config(variable=self.variable)

    def checked(self):
        return self.variable.get()

    def set_value(self,value):
        self.variable.set(value)

class App_Settings():
    xyinvert=0
    xdir=0
    ydir=0
    rgb=(1,1,1)
    charbits=8
    def show(self):
        self.window=Tk()
        self.window.geometry("500x500")
        self.window.wm_title('Paramètres')
        self.xyinvert_box=Checkbox(self.window,text="Inverser l'ordre de balayage ligne/colonne.")
        self.xyinvert_box.set_value(self.xyinvert)
        self.xdir_box=Checkbox(self.window,text="Inverser le sens de balayage des lignes")
        self.xdir_box.set_value(self.xdir)
        self.ydir_box=Checkbox(self.window,text="Inverser le sens de balayage des colonnes")
        self.ydir_box.set_value(self.ydir)
        self.rgb_label=Label(self.window,text="Utilisation des composantes:")
        self.rgbframe=Frame(self.window)
        self.checkR=Checkbox(self.rgbframe, text="Rouge")
        self.checkG=Checkbox(self.rgbframe, text="Vert")
        self.checkB=Checkbox(self.rgbframe, text="Bleu")
        self.checkR.set_value(self.rgb[0])
        self.checkG.set_value(self.rgb[1])
        self.checkB.set_value(self.rgb[2])
        self.checkR.pack(side="left",expand=True,fill="both")
        self.checkG.pack(side="left",expand=True,fill="both")
        self.checkB.pack(side="left",expand=True,fill="both")
        self.charbits_frame=Frame(self.window)
        self.entry_charbits=Entry(self.charbits_frame)
        self.entry_charbits.insert(0,self.charbits)
        self.charbits_frame.label=Label(self.charbits_frame,text="bits par caractères")
        self.entry_charbits.pack(side="left",expand=True, fill="x")
        self.charbits_frame.label.pack(side="right",expand=True, fill="both")
        self.xyinvert_box.pack(expand=True,fill='both')
        self.xdir_box.pack(expand=True,fill='both')
        self.ydir_box.pack(expand=True,fill='both')
        self.rgb_label.pack(expand=True,fill='both')
        self.rgbframe.pack(expand=True,fill='both')
        self.charbits_frame.pack(expand=True,fill="both")
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
    def update(self):
        self.xyinvert=self.xyinvert_box.checked()
        self.xdir=self.xdir_box.checked()
        self.ydir=self.ydir_box.checked()
        self.rgb=(self.checkR.checked(),self.checkG.checked(),self.checkB.checked())
        self.charbits=int(self.entry_charbits.get())
        print(self.xyinvert,self.xdir,self.ydir,self.rgb,self.charbits)
    def close_window(self):
        self.update()
        self.window.destroy()
        
    #todo: add update bindings
class Application(Tk):
    workimage=None
    def __init__(self):
        Tk.__init__(self)
        self.settings=App_Settings()
        self.geometry("500x500")
        self.wm_title("Interface de steganographie")
        self.fileExplorer=Frame(self)
        self.fileExplorer.entry=Entry(self.fileExplorer)
        self.fileExplorer.entry.bind("<Return>",self.setIMGfile)
        self.fileExplorer.button=Button(self.fileExplorer,command=self.Browse,text="Explorer...")
        self.fileExplorer.entry.pack(side="left",expand=True,fill="both")
        self.fileExplorer.button.pack(side="right",fill="both")
        self.text=Text(self)
        self.actions=Frame(self)
        self.actions.encode_button=Button(self.actions,text="Encoder",command=self.Encode)
        self.actions.decode_button=Button(self.actions,text="Decoder",command=self.Decode)
        self.actions.save_button=Button(self.actions,text="Sauvegarder l'image",command=self.SaveAS)
        self.actions.settings_button=Button(self.actions,text="Parametres",command=self.settings.show)
        self.actions.encode_button.pack(side="left",expand=True,fill="both")
        self.actions.decode_button.pack(side="left",expand=True,fill="both")
        self.actions.save_button.pack(side="left",expand=True,fill="both")
        self.actions.settings_button.pack(side='right',expand=True,fill='both')
        self.fileExplorer.pack(fill="both")
        self.text.pack(expand=True,fill="both")
        self.actions.pack(fill="both")
        
    def Browse(self):
        filename= filedialog.askopenfilename(title="Select an Image",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
        if filename!="":
            self.fileExplorer.entry.delete(0,END)
            self.fileExplorer.entry.insert(0,filename)
            self.setIMGfile()
    def setIMGfile(self,a=None):
        self.workimage=pystega.Img(self.fileExplorer.entry.get())
    def SaveAS(self):
        filename=filedialog.asksaveasfilename(title="Save Image as",filetypes=(("Binary images","*.bmp"),("All files","*.*")))
        self.workimage.save(filename)
        print("Image saved as:",filename)
    def Encode(self):
        text=self.text.get(1.0,END)
        pystega.encode(self.workimage,text,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits)
    def Decode(self):
        text=pystega.decode(self.workimage,self.settings.xyinvert,self.settings.xdir,self.settings.ydir,self.settings.rgb,self.settings.charbits)
        self.text.delete(1.0,END)
        self.text.insert(1.0,text)
root=Application()
root.mainloop()