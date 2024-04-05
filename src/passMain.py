import tkinter as tk
import tkinter.ttk as ttk
import json
from passData import PassData
# from uiBuild import BuildFunctions


# builder = BuildFunctions()
data = PassData()

data.createTables()


try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassManger(tk.Frame):  
    def __init__(self):
        tk.Frame.__init__(self)
        
        self.updateLoginWindow()



    def updateLabels(self):

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        #? There might be, not bothered to look for it tho :)
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)
            
            try:
                self.lblAccountIssue.configure(text=f"{data.accountIssue}")
            except:
                pass

            if lastLoggedUser["LastLogDict"]["Loggedin"] == True: #* If user is logged in
                self.lblSlct.configure(text=f"Welcome, {data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])}.")
                try:
                    self.lblMainAccount.configure(text=f"{data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])}'s password vault.")

                    services = data.getSavedPasswordWebsites(lastLoggedUser['LastLogDict']['lastLoggedUser'])
                    self.serviceView.delete(*self.serviceView.get_children())
                    for service in services:
                        self.serviceView.insert("", tk.END, values=service)
                except:
                    print("User is not on their vault...\n \nDon't do anything...")


    
    def updateLoginWindow(self):

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        print(f"Update label says: {lastLoggedUser['LastLogDict']['Loggedin']}")
        if lastLoggedUser["LastLogDict"]["Loggedin"] == True:
            self.loggedInNoVaultWindow()
        else:
            self.buildUIStart1() #! Build login window based on user login status.
        

    def alzheimers(self):
        for widget in self.winfo_children():
            widget.grid_forget() #? Should clear all widgets? spoiler alert: IT DOES 🥹

    def logOut(self):
        lastLoggedUser["LastLogDict"]["Loggedin"] = False
        lastLoggedUser["LastLogDict"]["lastLoggedUser"] = "none"
        
        with open("assets/lastLogin.json", "w") as lastLogin:
            json.dump(lastLoggedUser, lastLogin, indent=4)
        
        self.updateLoginWindow()

    def onPasswordSelect(self):
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if len(curItem) > 0:
            try: 
                self.lblCurrentSelectC.config(text = 'Currently selected action: {}'.format(curItem[0]))
            except:
                print("For some reason it failed.. dunno why")

    def sendLoginDetails(self):
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        data.loginUser(userName=usernameToSend, password=passwordToSend)

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)
    
        if len(data.accountIssue) != 0: #* Failed login, update labels to maintain user info on entries and display error msg.
            self.updateLabels()
        else: #* Successful login, update the entire window.
            self.updateLoginWindow()

        print(f"Sender says: {lastLoggedUser['LastLogDict']['Loggedin']}")

    def sendVaultUnlockRequest(self):
        passwordToTry = self.entryMPass.get()

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        data.checkMasterPassword(UID=lastLoggedUser['LastLogDict']['lastLoggedUser'], enteredPassword=passwordToTry)
        print(data.validMasterPass)
        
        #* Check whether or not the master password was a success utilizing the variabel in the data code.
        if data.validMasterPass == True:
            self.buildMainWindow()
            data.accountIssue = "" #* Reset accountIssue var incase user got the password wrong first try.
        else:
            data.accountIssue = "Invalid master password."
            self.updateLabels()
         #* Parse user ID and entered master password to send to the database.

    def sendPassCreationDetails(self):
        pass

    def sendCreationDetails(self):
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        confirmationToSend = self.rptPassEntry.get()
        emailToSend = self.emailEntry.get()
        data.createUser(name=usernameToSend, email=emailToSend, password=passwordToSend, confirmation=confirmationToSend)

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)
    
        if len(data.accountIssue) != 0: #* Failed login, update labels to maintain user info on entries and display error msg.
            self.updateLabels()
        else: #* Successful login, update the entire window.
            self.updateLoginWindow()

        print(f"Sender says: {lastLoggedUser['LastLogDict']['Loggedin']}")

    #! CONTINUING FORTH IS THE BUILDING OF ALL THE UIS
    #! This code is about to get messy really quickly
    #! Such is the code of ui building
    #! 😔

    def buildUIStart1(self): 
        self.alzheimers()
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

    
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

        self.btnRegister = ttk.Button(self.Frame, text="Create account", command=self.buildRegisterWindow) #! Pass for now
        self.btnRegister.grid(row=6, column=1)
        self.pack()


    def buildRegisterWindow(self):
        self.alzheimers()
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        self.lblSlct = ttk.Label(self.Frame, text="Create account.")
        self.lblSlct.grid(column=0, row=0, columnspan=2)

        self.lblUN = ttk.Label(self.Frame, text="Username")
        self.lblUN.grid(row=1, column=0, columnspan=2)

        self.userNameEntry = ttk.Entry(self.Frame, text="Username")
        self.userNameEntry.grid(row=2, column=0, columnspan=2)


        self.lblEM = ttk.Label(self.Frame, text="Email")
        self.lblEM.grid(row=3, column=0, columnspan=2)

        self.emailEntry = ttk.Entry(self.Frame)
        self.emailEntry.grid(row=4, column=0, columnspan=2)

        self.lblPass = ttk.Label(self.Frame, text="Password")
        self.lblPass.grid(row=5, column=0, columnspan=2)

        self.passwordEntry = ttk.Entry(self.Frame, text="Password", show="\u2022") #! u2022 is for the bullet symbol to hide the user's password.and
        #? Maybe incorporate a "show" button?
        #? Depends on if TKinter allows that.
        self.passwordEntry.grid(row=6, column=0, columnspan=2)

        self.lblRptPass = ttk.Label(self.Frame, text="Confirm password")
        self.lblRptPass.grid(row=7, column=0, columnspan=2)

        self.rptPassEntry = ttk.Entry(self.Frame, text="Confirm Password", show="\u2022")
        self.rptPassEntry.grid(row=8, column=0, columnspan=2)


        self.lblAccountIssue = ttk.Label(self.Frame, text="")
        self.lblAccountIssue.grid(row=9, column=0, columnspan=2)

        self.btnLogin = ttk.Button(self.Frame, text="Create account", command=self.sendCreationDetails) 
        self.btnLogin.grid(row=10, column=0)

        self.btnRegister = ttk.Button(self.Frame, text="Log in to existing account", command=self.buildUIStart1) #! Pass for now
        self.btnRegister.grid(row=10, column=1)

        self.pack()

    def loggedInNoVaultWindow(self):
        print("AAAAA")
        self.alzheimers()
        
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        self.lblSlct = ttk.Label(self.Frame, text="Welcome.. \nif you see this, the update label function failed...")
        self.lblSlct.grid(column=0, row=0, columnspan=2)

        self.lblPlease = ttk.Label(self.Frame, text="Verify your master password to continue.")
        self.lblPlease.grid(column=0, row=1, columnspan=2)

        self.entryMPass = ttk.Entry(self.Frame, show="\u2022")
        self.entryMPass.grid(column=0, row=2, columnspan=2)

        self.btnUnlock = ttk.Button(self.Frame, text="Unlock vault", command=self.sendVaultUnlockRequest)
        self.btnUnlock.grid(column=0, row=4)

        self.btnLogOut = ttk.Button(self.Frame, text="Log out", command=self.logOut)
        self.btnLogOut.grid(column=1, row=4)

        self.lblAccountIssue = ttk.Label(self.Frame, text="")
        self.lblAccountIssue.grid(row=3, column=0, columnspan=2)

        self.pack()
        self.updateLabels()        
    

    def buildMainWindow(self):
        self.alzheimers()

        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        self.lblMainAccount = ttk.Label(self.Frame, text="woops, something went wrong")
        self.lblMainAccount.grid(column=0, row=0, columnspan=2)
        
        self.serviceView = ttk.Treeview(self.Frame, column=("Service"), show='headings')
        self.serviceView.bind("<ButtonRelease-1>", self.onPasswordSelect)
        self.serviceView.heading("#1", text="Service")
        self.serviceView["displaycolumns"]=("Service")
        ysb = ttk.Scrollbar(self, command=self.serviceView.yview, orient=tk.VERTICAL)
        self.serviceView.configure(yscrollcommand=ysb.set)
        self.serviceView.grid(column=0, row=1, rowspan=5, padx=25, pady=5)

        self.lblSlctService = ttk.Label(self.Frame, text="No selected password.")
        self.lblSlctService.grid(column=1, row=1, padx=25)

        self.lblSlctUN = ttk.Label(self.Frame, text="")
        self.lblSlctUN.grid(column=1, row=3)

        self.lblSlctPass = ttk.Label(self.Frame, text="")
        self.lblSlctPass.grid(column=1, row=5)

        self.btnAddPassword = ttk.Button(self.Frame, text="+", command=self.buildServiceAddition)
        self.btnAddPassword.grid(column=0, row=7, pady=3)

        self.btnLockVault = ttk.Button(self.Frame, text="Lock vault", command=self.loggedInNoVaultWindow)
        self.btnLockVault.grid(column=1, row=7)

        self.pack()
        self.updateLabels()


    def buildServiceAddition(self):
        self.alzheimers()
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        self.lblSlct = ttk.Label(self.Frame, text="Add password to vault")
        self.lblSlct.grid(column=0, row=0, columnspan=2)

        self.lblSrvice = ttk.Label(self.Frame, text="Service")
        self.lblSrvice.grid(row=1, column=0, columnspan=2)

        self.serviceEntry = ttk.Entry(self.Frame, text="Service")
        self.serviceEntry.grid(row=2, column=0, columnspan=2)


        self.lblUN = ttk.Label(self.Frame, text="Username")
        self.lblUN.grid(row=3, column=0, columnspan=2)

        self.userNameEntry = ttk.Entry(self.Frame)
        self.userNameEntry.grid(row=4, column=0, columnspan=2)

        self.lblPass = ttk.Label(self.Frame, text="Password")
        self.lblPass.grid(row=5, column=0, columnspan=2)

        self.passwordEntry = ttk.Entry(self.Frame, text="Password", show="\u2022") #! u2022 is for the bullet symbol to hide the user's password.and
        #? Maybe incorporate a "show" button?
        #? Depends on if TKinter allows that.
        self.passwordEntry.grid(row=6, column=0, columnspan=2)

        self.btnLogin = ttk.Button(self.Frame, text="Add to vault", command=self.sendPassCreationDetails) 
        self.btnLogin.grid(row=7, column=0)

        self.btnRegister = ttk.Button(self.Frame, text="Cancel", command=self.buildMainWindow) #! Pass for now
        self.btnRegister.grid(row=7, column=1)

        self.pack()


prg = PassManger()
prg.master.title('Password Manager')
prg.mainloop()
