import tkinter as tk
import tkinter.ttk as ttk
 
#* File for building UI, these functions will be called by the main code, as to not make the main code be really weird
class BuildFunctions(ttk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("TestApp for passDB")

        def buildLoginScreen(self):
            self.lblTitle = ttk.Label(text="")