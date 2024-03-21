import tkinter as tk
import tkinter.ttk as ttk

class PassManager(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("AAAAAAB")
        self.buildUIStart1()

    def buildUIStart1(self):
        self.label = ttk.Label(self, text="Hello, world!")
        self.label.grid(column=0, row=0)

root = tk.Tk()
app = PassManager(root)
app.mainloop()
