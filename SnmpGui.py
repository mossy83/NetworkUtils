#!/bin/bash python
from tkinter import *
from pysnmp.hlapi import *

def SnmpGui():
    root = Tk()
    root.geometry("640x640+0+0")
    root.title("Switch Port Availablity")

    ipLabel = Label(root, text="IP/DNS Name: ").grid(row=0, sticky=E)
    daysLabel = Label(root, text="Days Down: ").grid(row=1, sticky=E)

    ipEntry = Entry(root).grid(row=0, column=1)
    daysEntry = Entry(root).grid(row=1, column=1)

    root.mainloop()

def main():
    SnmpGui()

if __name__ == '__main__':
    main()
