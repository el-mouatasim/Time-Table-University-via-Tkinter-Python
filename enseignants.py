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

class EnsWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1280, 650
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
        self.mainframe = LabelFrame(self.add_prod_win, width=1200, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        self.buve.menu.add_command(label="Import le fichier excel",command=self.importprof)
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
        self.buve1.menu.add_command(label="Supprimer tout",command=self.delallprof)
        
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
        # intial para
        #self.max_rand_value = 9 # Max bounds for random int, increases every level
        self.user_level = 1  # Users current level
        self.current_correctness = 3  # Current consecutive questions correct (starts at 3 if goes to 6 up 1 level if down to 0 down 1 level)
       
        ####
        mFrame1 = LabelFrame(self.add_prod_win, text = 'Informations sur Enseignant',width=910, height=200)
        mFrame1.place(x=50,y=40)
        Label(mFrame1, text = 'Nom : ', font=('Orbitron', 15)).place(x=10, y=50,height = 30)
        self.nom = StringVar()
        x1=myentry(mFrame1, textvariable=self.nom,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15))
        x1.place(x=110, y=50,height = 30)
        self.cur.execute("select nom from enseignant")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        x1.set_completion_list(a)
        Label(mFrame1, text = 'Tel :', font=('Orbitron', 15)).place(x=330, y=50,height = 30)
        self.tel = StringVar()
        Entry(mFrame1, textvariable=self.tel, width=18, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=375, y=50,height = 30) 
        Label(mFrame1, text = 'Email :', font=('Orbitron', 15)).place(x=580, y=50,height = 30)
        self.email = StringVar()
        Entry(mFrame1, textvariable=self.email, width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=645, y=50,height = 30) 
        
        Label(mFrame1, text = 'Spécialité :', font=('Orbitron', 15)).place(x=10, y=100,height = 30)
        self.specialite = StringVar()
        Entry(mFrame1, textvariable=self.specialite,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=110, y=100,height = 30)
      
        Label(mFrame1, text = 'Grade :', font=('Orbitron', 15)).place(x=360, y=100,height = 30)
        self.grade = Combobox(mFrame1, width=10)
        self.grade['values'] = ('',
                                    'PA',
                                    'PH',
                                    'PES',
                                    'AUTRE')
        self.grade.current(0)  # set the selected item
        self.grade.place(x=440, y=100,height = 30)        
        Label(mFrame1, text = 'Bureau :', font=('Orbitron', 15)).place(x=510, y=100,height = 30) 
        self.bureau = Combobox(mFrame1, width=10)
        self.bureau['values'] = ('',
                                    'D1-B',
                                    'D2-B',
                                    'D3-B',
                                    'D4-B',
                                    'D5-B',
                                    'D6-B',
                                    'AUTRE')
        self.bureau.current(0)  # set the selected item
        self.bureau.place(x=590, y=100,height = 30)  
        Label(mFrame1, text = 'Département :', font=('Orbitron', 15)).place(x=690, y=100,height = 30)
        self.departement = Combobox(mFrame1, width=10)
        self.departement['values'] = ('',
                                    'MIG',
                                    'PC',
                                    'LASH',
                                    'AUTRE')
        self.departement.current(0)  # set the selected item
        self.departement.place(x=810, y=100,height = 30)                        

                              
        mFrame = Frame(self.add_prod_win,width=800, height=600)
        mFrame.place(x=50,y=250)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',
         'Nom', 'tel', "email", 'specialite','grade','bureau','departement'), 
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
        self.tree.heading('tel', text="Tel", anchor=W)
        self.tree.heading('email', text="Email", anchor=W)
        self.tree.heading('specialite', text="Spécialité", anchor=W)
        self.tree.heading('grade', text="Grade", anchor=W)
        self.tree.heading('bureau', text="Bureau", anchor=W)
        self.tree.heading('departement', text="Département", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        self.getprof()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)

        
    def getprof(self,x=0):
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)
         ans=''
         self.cur.execute("select * from enseignant")
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
        elif self.check_exist_prof()>0: 
            messagebox.showinfo("Validation info", "L'Enseignant avec le nom {} est deja exist!".format(self.nom.get()))
            return
        else:    
            self.cur.execute("INSERT INTO enseignant VALUES(NULL,?, ?, ?, ?, ?, ?, ?)",
                      (self.nom.get(),self.tel.get(), self.email.get(), self.specialite.get(), self.grade.get(), self.bureau.get(),self.departement.get()))
            self.base.commit()
            self.getprof()
            messagebox.showinfo("Validation info", "Enseignant {} ajouté avec succès".format(self.nom.get()))
            self.claireframe()
        
    def check_exist_prof(self):
        self.cur.execute("SELECT * FROM enseignant  WHERE nom = ?",
                         (self.nom.get(),))#add "," after
        db_rows1=self.cur.fetchall()
        ls=len(list(db_rows1))
        chekrow = 0
        if 1 <=  ls: 
            chekrow += 1
        return chekrow
            
    def updateprof(self):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        self.nom.set((self.nom.get()).upper())
        if self.nom.get() == '':
            messagebox.showerror("Erreur", "Merci de compléter le champ Nom!")
            return
        if(len(li) >= 6):     
            self.cur.execute("update enseignant set  nom=?, tel = ?, email = ?, specialite =?, grade =?, bureau=?, departement=? where id = ?;",
              (self.nom.get(),self.tel.get(), self.email.get(), self.specialite.get(), self.grade.get(), self.bureau.get(),self.departement.get(),li[0]))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            cur=self.getprof(li[0])
            self.tree.selection_set(cur)
            self.claireframe()
        
    def delprof(self):
        cur = self.tree.focus()
        cur = self.tree.item(cur)
        li = cur['values']
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer l'enseignant  sélectionner?") == True and len(li) >= 6:
            self.cur.execute("delete from enseignant  where id = ?;", (li[0],))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getprof()
            self.claireframe()

    def delallprof(self):
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer tout enseignants de département {}?".format(self.departement.get())) == True :
            self.cur.execute("delete from enseignant where departement = ?;", (self.departement.get(),))
            self.base.commit()
            self.tree.delete(*self.tree.get_children())
            self.getprof()
            
    def clicktable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 6):
            self.nom.set((li[1]))
            self.tel.set((li[2]))
            self.email.set((li[3]))
            self.specialite.set((li[4]))
            self.grade.insert(END, li[5])
            self.bureau.insert(END, li[6])
            self.departement.insert(END, li[7])

    def claireframe(self):
        self.nom.set('')
        self.tel.set('')
        self.email.set('')
        self.specialite.set('')
        self.grade.delete(0, END)
        self.bureau.delete(0, END)
        self.departement.delete(0, END) 
          
    def rechprof(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("select * from enseignant")
        li=self.cur.fetchall() 
        if (self.nom.get() == ''):
            messagebox.showerror("Erreur", "Merci de compléter le champ nom")
            return
        
        for i in li:
            if(i[1]==self.nom.get()):
                self.tree.insert('', 'end', values=(i))        
    def importprof(self):
        xl_file =  filedialog.askopenfilename(initialdir = "./docs",title = "Select file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
        table_name = 'enseignant'
        conn = self.base
        c = self.cur
        df = pd.read_excel(xl_file)
        df.columns = self.get_column_names_from_db_table(c, table_name)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        #conn.close()
        messagebox.showinfo("Validation info", "SQL insert process finished")
        self.getprof()        

    def get_column_names_from_db_table(self,sql_cursor, table_name):
    
        table_column_names = 'PRAGMA table_info(' + table_name + ');'
        sql_cursor.execute(table_column_names)
        table_column_names = sql_cursor.fetchall()
    
        column_names = list()
    
        for name in table_column_names:
            column_names.append(name[1])
    
        return column_names 



