import tkinter as tk
import tkinter.ttk as ttk
import json
import requests, hashlib, time #* All these libraries are for sending and receiving data to the haveibeenpwned API.
#? Although the time library is just to show and hide the result in the ui after five seconds.
from passData import PassData


try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassManger(tk.Frame):  
    def __init__(self):
        tk.Frame.__init__(self)
        self.showingPassword = False
        
        self.data = PassData(self)

        self.data.createTables()

        self.updateLoginWindow()


    def updateLabels(self):

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        #? There might be, not bothered to look for it tho :)
        #! this exact one must be kept, as it breaks if i try to incorporate the function into replacing this one here.
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)
            
            try:
                self.lblAccountIssue.configure(text=f"{self.data.accountIssue}")
            except:
                pass

            if lastLoggedUser["LastLogDict"]["Loggedin"] == True: #* If user is logged in
                self.lblSlct.configure(text=f"Welcome, {self.data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])}.")
                try:
                    self.lblMainAccount.configure(text=f"{self.data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])}'s password vault.")

                    services = self.data.getSavedPasswordWebsites(lastLoggedUser['LastLogDict']['lastLoggedUser'])
                    self.serviceView.delete(*self.serviceView.get_children())
                    self.clearPasswordButtons()
                    self.lblSlctService.config(text = "No selected password.")
                    self.lblSlctUN.config(text="")
                    self.lblSlctPass.config(text="")
                    for service in services:
                        self.serviceView.insert("", tk.END, values=service)
                except Exception as e:
                    print("Exception occurred under label updating:", e)


    
    def updateLoginWindow(self):

        
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        print(f"Update label says: {lastLoggedUser['LastLogDict']['Loggedin']}")
        if lastLoggedUser["LastLogDict"]["Loggedin"] == True:
            self.loggedInNoVaultWindow()
        else:
            self.buildUIStart1() #! Build login window based on user login status.
        

    def clearSettingsWindow(self):
        for widget in self.settingsWindow.winfo_children():
            widget.pack_forget()

    def alzheimers(self):
        for widget in self.winfo_children():
            widget.grid_forget() #? Should clear all widgets? spoiler alert: IT DOES 🥹

    def logOut(self):
        lastLoggedUser["LastLogDict"]["Loggedin"] = False
        lastLoggedUser["LastLogDict"]["lastLoggedUser"] = "0"
        
        with open("assets/lastLogin.json", "w") as lastLogin:
            json.dump(lastLoggedUser, lastLogin, indent=4)
        
        self.updateLoginWindow()

    def onPasswordSelect(self, event):
        
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if len(curItem) > 0:
            self.clearPasswordButtons()
            service = curItem[0]
            #* Reopen the JSON file so that it can actually read things when the user logged in for the first time, else the UID is set to none
            #* Which isnt really very good.
            with open("assets/lastLogin.json") as lastLogin:
                lastLoggedUser = json.load(lastLogin)
            uID = lastLoggedUser['LastLogDict']['lastLoggedUser']
            credentials = self.data.getCredentialsForService(service, uID)
            if credentials:
                username, password = credentials
                self.lblSlctService.config(text = 'Currently selected service: {}'.format(curItem[0]))
                self.lblSlctUN.config(text=f"Username: {username}")
                self.lblSlctPass.config(text="Password: " + "\u2022" * len(password))

                self.btnCheck = ttk.Button(self.Frame, text="Check breaches", command=self.sendPasswordCheck)
                self.btnCheck.grid(row=4, column=1, padx=(0,250))

                self.btnShow = ttk.Button(self.Frame, text="Show", command=self.togglePasswordVisibility)
                self.btnShow.grid(row=4, column=1, padx=(250,250))

                self.btnCopy = ttk.Button(self.Frame, text="Copy to clipboard", command=self.copyPasswordToClip)
                self.btnCopy.grid(row=4, column=1, padx=(250,0))
            else:
               print("No credentials found for selected thingy.")

    def clearPasswordButtons(self):
        #* So that the buttons do not layer over eachother.
        if hasattr(self, 'btnCheck'):
            self.btnCheck.destroy()
        if hasattr(self, 'btnShow'):
            self.btnShow.destroy()
        if hasattr(self, 'btnCopy'):
            self.btnCopy.destroy()

    #! Functions for the password buttons go here:

    def togglePasswordVisibility(self):
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if curItem:
            service = curItem[0]
            with open("assets/lastLogin.json") as lastLogin:
                lastLoggedUser = json.load(lastLogin)

            uID = lastLoggedUser['LastLogDict']['lastLoggedUser']
            credentials = self.data.getCredentialsForService(service, uID)
            if credentials:
                if self.showingPassword == False:
                    self.showingPassword = True
                    username, password = credentials
                    self.lblSlctPass.config(text=f"Password: {password}")
                    self.btnShow.config(text="Hide", command=self.togglePasswordVisibility)
                elif self.showingPassword == True:
                    self.showingPassword = False
                    username, password = credentials
                    self.lblSlctPass.config(text="Password: " + "\u2022" * len(password))
                    self.btnShow.config(text="Show", command=self.togglePasswordVisibility)
            else:
                print("No credentials found for selected service.")


    def copyPasswordToClip(self): #* Function for copying the password to the user's clipboard
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if curItem:
            service = curItem[0]
            with open("assets/lastLogin.json") as lastLogin:
                lastLoggedUser = json.load(lastLogin)

            uID = lastLoggedUser["LastLogDict"]["lastLoggedUser"]
            credentials = self.data.getCredentialsForService(service, uID)
            if credentials: #* Check if something got fetched.
                username, password = credentials 
                #* We wont be using the username variable, but we will but using the password.
                #* Username is called so that we can also retrieve the password
                #* I suck at coding KEK

                #* Clear clipboard
                self.clipboard_clear()
                #* Insert password into clipboard
                self.clipboard_append(password)
                self.update() #* Apply changes
                print(f"Put password into clipboard: {password}")
            else:
                print("No password was found to be able to be copied.")
        else: 
            print("What the fuck are you doing buddy.")

    def sendPasswordCheck(self):
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if curItem:
            service = curItem[0]
            with open("assets/lastLogin.json") as lastLogin:
                lastLoggedUser = json.load(lastLogin)

            uID = lastLoggedUser["LastLogDict"]["lastLoggedUser"]
            credentials = self.data.getCredentialsForService(service, uID)
            if credentials: 
                username, password = credentials 

                # Check for breaches
                numBreaches = self.checkPasswordForBreaches(password)
                
                # Update label with breach information
                if numBreaches > 0:
                    self.lblAPIResponse.config(text=f"This password has been found in {numBreaches} breaches. \nIt is recommended you change your password now.")  
                else:
                    self.lblAPIResponse.config(text="This password has not been found in any breaches.")
                self.after(5000, lambda: self.lblAPIResponse.config(text=""))
            else: 
                print("No password was found for the selected service.")
        else: 
            print("No service selected.")



    def checkPasswordForBreaches(self, password):
        sha1password = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1password[:5], sha1password[5:]

        #* Send request to API
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

        #* Check whether or not the response was a success.
        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.startswith(suffix):
                    return int(line.split(":")[1])
            return 0
        else:
            print(f"Error: {response.status_code}")

    #! other functions continue here.

    def sendDeletePassRequest(self): #* Fetch currently selected service, and send it to the database to get wiped.
        curItem = self.serviceView.item(self.serviceView.focus())['values']
        if curItem:
            service = curItem[0]
            self.data.deletePassword(service)
            self.updateLabels()

    def sendLoginDetails(self):
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        self.data.loginUser(userName=usernameToSend, password=passwordToSend)
    
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        if len(self.data.accountIssue) != 0: #* Failed login, update labels to maintain user info on entries and display error msg.
            self.updateLabels()
        else: #* Successful login, update the entire window.
            self.buildMainWindow() #* We just logged in, no need to retype pasword
            #self.updateLoginWindow()
            self.passwordEntry.delete(0, tk.END) #* Clear the entry so that it doesnt carry over Buhh
            self.userNameEntry.delete(0, tk.END)

        print(f"Sender says: {lastLoggedUser['LastLogDict']['Loggedin']}")


    def sendVaultUnlockRequest(self):
        passwordToTry = self.entryMPass.get()
        self.entryMPass.delete(0, tk.END) #* Clear the entry

        #* Reopen the file to read the updated content 
        #! WHY ISNT THERE A BETTER WAY TO DO THIS 😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭😭
        
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        self.data.checkMasterPassword(UID=lastLoggedUser['LastLogDict']['lastLoggedUser'], enteredPassword=passwordToTry)
        print(self.data.validMasterPass)
        
        #* Check whether or not the master password was a success utilizing the variabel in the self.data code.
        if self.data.validMasterPass == True:
            self.buildMainWindow()
            self.data.accountIssue = "" #* Reset accountIssue var incase user got the password wrong first try.
        else:
            self.data.accountIssue = "Invalid master password."
            self.updateLabels()
         #* Parse user ID and entered master password to send to the database.

    def sendPassCreationDetails(self): #! For creating the service with the password
        #* Reopen the file to read the updated content 
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

        userID = lastLoggedUser['LastLogDict']['lastLoggedUser']
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        serviceToSend = self.serviceEntry.get()
      

        self.data.createPassword(password=passwordToSend, owner=userID, service=serviceToSend, username=usernameToSend)
        if len(self.data.accountIssue) != 0: #* if there is an issue, stop code in its tracks.abs
            self.updateLabels()
        else:
            self.buildMainWindow() #* Send user back, so there is an indication they created their password.
            self.passwordEntry.delete(0, tk.END)
            self.serviceEntry.delete(0, tk.END) 
            self.userNameEntry.delete(0, tk.END)

    def sendCreationDetails(self): #! To create the user
        usernameToSend = self.userNameEntry.get()
        passwordToSend = self.passwordEntry.get()
        confirmationToSend = self.rptPassEntry.get()
        emailToSend = self.emailEntry.get()

        self.data.createUser(name=usernameToSend, email=emailToSend, password=passwordToSend, confirmation=confirmationToSend)

        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)
    
        if len(self.data.accountIssue) != 0: #* Failed login, update labels to maintain user info on entries and display error msg.
            self.updateLabels()
        else: #* Successful login, update the entire window.
            self.buildMainWindow() #* no need to send the user the the master password window, just let them through.
            #* clear entries only here, or else the user will be forced to retype EVERYTHING instead of just retrying the thing that errored.
            self.passwordEntry.delete(0, tk.END)
            self.userNameEntry.delete(0, tk.END)
            self.rptPassEntry.delete(0, tk.END)
            self.emailEntry.delete(0, tk.END)

        print(f"Sender says: {lastLoggedUser['LastLogDict']['Loggedin']}")

    #! CONTINUING FORTH IS THE BUILDING OF ALL THE UIS
    #! This code is about to get messy really quickly
    #! Such is the code of ui building
    #! 😔

    def buildUIStart1(self): 
        try:
            self.alzheimers()
        except:
            print("Called from deletion request, clearing both things")
            self.settingsWindow.destroy()
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

        self.lblPass = ttk.Label(self.Frame, text="Master password")
        self.lblPass.grid(row=5, column=0, columnspan=2)

        self.passwordEntry = ttk.Entry(self.Frame, text="Password", show="\u2022") #! u2022 is for the bullet symbol to hide the user's password.and
        #? Maybe incorporate a "show" button?
        #? Depends on if TKinter allows that.
        self.passwordEntry.grid(row=6, column=0, columnspan=2)

        self.lblRptPass = ttk.Label(self.Frame, text="Confirm master password")
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
        self.lblSlctUN.grid(column=1, row=2)

        self.lblSlctPass = ttk.Label(self.Frame, text="")
        self.lblSlctPass.grid(column=1, row=3)

        self.lblAPIResponse = ttk.Label(self.Frame, text="")
        self.lblAPIResponse.grid(column=1, row=5, pady=1)

        self.btnAddPassword = ttk.Button(self.Frame, text="+", command=self.buildServiceAddition)
        self.btnAddPassword.grid(column=0, row=7, pady=3, padx=(0,100))

        self.btnDelPassword = ttk.Button(self.Frame, text="-", command=self.sendDeletePassRequest)
        self.btnDelPassword.grid(column=0, row=7, padx=(100,0))

        self.btnLockVault = ttk.Button(self.Frame, text="Lock vault", command=self.loggedInNoVaultWindow)
        self.btnLockVault.grid(column=1, row=7, padx=(100, 20))

        self.btnUserSettings = ttk.Button(self.Frame, text="User Settings", command=self.openUserSettings)
        self.btnUserSettings.grid(column=1, row=7, padx=(0, 100))

        self.pack()
        self.updateLabels()


    def openUserSettings(self):
        with open("assets/lastLogin.json") as lastLogin:
            lastLoggedUser = json.load(lastLogin)

            
        try:
            self.clearSettingsWindow() # Replace it in case its being called from cancel buttons.
        except: 
            print("UI already doesn't exist already...\nso we create a new instance of it.") #* thank you C# :DD
            self.settingsWindow = tk.Toplevel(self)
            self.settingsWindow.title("User Settings")

        foundUser = self.data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])

        lblUserSettings = ttk.Label(self.settingsWindow, text=f"User Settings for account: {foundUser}")
        lblUserSettings.pack(pady=10, padx=50)

        btnEditDetails = ttk.Button(self.settingsWindow, text="Edit Details [Soon]")  # Implement the command as needed
        btnEditDetails.pack(pady=5)

        btnDeleteAccount = ttk.Button(self.settingsWindow, text="Delete Account", command=self.confirmDeleteAccount)
        btnDeleteAccount.pack(pady=5)

        btnClose = ttk.Button(self.settingsWindow, text="Close", command=self.settingsWindow.destroy)
        btnClose.pack(pady=20)

    def confirmDeleteAccount(self):
        self.clearSettingsWindow()
        foundUser = self.data.getUserFromID(lastLoggedUser['LastLogDict']['lastLoggedUser'])

        foundUID = lastLoggedUser['LastLogDict']['lastLoggedUser'] # We fetch the UID so that we dont have to do shitty bloated logic in the database.

        self.lblConfirmation = ttk.Label(self.settingsWindow, text=f"Are you sure you want to delete your account, {foundUser}?")
        self.lblConfirmation.pack(pady=10)

        self.btnYes = ttk.Button(self.settingsWindow, text="Delete account", command=lambda: self.data.deleteUser(foundUID))
                                
        self.btnYes.pack(pady=5)

        self.btnCancel = ttk.Button(self.settingsWindow, text="Cancel", command=self.openUserSettings)
        self.btnCancel.pack(pady=5)


    def buildServiceAddition(self):
        self.alzheimers()
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        self.lblSlct = ttk.Label(self.Frame, text="Add password to vault")
        self.lblSlct.grid(column=0, row=0, columnspan=2)

        self.lblSrvice = ttk.Label(self.Frame, text="Name of service")
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

        self.lblAccountIssue = ttk.Label(self.Frame, text="")
        self.lblAccountIssue.grid(row=7, column=0, columnspan=2)

        self.btnLogin = ttk.Button(self.Frame, text="Add to vault", command=self.sendPassCreationDetails) 
        self.btnLogin.grid(row=8, column=0)

        self.btnRegister = ttk.Button(self.Frame, text="Cancel", command=self.buildMainWindow) #! Pass for now, cause that makes sense
        self.btnRegister.grid(row=8, column=1)

        self.pack()

prg = PassManger()
prg.master.title('Password Manager')
prg.mainloop()
