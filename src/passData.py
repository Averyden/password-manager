import sqlite3

class PassData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.db")

        
    def getUserFromID(self, id):
        print("Fetching username based on UID...")
        c = self.db.cursor()
        c.execute("""SELECT name FROM Users WHERE id = ?""", [id])
        fetchedUser = c.fetchone()
        print(fetchedUser[0])
        return fetchedUser[0]

    def createUser(self, name="", email="", password=""): #? Maybe encrypt passwords, so they arent in plain text?
        print("Registering new user...")
        c = self.db.cursor()
        c.execute('''INSERT INTO Users (name, email, password) VALUES (?,?,?)''', [name,email,password]) 
        self.db.commit()

    def loginUser(self, userName="", password=""):
        validLogin = False #* Bool to check at the end of function
        print(f"Checking credentials for username {userName}...\n")
        if len(userName) <= 2:
            print("Invalid username...\n")
        
        if len(password) <= 2:
            print("Invalid password requested...\n")

        c = self.db.cursor
        try:
            c.execute("""SELECT name FROM Users WHERE name = ?""", [userName])
        except Exception as e:
            print("User does not exist:", e)

        c.execute("""SELECT password FROM Users WHERE name = ?""", [userName])
        if c.fetchone[0] == password:
            validLogin = True
            print("Valid credentials... \nLogging in...")
        else: 
            print(f"Invalid credentials for user {userName}... \n")
        
        return validLogin
            

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