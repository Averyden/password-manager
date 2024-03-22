import tkinter as tk
import tkinter.ttk as ttk
import json
from passData import PassData

data = PassData()


data.createUser("JEff", "jeff@island.com", "123")

data.getUserFromID(1) #* should fetch jeff

try:
    with open("assets/lastLogin.json") as lastLogin:
        lastLoggedUser = json.load(lastLogin)
except Exception as e:
    print("Error loading JSON:", e)

class PassManger(tk.Frame):  
    def __init__(self):
        tk.Frame.__init__(self)
        # self.root = root
       # self.root.title("TestApp for passDB")
        self.buildUIStart1()

    def toggleLog(self):
        if lastLoggedUser["LastLogDict"]["Loggedin"] == False:
            lastLoggedUser["LastLogDict"]["Loggedin"] = True
        else: 
            lastLoggedUser["LastLogDict"]["Loggedin"] = False

    def buildUIStart1(self): 
        self.Frame = tk.Frame(self)
        self.Frame.grid(column=0, row=0)

        if lastLoggedUser["LastLogDict"]["Loggedin"] == False: #* Check if a user was seen logged in, if not, prompt with buttons
            print("No user found to be logged in since last time running")
            self.lblSlct = ttk.Label(self.Frame, text="Select an option for user handling.")
            self.lblSlct.grid(column=0, row=0, columnspan=2)

            self.btnToggle = ttk.Button(self.Frame, text="Log in", command=self.toggleLog)
        else:
            print("Wow!")
            self.lblSlct = ttk.Label(self.Frame, text="you win")
            self.lblSlct.grid(column=0, row=0, columnspan=2)

            self.btnToggle = ttk.Button(self.Frame, text="Log out", command=self.toggleLog)
        
        self.btnToggle.grid(column=0, row=1, columnspan=2)

        self.pack()

prg = PassManger()
prg.master.title('PasManJSONTest')
prg.mainloop()
