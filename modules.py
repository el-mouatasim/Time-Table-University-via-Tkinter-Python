from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

from Addtional_features import mycombobox, myentry

import sqlite3
import pandas as pd
import sys
import os 
from theme_engine import ThemeEngine

sys.path.append(os.path.abspath('../'))

class ModWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1280, 640
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.add_prod_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        #self.add_prod_win.resizable(0,0) # Disabling resize
        # Forcing Top-level window to stay on Top
        #self.add_prod_win.attributes('-topmost', 'true')
        # Setting Top Level Window Title
        self.add_prod_win.title("TT Gestion des modules")

        self.mainframe = LabelFrame(self.add_prod_win, width=1200, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        self.buve.menu.add_command(label="Import le fichier excel",command=self.importmodule)
        self.buve.menu.add_command(label="Claire frame",command=self.claireframe)
        self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=120, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        self.buve1.menu.add_command(label="Ajouter le module",command=self.addmodule)
        self.buve1.menu.add_command(label="Mise à jour le module",command=self.updatemodule)
        self.buve1.menu.add_command(label="Supprimer le module",command=self.delmodule)
        self.buve1.menu.add_command(label="Supprimer la filière",command=self.delallmodule)
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
         # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche par module",command=self.rechmodule)
        self.buve2.menu.add_command(label="Recherche par filière et semester",command=self.rechmodulefs)
        self.buve2.menu.add_command(label="Recherche tout",command=self.getmodule)
     
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()        
       
        ####

        mFrame1 = LabelFrame(self.add_prod_win, text = 'Informations sur Module',width=1100, height=100)
        mFrame1.place(x=50,y=50)


        Label(mFrame1, text = 'Filière:',  font=('Orbitron', 15)).place(x=50, y=50,height = 30)
        self.filier = mycombobox(mFrame1, width=10)
        self.filier.place(x=150, y=50,height = 30)
        self.cur.execute("select filiere from module")
        lif = self.cur.fetchall()    
        af = []
        for i in range(0, len(lif)):
            if lif[i][0] not in af:
                af.append(lif[i][0])
        self.filier.set_completion_list(af)        
       
        Label(mFrame1, text = 'Semestre:',  font=('Orbitron', 15)).place(x=300, y=50,height = 30) 
        self.semestre = Combobox(mFrame1, width=7)
        self.semestre['values'] = ('',
                                    'S1',
                                    'S2',
                                    'S3',
                                    'S4',
                                    'S5',
                                    'S6')
        self.semestre.current(0)  # set the selected item
        self.semestre.place(x=450, y=50,height = 30)  


        Label(mFrame1, text = 'Intitulé de module:',  font=('Orbitron', 15)).place(x=600, y=50,height = 30)
        self.nom_mod = StringVar()
        #Entry(mFrame1, textvariable=self.nom_mod, font="roboto 13", bg="#FFFFFF", width=30).place(x=365, y=50,height = 30)
        x1=myentry(mFrame1, textvariable=self.nom_mod,  width=25, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15))
        x1.place(x=800, y=50,height = 30)
        self.cur.execute("select nom from module")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        x1.set_completion_list(a)
        
        mFrame = Frame(self.add_prod_win,width=800, height=600)
        mFrame.place(x=150,y=225)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',  'filiere', "semestre", 'Nom'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=40)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)
        self.tree.column('#4', stretch=NO, minwidth=0, width=300)
        self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('Nom', text="Intitulé", anchor=W)
        self.tree.heading('filiere', text="Filière", anchor=W)
        self.tree.heading('semestre', text="Semestre", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getmodule()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)

        
    def getmodule(self,x=0):
         #self.base = sqlite3.connect("dataFPO.db")#سبحان الله
         #self.cur = self.base.cursor()
         # cleaning Table 
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)
         ans=''
         self.cur.execute("select * from module")
         modulelist = self.cur.fetchall()
         for i in modulelist:
              self.tree.insert('', 'end', values=(i))
              if (str(x) == i[0]):
                  a=self.tree.get_children()
                  ans=a[len(a)-1]

         return ans       

    def validation(self):
        if  self.nom_mod.get() == '' or self.filier.get() == '' or self.semestre.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter tous les champs*")
            return 0
  
    def addmodule(self):
        if self.validation() == 0:
            return
        elif self.check_exist()>0: 
            messagebox.showinfo("Validation info", "Le Module {} est deja exist!".format(self.nom_mod.get()))
            return
        else:    
            self.cur.execute("INSERT INTO module VALUES(NULL,?, ?, ?)",
                      (self.filier.get(), self.semestre.get(),self.nom_mod.get()))
            self.base.commit()
            self.getmodule()
            messagebox.showinfo("Validation info", "Module {} ajouté avec succès".format(self.nom_mod.get()))
            self.claireframe()
        
    def check_exist(self):
        self.cur.execute("SELECT * FROM module  WHERE nom = ? AND  filiere = ? AND semestre = ?",
                         (self.nom_mod.get(),self.filier.get(), self.semestre.get()))
        db_rows1=self.cur.fetchall()
        ls=len(list(db_rows1))
        chekrow = 0
        if 1 <=  ls: 
            chekrow += 1
        return chekrow
            
    def updatemodule(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.nom_mod.set((self.nom_mod.get()).upper())
        if self.validation() == 0:
            return
        if messagebox.askyesno('Alerte!',"Voulez-vous modifier le module sélectionner?") == True and (len(li) >= 3):     
            self.cur.execute("update module set  nom=?,  filiere = ?, semestre = ? where id = ?;",
                          (self.nom_mod.get(),self.filier.get(), self.semestre.get(),li[0]))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur=self.getmodule(li[0])
            self.tree.selection_set(cur)
            self.claireframe()
        
    def delmodule(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer le module sélectionner?") == True and len(li) >= 6:
            self.cur.execute("delete from module where id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getmodule()
            self.claireframe()

    def delallmodule(self):
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer la filière {}?".format(self.filier.get())) == True :
            self.cur.execute("delete from module where filiere = ?;", (self.filier.get(),))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getmodule()
            self.claireframe()
            
    def clicktable(self, event):
        self.claireframe()
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 3):
            self.nom_mod.set((li[3]))
            self.filier.insert(END, li[1])
            self.semestre.insert(END, li[2])

    def claireframe(self):
        self.nom_mod.set('')
        self.filier.delete(0, END)
        self.semestre.delete(0, END)
            
    def rechmodule(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from module")
        li=self.cur.fetchall() 
        if (self.nom_mod.get() == ''):
            messagebox.showerror("Erreur", "Merci de compléter  le champ: Intitulé ")
            return
        else:
            for i in li:
                if(i[2]==self.nom_mod.get()):
                    self.tree.insert('', 'end', values=(i))        

    def rechmodulefs(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from module")
        li=self.cur.fetchall() 
        if (self.filier.get() =='' and self.semestre.get()==''):
            messagebox.showerror("Erreur", "Merci de compléter les champs: Filière et Semestre")
            return        
        else:
            for i in li:
                if(i[3]==self.filier.get() and i[4]==self.semestre.get()):
                    self.tree.insert('', 'end', values=(i))
                    
    def importmodule(self):
        try:
            xl_file =  filedialog.askopenfilename(initialdir = "./docs",title = "Select file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
            table_name = 'module'
            conn = self.base
            c = self.cur
            df = pd.read_excel(xl_file)
            df.columns = self.get_column_names_from_db_table(c, table_name)
            df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
            #conn.close()
            messagebox.showinfo("Validation info", "SQL insert process finished")
            self.getmodule() 
        except:
            messagebox.showinfo("Validation info", "Fichier excel n'existe pas !")

    def get_column_names_from_db_table(self,sql_cursor, table_name):
    
        table_column_names = 'PRAGMA table_info(' + table_name + ');'
        sql_cursor.execute(table_column_names)
        table_column_names = sql_cursor.fetchall()
    
        column_names = list()
    
        for name in table_column_names:
            column_names.append(name[1])
    
        return column_names 





