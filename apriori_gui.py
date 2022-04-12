from cgitb import text
from email.message import Message
from faulthandler import disable
from fileinput import filename
from os import system
import re
import tkinter as tk
from tkinter import CENTER, END, RAISED, StringVar, filedialog
from turtle import st
from webbrowser import get

from numpy import pad

from apriori import Apriori

def browseFiles():
    global fileName
    fileName = filedialog.askopenfilename(  initialdir = "/", 
                                            title = "Select a File", 
                                            filetypes = (("Text files", "*.txt*"),("all files", "*.*")))
    explore_var.set(fileName)

def submit():
    global minSup, minCon, g_RHS, dataset
    input = dataset_box.get("1.0", END)
    if input!='' : 
        fileName = 'input_data.csv'
        newFile = open('input_data.csv','w+')
        print(input, file=newFile)
        newFile.close()
    if support_var.get()!='' : minSup = float(support_var.get())
    if confidence_var.get()!='' : minCon = float(confidence_var.get())
    if rhs_var.get()!='' : g_RHS = frozenset([rhs_var.get()])
    dataset = fileName
    root.destroy()

root=tk.Tk()
root.geometry("1000x850")
root.title("Input")

minSup = 0.2
minCon = 0.5
g_RHS = frozenset(['Bread'])
dataset = ''
fileName = 'data\\transaction.csv'

support_var=tk.StringVar()
confidence_var=tk.StringVar()
rhs_var=tk.StringVar()
explore_var=tk.StringVar()

dataset_box =  tk.Text(root,height=30,width=40)

explore_label = tk.Label(root, text = 'Dataset', font=('bold'))
explore_entry = tk.Entry(root,textvariable = explore_var, font=('normal'))
button_explore = tk.Button(root, text = "Select",command = browseFiles)

support_label = tk.Label(root, text = 'Min Support', font=('bold'))
support_entry = tk.Entry(root,textvariable = support_var, font=('normal'))

confidence_label = tk.Label(root, text = 'Min Confidence', font = ('bold'))
confidence_entry=tk.Entry(root, textvariable = confidence_var, font = ('normal'))

rhs_label = tk.Label(root, text = 'Right Destination', font = ('bold'))
rhs_entry=tk.Entry(root, textvariable = rhs_var, font = ('normal'))

sub_btn=tk.Button(root,text = 'Submit', font=('normal'), command = submit)

px1= 470 
px2, px3= px1+150, px1+350
py1 = 370

dataset_box.place(x=80, y= 110)

explore_label.place(x=px1, y=py1)
explore_entry.place(x=px2, y=py1)
button_explore.place(x=px3, y=py1)

support_label.place(x=px1, y=py1+40)
support_entry.place(x=px2, y=py1+40)

confidence_label.place(x=px1, y=py1+80)
confidence_entry.place(x=px2, y=py1+80)

rhs_label.place(x=px1, y=py1+120)
rhs_entry.place(x=px2, y=py1+120)

# sub_btn.grid(row=4,column=1, pady=5, padx=10)
sub_btn.place(x=px2, y=py1+200, anchor=CENTER)


root.mainloop()
