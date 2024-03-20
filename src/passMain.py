import tkinter as tk
import tkinter.ttk as ttk
from passData import PassData
from uiBuild import BuildFunctions

builder = BuildFunctions()
data = PassData()

class PassManger(ttk.Frame):
    def __init__(self,root):
        self.root = root
        self.root.title("TestApp for passDB")

        self.buildUIStart1()


    def buildUIStart1(self): #* Prompt user with login / register user button
        pass

