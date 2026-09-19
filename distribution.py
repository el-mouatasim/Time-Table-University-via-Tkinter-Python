from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

from Addtional_features import  mycombobox, myentry

import sqlite3

import sys
import os 
from theme_engine import ThemeEngine

sys.path.append(os.path.abspath('../'))

class DistWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1100, 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.add_prod_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.add_prod_win.resizable(0,0) # Disabling resize
        # Forcing Top-level window to stay on Top
        #self.add_prod_win.attributes('-topmost', 'true')
        # Setting Top Level Window Title
        self.add_prod_win.title("TT Distribution")

        #self.executed = False # whether user has clicked browse at least once
        self.mainframe = LabelFrame(self.add_prod_win, width=700, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        #self.buve.menu.add_command(label="Import le fichier excel",command=self.importetudiant)
        self.buve.menu.add_command(label="Claire frame",command=self.claireframe)
        #self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=120, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        self.buve1.menu.add_command(label="Ajouter la distribution",command=self.adddist)
        self.buve1.menu.add_command(label="Mise à jour la distribution",command=self.updatedist)
        self.buve1.menu.add_command(label="Supprimer la distribution",command=self.deldist)
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
         # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche la distribution",command=self.rechdist)        
        
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()
      
        mFrame1 = LabelFrame(self.add_prod_win, text = 'Informations sur la distribution',width=700, height=230)
        mFrame1.place(x=50,y=70)
        Label(mFrame1, text = 'Filière: ').grid(row=2,column=1)
        self.filiere = mycombobox(mFrame1, width=7)
        self.filiere.grid(row=2,column=2)
        self.cur.execute("select filiere from module")
        lif = self.cur.fetchall()    
        af = []
        for i in range(0, len(lif)):
            if lif[i][0] not in af:
                af.append(lif[i][0])
        self.filiere.set_completion_list(af)         
                
        Label(mFrame1, text = 'Semestre: ').grid(row=2,column=3)
        self.semestre = Combobox(mFrame1, width=7)
        self.semestre['values'] = ('',
                                    'S1',
                                    'S2',
                                    'S3',
                                    'S4',
                                    'S5',
                                    'S6')
        self.semestre.current(0)  # set the selected item
        self.semestre.grid(row=2,column=4)
        self.semestre.bind("<<ComboboxSelected>>", self.callback)
        
        Label(mFrame1, text = '# Sections: ').grid(row=3,column=1)
        self.No_section = IntVar()      
        self.section = Spinbox(mFrame1, textvar=self.No_section, bg="#ccefff", fg='blue', from_=1, to=3, width=5, bd=5,
                  font=('Orbitron', 15))
        self.section.grid(row=3,column=2)

        Label(mFrame1, text = '# Groupes TD: ').grid(row=3,column=3)
        self.No_groupe = IntVar()      
        self.group = Spinbox(mFrame1, textvar=self.No_groupe, bg="#ccefff", fg='blue', from_=1, to=6, width=5, bd=5,
                  font=('Orbitron', 15))
        self.group.grid(row=3,column=4)

        Label(mFrame1, text = '# Groupes TP: ').grid(row=3,column=5)
        self.No_groupe_tp = IntVar()      
        self.group_tp = Spinbox(mFrame1, textvar=self.No_groupe_tp, bg="#ccefff", fg='blue', from_=0, to=6, width=5, bd=5,
                  font=('Orbitron', 15))
        self.group_tp.grid(row=3,column=6)
        
        Label(mFrame1, text = 'Cours commun: ', width=25).grid(row=4,column=1)
        self.commun = mycombobox(mFrame1, width=25)
        self.commun.grid(row=4,column=2)
        
        mFrame = Frame(self.add_prod_win,width=800, height=500)
        mFrame.place(x=50,y=200)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',
         'Filière', 'Semestre',  "Sections", 'Groupes', 'Groupes_tp', 'Commun'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=70)
        self.tree.column('#2', stretch=NO, minwidth=0, width=120)
        self.tree.column('#3', stretch=NO, minwidth=0, width=120)
        self.tree.column('#4', stretch=NO, minwidth=0, width=120)
        self.tree.column('#5', stretch=NO, minwidth=0, width=120)
        self.tree.column('#6', stretch=NO, minwidth=0, width=120)
        self.tree.column('#7', stretch=NO, minwidth=0, width=200)
        self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('Filière', text="Filière", anchor=W)
        self.tree.heading('Semestre', text="Semestre", anchor=W)
        self.tree.heading('Sections', text="# Sections", anchor=W)
        self.tree.heading('Groupes', text="# Groupes TD", anchor=W)        
        self.tree.heading('Groupes_tp', text="# Groupes TP", anchor=W)
        self.tree.heading('Commun', text="Commun", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=20)
        self.getdist()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)

    def callback(self,eventObject):
        self.cur.execute("SELECT nom FROM module  WHERE filiere = ? AND  semestre = ?",(self.filiere.get(),self.semestre.get()))
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        self.commun.set_completion_list(a)
        
    def getdist(self,x=0):
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)
         ans=''
         self.cur.execute("select * from distribution")
         distlist = self.cur.fetchall()
         for i in distlist:
              self.tree.insert('', 'end', values=(i))
              if (str(x) == i[0]):
                  a=self.tree.get_children()
                  ans=a[len(a)-1]
         return ans       
  
    def adddist(self):
        if self.filiere.get() == '' or self.semestre.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Filière ou Semestre !")
            return
        elif self.check_exist_dist()>0: 
            messagebox.showinfo("Validation info", "Distribution de la filière {} - semestreest {} deja exist!".format(self.filiere.get(),self.semestre.get()))
            return
        else:    
            self.cur.execute("INSERT INTO distribution VALUES(NULL,?, ?, ?, ?, ?, ?)",
                      (self.filiere.get(),self.semestre.get(), self.No_section.get(), self.No_groupe.get(), self.No_groupe_tp.get(), self.commun.get()))
            self.base.commit()
            self.getdist()
            messagebox.showinfo("Validation info", "Distribution de la filière {} - semestreest {} ajouté avec succès".format(self.filiere.get(),self.semestre.get()))
            self.claireframe()
        
    def check_exist_dist(self):
        self.cur.execute("SELECT * FROM distribution  WHERE filiere = ? and semestre = ?",
                         (self.filiere.get(),self.semestre.get(),))#add "," after
        db_rows1=self.cur.fetchall()
        ls=len(list(db_rows1))
        chekrow = 0
        if 1 <=  ls: 
            chekrow += 1
        return chekrow
            
    def updatedist(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.filiere.set((self.filiere.get()).upper())
        self.semestre.set((self.semestre.get()).upper())
        if self.filiere.get() == '' or self.semestre.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Filière ou Semestre !")
            return
        if(len(li) >= 5):     
            self.cur.execute("update distribution set  filiere=?, semestre = ?,  section =?, groupe =?, groupetp=?, commun=? where id = ?;",
              (self.filiere.get(),self.semestre.get(),  self.No_section.get(), self.No_groupe.get(), self.No_groupe_tp.get(), self.commun.get(),li[0]))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur=self.getdist(li[0])
            self.tree.selection_set(cur)
            self.claireframe()
        
    def deldist(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer la distribution  sélectionner?") == True and len(li) >= 6:
            self.cur.execute("delete from distribution  where id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getdist()
            self.claireframe()

    def clicktable(self, event):
        self.claireframe()
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 5):
            self.filiere.set((li[1]))
            self.semestre.insert(END, li[2])
            self.No_section.set((li[3]))
            self.No_groupe.set((li[4]))
            self.No_groupe_tp.set((li[5]))
            self.commun.set((li[6]))
            

    def claireframe(self):
        self.filiere.set('')
        self.semestre.delete(0, END)
        self.No_section.set('1')
        self.No_groupe.set('1')
        self.No_groupe_tp.set('0')
        self.commun.set('')
          
    def rechdist(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from distribution")
        li=self.cur.fetchall() 
        if (self.filiere.get() == ''):
            messagebox.showerror("Erreur", "Merci de compléter le champ filiere")
            return
        
        for i in li:
            if(i[1]==self.filiere.get()):
                self.tree.insert('', 'end', values=(i)) 





