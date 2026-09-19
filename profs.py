from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

from Addtional_features import myentry, mycombobox

import sqlite3

import sys
import os 
from theme_engine import ThemeEngine

sys.path.append(os.path.abspath('../'))

class ProfWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1100, 650
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.add_prod_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.add_prod_win.resizable(0,0) # Disabling resize
        # Forcing Top-level window to stay on Top
        #self.add_prod_win.attributes('-topmost', 'true')
        # Setting Top Level Window Title
        self.add_prod_win.title("TT Enseignants")

        #self.executed = False # whether user has clicked browse at least once
        self.mainframe = LabelFrame(self.add_prod_win, width=1100, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        #self.buve.menu.add_command(label="Import le fichier excel",command=self.importprof)
        self.buve.menu.add_command(label="Claire frame",command=self.claireframe)
        #self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=120, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        self.buve1.menu.add_command(label="Ajouter le prof",command=self.addprof)
        self.buve1.menu.add_command(label="Mise à jour le prof",command=self.updateprof)
        self.buve1.menu.add_command(label="Supprimer le prof",command=self.delprof)
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
         # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche le prof",command=self.rechprof)
        #self.buve2.menu.add_command(label="Recherche par filière et semester",command=self.rechmodulefs)
        #self.buve2.menu.add_command(label="Recherche tout",command=self.getmodule)
        
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()

        mFrame1 = LabelFrame(self.add_prod_win, text = 'Informations sur Profs',width=1100, height=200)
        mFrame1.place(x=50,y=40)
        Label(mFrame1, text = 'Prof. : ', font=('Orbitron', 15)).place(x=10, y=50,height = 30)
        self.nom = StringVar()
        x1=myentry(mFrame1, textvariable=self.nom,  width=25, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15))
        x1.place(x=100, y=50,height = 35)
        self.cur.execute("select prof from profs")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        x1.set_completion_list(a)

        
        Label(mFrame1, text = 'Filière:',  font=('Orbitron', 15)).place(x=400, y=50,height = 30)
        self.filiere = mycombobox(mFrame1, width=10)
        self.filiere.place(x=480, y=50,height = 30)
        self.cur.execute("select filiere from module")
        lif = self.cur.fetchall()    
        af = []
        for i in range(0, len(lif)):
            if lif[i][0] not in af:
                af.append(lif[i][0])
        self.filiere.set_completion_list(af)        

        Label(mFrame1, text = 'Semestre: ', font=('Orbitron', 15)).place(x=660, y=50,height = 30)
        self.semestre = Combobox(mFrame1, width=10)
        self.semestre['values'] = ('',
                                    'S1',
                                    'S2',
                                    'S3',
                                    'S4',
                                    'S5',
                                    'S6')
        self.semestre.current(0)  # set the selected item
        self.semestre.place(x=810, y=50,height = 30)
        self.semestre.bind("<<ComboboxSelected>>", self.callback)
        Label(mFrame1, text = 'Module :', font=('Orbitron', 15)).place(x=10, y=100,height = 30)
        self.module=mycombobox(mFrame1, width=35)
        self.module.place(x=110, y=100,height = 30)                       

                              
        mFrame = Frame(self.add_prod_win,width=800, height=600)
        mFrame.place(x=50,y=250)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',
         'prof', 'filiere', "semestre", 'module'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=70)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)
        self.tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.tree.column('#5', stretch=NO, minwidth=0, width=150)
        self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('prof', text="Prof.", anchor=W)
        self.tree.heading('filiere', text="Filière", anchor=W)
        self.tree.heading('semestre', text="Semestre", anchor=W)
        self.tree.heading('module', text="Module", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getprof()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)
        
    def callback(self,eventObject):
        self.cur.execute("SELECT nom FROM module  WHERE filiere = ? AND  semestre = ?",(self.filiere.get(),self.semestre.get()))
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        self.module.set_completion_list(a)
        
    def getprof(self,x=0):
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)
         ans=''
         self.cur.execute("select * from profs")
         proflist = self.cur.fetchall()
         for i in proflist:
              self.tree.insert('', 'end', values=(i))
              if (str(x) == i[0]):
                  a=self.tree.get_children()
                  ans=a[len(a)-1]
         return ans       
  
    def addprof(self):
        if self.nom.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Nom!")
            return
        else:    
            self.cur.execute("INSERT INTO profs VALUES(NULL,?, ?, ?, ?)",
                      (self.nom.get(),self.filiere.get(), self.semestre.get(), self.module.get()))
            self.base.commit()
            self.getprof()
            messagebox.showinfo("Validation info", "Enseignant {} ajouté avec succès".format(self.nom.get()))
            self.claireframe()
        

            
    def updateprof(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.nom.set((self.nom.get()).upper())
        if self.nom.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Nom!")
            return
        if(len(li) >= 5):     
            self.cur.execute("update profs set  prof=?, filiere = ?, semestre = ?, module =? where id = ?;",
              (self.nom.get(),self.filiere.get(), self.semestre.get(), self.module.get(),li[0]))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur=self.getprof(li[0])
            self.tree.selection_set(cur)
            self.claireframe()
        
    def delprof(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer l'enseignant  sélectionner?") == True and len(li) >= 5:
            self.cur.execute("delete from profs  where id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getprof()
            self.claireframe()

            
    def clicktable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 5):
            self.nom.set((li[1]))
            self.filiere.set((li[2]))
            self.semestre.set((li[3]))
            self.module.set((li[4]))

    def claireframe(self):
        self.nom.set('')
        self.filiere.set('')
        self.semestre.set('')
        self.module.set('') 
          
    def rechprof(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from profs")
        li=self.cur.fetchall() 
        if (self.nom.get() == ''):
            messagebox.showerror("Erreur", "Merci de compléter le champ nom")
            return
        
        for i in li:
            if(i[1]==self.nom.get()):
                self.tree.insert('', 'end', values=(i))
                




