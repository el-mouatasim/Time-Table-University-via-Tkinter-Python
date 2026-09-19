from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

from Addtional_features import myentry

import sqlite3

import sys
import os 
from theme_engine import ThemeEngine

sys.path.append(os.path.abspath('../'))

class SalWindow(ThemeEngine):
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
        self.add_prod_win.title("TT Gestion des Salles")

        #self.executed = False # whether user has clicked browse at least once
        self.mainframe = LabelFrame(self.add_prod_win, width=1200, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        self.buve.menu.add_command(label="Import le fichier excel",command=self.importsalle)
        self.buve.menu.add_command(label="Claire frame",command=self.claireframe)
        self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=120, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        self.buve1.menu.add_command(label="Ajouter la salle",command=self.addsalle)
        self.buve1.menu.add_command(label="Mise à jour la salle",command=self.updatesalle)
        self.buve1.menu.add_command(label="Supprimer la salle",command=self.delsalle)
        #self.buve1.menu.add_command(label="Supprimer tout",command=self.delallprof)
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
        # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche la salle",command=self.rechsalle)
        self.buve2.menu.add_command(label="Recherche tout",command=self.getsalle)
        
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()        
        # intial para
        #self.max_rand_value = 9 # Max bounds for random int, increases every level
        self.user_level = 1  # Users current level
        self.current_correctness = 3  # Current consecutive questions correct (starts at 3 if goes to 6 up 1 level if down to 0 down 1 level)
       
        ####

        mFrame1 = LabelFrame(self.add_prod_win, text = 'Informations sur Salle',width=900, height=230)
        mFrame1.place(x=50,y=30)
        Label(mFrame1, text = 'Nom : ', font=('Orbitron', 15)).place(x=10, y=50,height = 30)
        self.nom = StringVar()
        x1=myentry(mFrame1, textvariable=self.nom,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15))
        x1.place(x=110, y=50,height = 30)
        self.cur.execute("select nom from salle")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        x1.set_completion_list(a)
        Label(mFrame1, text = 'Capaciter :', font=('Orbitron', 15)).place(x=330, y=50,height = 30)
        self.capaciter = StringVar()
        Entry(mFrame1, textvariable=self.capaciter,  width=10, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=450, y=50,height = 30) 
        Label(mFrame1, text = 'Cours :', font=('Orbitron', 15)).place(x=600, y=50,height = 30)
        self.cours = StringVar() 
        self.cours = Combobox(mFrame1, width=10)
        self.cours['values'] = ('',
                                    'OUI',
                                    'NON')
        self.cours.current(0)  
        self.cours.place(x=660, y=50,height = 30) 
        Label(mFrame1, text = 'TD :', font=('Orbitron', 15)).place(x=10, y=100,height = 30)
        self.td= StringVar() 
        self.td = Combobox(mFrame1, width=10)
        self.td['values'] = ('',
                                    'OUI',
                                    'NON')
        self.td.current(0)  
        self.td.place(x=110, y=100,height = 30)         
        Label(mFrame1, text = 'TP :', font=('Orbitron', 15)).place(x=210, y=100,height = 30)
        self.tp= StringVar() 
        self.tp = Combobox(mFrame1, width=10)
        self.tp['values'] = ('',
                                    'OUI',
                                    'NON')
        self.tp.current(0)  
        self.tp.place(x=310, y=100,height = 30)         
        Label(mFrame1, text = 'Exam :', font=('Orbitron', 15)).place(x=410, y=100,height = 30)
        self.exam= StringVar() 
        self.exam = Combobox(mFrame1, width=10)
        self.exam['values'] = ('',
                                    'OUI',
                                    'NON')
        self.exam.current(0)  
        self.exam.place(x=510, y=100,height = 30)          
        Label(mFrame1, text = 'Departement  :', font=('Orbitron', 15)).place(x=620, y=100,height = 30)
        self.departement = Combobox(mFrame1, width=10)
        self.departement['values'] = ('',
                                    'MIG',
                                    'PC',
                                    'LASH',
                                    'AUTRE')
        self.departement.current(0)  # set the selected item
        self.departement.place(x=750, y=100,height = 30)  
                      
                                      
        
        mFrame = Frame(self.add_prod_win,width=800, height=600)
        mFrame.place(x=50,y=250)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',
         'Nom', 'capaciter', "cours", 'td','tp','exam','departement'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=70)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.column('#4', stretch=NO, minwidth=0, width=150)
        self.tree.column('#5', stretch=NO, minwidth=0, width=150)
        self.tree.column('#6', stretch=NO, minwidth=0, width=70)                 
        self.tree.column('#7', stretch=NO, minwidth=0, width=70)
        self.tree.column('#8', stretch=NO, minwidth=0, width=100)
        self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('Nom', text="Nom", anchor=W)
        self.tree.heading('capaciter', text="Capaciter", anchor=W)
        self.tree.heading('cours', text="Cours", anchor=W)
        self.tree.heading('td', text="TD", anchor=W)
        self.tree.heading('tp', text="TP", anchor=W)
        self.tree.heading('exam', text="Exam", anchor=W)
        self.tree.heading('departement', text="Departement", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=35)
        self.getsalle()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)

        
    def getsalle(self,x=0):
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)
         ans=''
         self.cur.execute("select * from salle")
         sallelist = self.cur.fetchall()
         for i in sallelist:
              self.tree.insert('', 'end', values=(i))
              if (str(x) == i[0]):
                  a=self.tree.get_children()
                  ans=a[len(a)-1]
         return ans       
  
    def addsalle(self):
        if self.nom.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Nom!")
            return
        elif self.check_exist_salle()>0: 
            messagebox.showinfo("Validation info", "Salle avec le nom {} est deja exist!".format(self.nom.get()))
            return
        else:    
            self.cur.execute("INSERT INTO salle VALUES(NULL,?, ?, ?, ?, ?, ?, ?)",
                      (self.nom.get(),self.capaciter.get(), self.cours.get(), self.td.get(), self.tp.get(), self.exam.get(),self.departement.get()))
            self.base.commit()
            self.getsalle()
            messagebox.showinfo("Validation info", "Salle {} ajouté avec succès".format(self.nom.get()))
            self.claireframe()
        
    def check_exist_salle(self):
        self.cur.execute("SELECT * FROM salle  WHERE nom = ?",
                         (self.nom.get(),))#add "," after
        db_rows1=self.cur.fetchall()
        ls=len(list(db_rows1))
        chekrow = 0
        if 1 <=  ls: 
            chekrow += 1
        return chekrow
            
    def updatesalle(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.nom.set((self.nom.get()).upper())
        if self.nom.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Nom!")
            return
        if(len(li) >= 6):     
            self.cur.execute("update salle set  nom=?, capaciter = ?, cours = ?, td =?, tp =?, exam=?, departement=? where id = ?;",
              (self.nom.get(),self.capaciter.get(), self.cours.get(), self.td.get(), self.tp.get(), self.exam.get(),self.departement.get(),li[0]))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur=self.getsalle(li[0])
            self.tree.selection_set(cur)
            self.claireframe()
        
    def delsalle(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer la salle  sélectionner?") == True and len(li) >= 6:
            self.cur.execute("delete from salle  where id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getsalle()
            self.claireframe()

    def clicktable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 6):
            self.nom.set((li[1]))
            self.capaciter.set((li[2]))
            self.cours.insert(END, li[3])
            self.td.insert(END, li[4])
            self.tp.insert(END, li[5])
            self.exam.insert(END, li[6])
            self.departement.insert(END, li[7])

    def claireframe(self):
        self.nom.set('')
        self.capaciter.set('')
        self.cours.delete(0, END)
        self.td.delete(0, END)
        self.tp.delete(0, END)
        self.exam.delete(0, END)
        self.departement.delete(0, END) 
          
    def rechsalle(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from salle")
        li=self.cur.fetchall() 
        if (self.nom.get() == ''):
            messagebox.showerror("Erreur", "Merci de compléter le champ nom")
            return
        
        for i in li:
            if(i[1]==self.nom.get()):
                self.tree.insert('', 'end', values=(i))        
   
    def importsalle(self):
        xl_file = 'docs/FPO_salles.xlsx'
        table_name = 'salle'
        conn = self.base
        c = self.cur
        df = pd.read_excel(xl_file)
        df.columns = self.get_column_names_from_db_table(c, table_name)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        #conn.close()
        messagebox.showinfo("Validation info", "SQL insert process finished")
        self.getsalle()        

    def get_column_names_from_db_table(self,sql_cursor, table_name):
    
        table_column_names = 'PRAGMA table_info(' + table_name + ');'
        sql_cursor.execute(table_column_names)
        table_column_names = sql_cursor.fetchall()
    
        column_names = list()
    
        for name in table_column_names:
            column_names.append(name[1])
    
        return column_names 





