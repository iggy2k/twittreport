from __future__ import annotations
import os
import tkinter as tk
import retriever
import visualize
import cleaner
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.username = None
        self.setup()

    def setup(self):
        self.parent.title("TwittReport GUI")

        self.parent.protocol("WM_DELETE_WINDOW", self.close)

        # Theme by rdbende
        # https://github.com/rdbende/Forest-ttk-theme
        self.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')

        self.parent.iconbitmap('icon.ico')

        self.parent.geometry('300x250')

        self.parent.resizable(False, False)

        # Start in the center
        w = self.parent.winfo_reqwidth()
        h = self.parent.winfo_reqheight()
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h)
        self.parent.geometry('+%d+%d' % (x, y))

        self.label = tk.Label(self.parent, text="Enter twitter username")
        self.label.pack(pady=(20, 5))

        self.txt = tk.Entry(self.parent, width=15)
        self.txt.pack()

        self.label_validator = tk.Label(
            self.parent, text="...")
        self.label_validator.pack()

        self.button_gen = tk.Button(
            self.parent, text="Generate Report", command=self.generate)
        self.button_gen.pack(pady=(20, 20))

        self.bar = Progressbar(self.parent, length=200,
                               style='black.Horizontal.TProgressbar')
        self.bar.pack()

        self.label_warning = tk.Label(
            self.parent, text="This program is single-threaded, spam-clicking while it is busy can freeze it.", wraplength=300)
        self.label_warning.pack(pady=(10, 0))

    def close(self):
        self.parent.destroy()
        exit()

    def generate(self):
        if self.txt.get() == "":
            self.label_validator['text'] = "No username entered!"
            return 1
        try:
            self.label_validator['text'] = "Retrieving tweets..."
            self.bar['value'] += 25
            self.update()
            retriever.main(self.txt.get())
            self.label_validator['text'] = "Processing tweets..."
            self.bar['value'] += 25
            self.update()
            result = visualize.main()
            self.label_validator['text'] = "Cleaning up..."
            self.bar['value'] += 25
            self.update()
            cleaner.clean()
            self.label_validator['text'] = "Done!"
            self.bar['value'] += 25
            self.update()
            tk.messagebox.showinfo(title="TwittReport",
                                   message="Report saved as {}".format(result))
        except Exception:
            print("Something went wrong!")
        finally:
            self.bar['value'] = 0
            self.update()
            cleaner.clean()


if __name__ == '__main__':

    root = tk.Tk()
    run = App(root)
    root.mainloop()
