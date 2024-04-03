import sqlite3
import json

try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.db")

        self.loginIssue = "" #* Set to a global var so it can be called from the main code.

        
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
        self.loginIssue = "" #* String to return incase logging in fails.
        print(f"Checking credentials for username {userName}...\n")
        if len(userName) <= 2:
            self.loginIssue = "Please provide a valid username."
            print("Invalid username...\n")
            if len(userName) == 0:
                self.loginIssue = "Please provide a username."
                print("No username submitted...\n")
                return self.loginIssue
            return self.loginIssue
            
        if len(password) <= 2:
            self.loginIssue = "Please provide a valid password."
            print("No password provided...\n")
            if len(password) == 0:
                self.loginIssue = "Please provide a password."
                print("Invalid password requested...\n")
                return self.loginIssue
            return self.loginIssue

        c = self.db.cursor()
        try:
            c.execute("""SELECT name FROM Users WHERE name = ?""", [userName])
            fetchedName = c.fetchone()

            if fetchedName is not None: #! Username is correct, move on to checking the password.
                c.execute("""SELECT password FROM Users WHERE name = ?""", [userName])
                fetchedPass = c.fetchone()
                
                if fetchedPass is not None and fetchedPass[0] == password: #! Password is correct, and exists, move on.
                    c.execute("""SELECT id FROM Users WHERE name = ?""", [userName])
                    fetchedID = c.fetchone()

                    if fetchedID is not None: #! the UID does exist, now write to JSON file.
                        validLogin = True
                        lastLoggedUser["LastLogDict"]["Loggedin"] = True
                        lastLoggedUser["LastLogDict"]["lastLoggedUser"] = fetchedID[0]
                        print("Valid credentials... \nLogging in...")

                    else: 
                        print(f"Failed to retrieve user ID for {userName}...")
                        self.loginIssue = "Error while logging in."
                else:
                    print(f"Invalid credentials for user {userName}... \n")
                    self.loginIssue = "Invalid username or password."
            else:
                print("User does not exist.")
                self.loginIssue = "Invalid username or password."

        except Exception as e:
            print("Error during login:", e)

        with open("assets/lastLogin.json", "w") as lastLogin:
            json.dump(lastLoggedUser, lastLogin, indent=4)
        
        return validLogin, self.loginIssue
            

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