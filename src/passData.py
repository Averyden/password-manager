import sqlite3

class PassData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.db")

        
    def getUserFromID(self, id):
        pass

    def createUser(self, name="", email="", password=""): #? Maybe encrypt passwords, so they arent in plain text?
        print("Registering new user...")
        c.self.db.cursor()
        c.excecute('''INSERT INTO Users (name, email, password) VALUES (?,?,?)''', [name,email,password]) 
        self.db.commit()


    def createPassword(self, password="", owner="", service="", locked=0):
        print("Creating new password for user...")
        if len(owner) == 0:
            print("Can't create new password. \n \nOwner value can't be of null.")
        else:
            c = self.db.cursor()
            c.execute('''INSERT INTO Passwords (owner, service, password, locked) VALUES (?,?,?,?)''', [owner, service, password, locked])
            self.db.commit()

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
            print("Table 'Users' already exists... \nPassing...")

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
            print("Table 'Passwords' already exists... \nPassing...")
            

        self.db.commit()