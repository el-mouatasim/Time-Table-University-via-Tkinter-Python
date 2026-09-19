# importing modules
import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Database():
    """ Connects to Database
        Foreign Key Check=ON
        Key Arguments : None
    """
    def __init__(self):
        # Create a db or connect to one
        self.conn = sqlite3.connect("UTTMA_FPO.db")#if used database_tp.py
        # Enabling foreign key constraints
        #self.conn.execute("PRAGMA foreign_keys = 1")

        # Create cursor
        self.c = self.conn.cursor()
        
    ####=====================METHODS=========================####
            
    #==================== LOGIN ====================================#
        
    def create_login_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                PASSWORD TEXT NOT NULL
            )""")

    def insert_login_table(self):
        with self.conn:
            #self.c.execute("INSERT INTO login VALUES (1, 'firns', 'ufxx|twi')")
            self.c.execute("INSERT INTO login VALUES (1, 'admin', 'password')")
    
    def change_password(self, new_password):
        """Changes Password value from the databse
        Key Arguments: new_password -- String
        """
        with self.conn:
            self.c.execute("UPDATE login SET password = ? WHERE id = 1", (new_password,)) 

    def get_login_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM login")
            result = self.c.fetchone()
            return result   

    #======================== THEME =====================================#

    def create_theme_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE theme (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme_mode TEXT NOT NULL
            )""")
    
    def insert_theme_table(self):
        with self.conn:
            self.c.execute("INSERT INTO theme VALUES (1,'Light Mode')")
    
    def get_theme_value(self):
        with self.conn:
            self.c.execute("SELECT * FROM theme")
            result = self.c.fetchone()
            # print(result)
            return result
    
    def change_theme(self, theme_name):
        """Changes Theme value in Database
        Key Arguments: theme_name 
        theme_name allowed values = (1)Light Mode (2) Dark Mode
         """
        with self.conn:
            self.c.execute("UPDATE theme SET theme_mode = ? WHERE id = 1", (theme_name,))


        
      
    #==================== timetable_tp ====================================#
        
    def create_timetable_tp_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS timetable_tp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indi integer NOT NULL,
                indj integer NOT NULL,
                filiere TEXT NOT NULL,
                semestre str NOT NULL,
                section str,
                groupe str,
                jours TEXT NOT NULL,
                temps str NOT NULL,
                module TEXT NOT NULL,
                prof TEXT NOT NULL,
                local str NOT NULL,
                groupetp str
            )""")
            
    def get_timetable_tp_value(self):
        with self.conn:
            self.c.execute("SELECT filiere, semestre, section, groupe, groupetp FROM timetable_tp")
            result = self.c.fetchall()
            return result
        
    def update_timetable_tp_table(self, Jours, temp, cours, prof,  local, i, j, gfilier, gsemestre, gsection, ggroup, ggroup_tp):
        with self.conn:
            self.c.execute("UPDATE timetable_tp SET jours =?, temps=?, module=?, prof=?, local=?  WHERE indi=? AND indj=? AND filiere=? AND semestre=? AND section =? AND groupe=? AND groupetp =?",
              ( Jours, temp, cours, prof,  local, i, j, gfilier, gsemestre, gsection, ggroup, ggroup_tp))                        
            self.conn.commit()
            
    #==================== distribution ====================================#
        
    def create_distribution_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS distribution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filiere TEXT NOT NULL,
                semestre str NOT NULL,
                section str,
                groupe str,
                groupetp str,
                commun text
            )""")
            
    def insert_distribution_table(self, filiere, semestre, No_section, No_groupe_td, No_groupe_tp, commun):
        with self.conn:
            self.c.execute("INSERT INTO distribution VALUES(NULL,?, ?, ?, ?, ?, ?)",(filiere, semestre, No_section, No_groupe_td, No_groupe_tp,commun) )
            
        self.conn.commit()            
     #==================== module ====================================#
        
    def create_module_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS module (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filiere TEXT NOT NULL,
                semestre str NOT NULL,
                nom str NOT NULL
            )""")
            
    def insert_module_table(self, filiere, semestre, nom):
        with self.conn:
            self.c.execute("INSERT INTO module VALUES (NULL,?,?,?)",(filiere, semestre, nom) )
     #==================== profs ====================================#
        
    def create_profs_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS profs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prof TEXT NOT NULL,
                filiere TEXT NOT NULL,
                semestre str NOT NULL,
                module TEXT NOT NULL
            )""")
            
    def insert_profs_table(self, prof, filiere, semestre, module):
        with self.conn:
            self.c.execute("INSERT INTO profs VALUES (NULL,?,?,?,?)",(prof, filiere, semestre, module) )

     #==================== salle ====================================#
        
    def create_salle_table(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS salle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                capaciter INTEGER
            )""")
            
    def insert_salle_table(self, nom, capaciter):
        with self.conn:
            self.c.execute("INSERT INTO salle VALUES (NULL,?,?)",(nom, capaciter) )


            
############################################################################################################################################

    def drop_table(self, table_name):
        """Drops given table from the Database.
        Key Arguments: table_name -- String
        """
        with self.conn:
            self.c.execute(f"DROP TABLE {table_name}")

    def get_tables(self):
        """get all tables from the Database.
        """
        with self.conn:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            result = self.c.fetchall()#fetchone()
        for i in result:
            print(i)

    def get_columns(self, table_name):
        """Get columns in given table from the Database.
        Key Arguments: table_name -- String
        """
        with self.conn:
            cursor=self.c.execute(f"SELECT * FROM  {table_name}")
            result = cursor.description
        for i in result:
            print(i[0])
            
    def add_column(self, table_name, col_name):
        """Drops given table from the Database.
        Key Arguments: table_name -- String
        """
        with self.conn:
            self.c.execute(f"""
                        ALTER TABLE {table_name} 
                        ADD COLUMN {col_name} 'str'
                        """)
            
        self.conn.commit()
        
if __name__ == "__main__":
    
    db_obj = Database()
    
    #=================== LOGIN ===============================#
    # # Creating login table
    #db_obj.create_login_table()
    
    # # Inserting to login table
    #db_obj.insert_login_table()
    
    
    #====================== THEME =====================================#
    # # Creating theme table
    #db_obj.create_theme_table()
    
    # # Insert to theme table
    #db_obj.insert_theme_table()


    #====================== timetable_tp =====================================#
    # # Creating timetable_tp table
    #db_obj.create_timetable_tp_table()




    #===========================================================#
    # Drop a table
    #db_obj.drop_table("distribution")

    #===========================================================#
    #db_obj.get_tables()
    #db_obj.get_columns("timetable")

    #db_obj.add_column('section')
    #db_obj.add_column('groupetp')

    #db_obj.create_distribution_table()
    #db_obj.create_module_table()

    ##########################################################"


