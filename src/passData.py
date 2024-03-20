import sqlite3

class PassData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.db")

        
    def createUser(self):
        pass

    def createPassword(self):
        pass

    def deleteUser(self):
        pass #! MAKE SURE IT ALSO DELETES ALL THE PASSWORDS ASSOCIATED TO THE SAME USER

    def deletePassword(self):
        pass

    def editPassword(self):
        pass

    def updateUser(self): #* Updating user details incase they get a new email.
        pass

    
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
                owner INTEGER, 
                service TEXT,
                password TEXT,
                locked INTEGER);''')
                #* Supposed to be a boolean value, but SQLite doesn't support bools natively.
                #* So good ol' INT coming to save the day here.
                #* 0 for false, 1 for true.   
        except:
            print("Table 'Passwords' already exists... \n Passing...")
            

        self.db.commit()