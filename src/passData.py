import sqlite3
import json
import re

try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassData():
    def __init__(self):
        self.db = sqlite3.connect("assets/passData.db")

        self.accountIssue = "" #* Set to a global var so it can be called from the main code.
        self.validMasterPass = False #* No need to let someone in despite program just being launched.

        
    def getUserFromID(self, id):
        print("Fetching username based on UID...")
        c = self.db.cursor()
        c.execute("""SELECT name FROM Users WHERE id = ?""", [id])
        fetchedUser = c.fetchone()
        print(fetchedUser[0])
        return fetchedUser[0]

    def getCredentialsForService(self, service, uID):
        c = self.db.cursor()
        c.execute("""SELECT username, password FROM Passwords WHERE service = ? AND owner = ?""", (service, uID))
        credentials = c.fetchone()
        if credentials:
            return credentials
        else:
            print(f"No credentials found for service: {service}")
            return None


    def getSavedPasswordWebsites(self, id): #* function to return the websites that the user has saved their passwords for.
        c = self.db.cursor()
        c.execute("""SELECT service FROM Passwords WHERE owner = ?""", [id])

        services = []
        for service in c.fetchall():
            print(service[0])
            services.append((service[0]))

        return services


    def checkMasterPassword(self, UID="", enteredPassword=""):
        self.validMasterPass = False #* Reset it just in case.

        c = self.db.cursor()
        try:
            c.execute('''SELECT password FROM Users WHERE id = ?''', [UID])
            fetchedPassword = c.fetchone()
            if fetchedPassword != None:
                if fetchedPassword[0] == enteredPassword:
                    self.validMasterPass = True
                    print("Thingy worky")
        except Exception as e:
            print("Error while trying master password: \n", e)

    def createUser(self, name="", email="", password="", confirmation=""): #? Maybe encrypt passwords, so they arent in plain text?
        print("Registering new user...")
        validCreation = False #* False by default
        self.accountIssue = "" #* String to return to main program.
        if len(name) <= 2:
            self.accountIssue = "Username must be longer than two characters."
            print("Invalid username provided for registration... \n")
            if len(name) == 0:
                self.accountIssue = "Please provide a username."
                print("No username provided for registration...\n")
                return self.accountIssue
            return self.accountIssue

        #* Check username for special characters and/or spaces.
        if not re.match(r"^\S+$", name):
            self.accountIssue = "Username must not contain special characters."
            print("Invalid username containing special characters... \n")
            return self.accountIssue
        
        if len(password) <= 2:
            self.accountIssue = "Password must be longer than two characters."
            print("Invalid password provided...\n")
            if len(password) == 0:
                self.accountIssue = "Please provide a password."
                print("No password provided...\n")
                return self.accountIssue
            return self.accountIssue

        #* Make a check to see if the confirmed password is the same as the password
        if confirmation != password:
            self.accountIssue = "Passwords do not match."
            print("Invalid confirmation...\n")
            return self.accountIssue

        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            self.accountIssue = "Please provide a valid email address."
            print("Invalid email address provided...\n")
            return self.accountIssue

        if len(email) == 0:
            self.accountIssue = "Please provide an email address."
            print("No email address provided...\n")
            return self.accountIssue

        c = self.db.cursor()
        #* check username occupancy
        try:
            c.execute('''SELECT name FROM Users WHERE name = ?''', [name])
            fetchedName = c.fetchone()

            if fetchedName is not None:
                self.accountIssue = "Username is already in use."
                print(f"Username '{name}' is already occupied...\n")
                return self.accountIssue
            else:
                validCreation = True

            c2 = self.db.cursor()
            c2.execute('''SELECT email FROM Users WHERE email = ?''', [email])
            fetchedMail = c2.fetchone()
            if fetchedMail is not None:
                self.accountIssue = "Email is already in use."
                print(f"Email '{email}' is already occupied...\n")
                return self.accountIssue
        
        except Exception as e:
            print("Error during registration:", e)
        
        if validCreation == True:
            c.execute('''INSERT INTO Users (name, email, password) VALUES (?,?,?)''', [name,email,password]) 
            self.db.commit()
            print("created user")

            self.loginUser(userName=str(name), password=str(password))

            

    def loginUser(self, userName="", password=""):
        validLogin = False #* Bool to check at the end of function
        self.accountIssue = "" #* String to return incase logging in fails.
        print(f"Checking credentials for username {userName}...\n")
        if len(userName) <= 2:
            self.accountIssue = "Please provide a valid username."
            print("Invalid username...\n")
            if len(userName) == 0:
                self.accountIssue = "Please provide a username."
                print("No username submitted...\n")
                return self.accountIssue
            return self.accountIssue
            
        if len(password) <= 2:
            self.accountIssue = "Please provide a valid password."
            print("No password provided...\n")
            if len(password) == 0:
                self.accountIssue = "Please provide a password."
                print("Invalid password requested...\n")
                return self.accountIssue
            return self.accountIssue

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

                        with open("assets/lastLogin.json", "w") as lastLogin:
                            json.dump(lastLoggedUser, lastLogin, indent=4)  

                    else: 
                        print(f"Failed to retrieve user ID for {userName}...")
                        self.accountIssue = "Error while logging in."
                else:
                    print(f"Invalid credentials for user {userName}... \n")
                    self.accountIssue = "Invalid username or password."
            else:
                print("User does not exist.")
                self.accountIssue = "Invalid username or password."

        except Exception as e:
            print("Error during login:", e)
        
        return validLogin, self.accountIssue
            

    def createPassword(self, password="", owner="", service="", username=""):
        print("Creating new password for user...")
        if owner == 0:
            print("Can't create new password. \n \nOwner value can't be of null.")
        else:
            if not re.match(r"^\S+$", service): #* If theres any sort of special characters in there.
                self.accountIssue = "Please avoid using spaces and/or special characters in service name."
                return self.accountIssue    

            elif len(service) <= 1 or len(service) >= 21: #* Add an arbitrary character limit, to prevent overflow.
                self.accountIssue = "If the name of the service you're using is longer than 21 characters: \nplease provide a nickname for the service."
                return self.accountIssue
            elif len(username) <= 2 or len(username) > 20:
                self.accountIssue = "Please provide a username between 3 and 20 characters."
                return self.accountIssue
            elif len(password) <= 2 or len(password) > 32: #* Allow password to be longer than username, as the password should be the most secure bit.
                self.accountIssue = "Make sure your password is between 3 and 32 characters."
            else:
                c = self.db.cursor()
                c.execute('''INSERT INTO Passwords (owner, service, password, username) VALUES (?,?,?,?)''', [owner, service, password, username])
                self.db.commit()

    def deleteUser(self):
        pass #! MAKE SURE IT ALSO DELETES ALL THE PASSWORDS ASSOCIATED TO THE SAME USER

    def deletePassword(self, service):
        #? Should I really need to implement some sort of check here?
        #! Nah fuck it, we ball.
        print("Attempting to delete selected password")
        c = self.db.cursor()
        c.execute('''DELETE FROM Passwords WHERE service = ?''', [service])
        print("Deleted it")
        self.db.commit()
    
    def updateDetailsForService(self): #* For when the exam is over, ill work on implementing this
        pass
  
    def editMPassword(self):
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
                username TEXT);''')  
        except:
            print("Table 'Passwords' already exists... \nPassing...")
            

        self.db.commit()