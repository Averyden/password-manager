import tkinter as tk
import tkinter.ttk as ttk
import json
from passData import PassData
from uiBuild import BuildFunctions


builder = BuildFunctions()
data = PassData()

data.createTables()

#data.createUser("JEff", "jeff@island.com", "123")

data.getUserFromID(1) #* should fetch jeff

try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassManger(tk.Frame):  
    def __init__(self):
        tk.Frame.__init__(self)
        self.buildUIStart1()
        self.updateLabels()

    def updateLabels(self):
        try:
            self.lblAccountIssue.configure(text=f"{data.loginIssue}")
        except:
            pass

        if lastLoggedUser["LastLogDict"]["Loggedin"] == True:
            self.lblSlct.configure(text=f"Welcome, {data.getUserFromID(lastLoggedUser['LastLogDict']['Loggedin'])}.")

    def logOut(self):
        lastLoggedUser["LastLogDict"]["Loggedin"] = False
        lastLoggedUser["LastLogDict"]["lastLoggedUser"] = "none"
        
        with open("assets/lastLogin.json", "w") as lastLogin:
            json.dump(lastLoggedUser, lastLogin, indent=4)

    def sendLoginDetails(self):
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        data.loginUser(userName=usernameToSend, password=passwordToSend)
        self.updateLabels()

    def callBuildRegister(self):
        builder.buildRegisterUI()


    def buildUIStart1(self): 
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        if lastLoggedUser["LastLogDict"]["Loggedin"] == False: #* Check if a user was seen logged in, if not, prompt with buttons
            print("No user found to be logged in since last time running")
            self.lblSlct = ttk.Label(self.Frame, text="Please login or create account.")
            self.lblSlct.grid(column=0, row=0, columnspan=2)

            self.lblUN = ttk.Label(self.Frame, text="Username")
            self.lblUN.grid(row=1, column=0, columnspan=2)

            self.userNameEntry = ttk.Entry(self.Frame, text="Username")
            self.userNameEntry.grid(row=2, column=0, columnspan=2)

            self.lblPass = ttk.Label(self.Frame, text="Password")
            self.lblPass.grid(row=3, column=0, columnspan=2)

            self.passwordEntry = ttk.Entry(self.Frame, text="Password", show="\u2022") #! u2022 is for the bullet symbol to hide the user's password.and
            #? Maybe incorporate a "show" button?
            #? Depends on if TKinter allows that.
            self.passwordEntry.grid(row=4, column=0, columnspan=2)

            self.lblAccountIssue = ttk.Label(self.Frame, text="")
            self.lblAccountIssue.grid(row=5, column=0, columnspan=2)

            self.btnLogin = ttk.Button(self.Frame, text="Log in", command=self.sendLoginDetails) 
            self.btnLogin.grid(row=6, column=0)

            self.btnRegister = ttk.Button(self.Frame, text="Create account", command=None) #! Pass for now
            self.btnRegister.grid(row=6, column=1)

        else:
            print("Wow!")
            self.lblSlct = ttk.Label(self.Frame, text="Welcome.. \nif you see this, the update label function failed...")
            self.lblSlct.grid(column=0, row=0, columnspan=2)

            self.btnToggle = ttk.Button(self.Frame, text="Log out", command=self.logOut)
            self.btnToggle.grid(column=0, row=1, columnspan=2)
        
        

        self.pack()

prg = PassManger()
prg.master.title('PasManJSONTest')
prg.mainloop()
