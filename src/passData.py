import sqlite3

class passData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.py")

        
    def createTables(self):
        c = self.db.cursor()
        try: 
            c.execute('''
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                password TEXT);
            ''')
        except:
            print("Table 'Users' already exists... \n Passing...")

        try: #* Table to store each user's passwords
            c.execute('''
            CREATE TABLE Passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner INT, 
                SERVICE TEXT,
                password TEXT,
                locked INT);
                #* Supposed to be a boolean value, but SQLite doesn't support bools natively.
                #* So good ol' INT coming to save the day here.
                #* 0 for false, 1 for true.
            ''')
        except:
            print("Table 'Passwords' already exists... \n Passing...")
            

        self.db.commit()