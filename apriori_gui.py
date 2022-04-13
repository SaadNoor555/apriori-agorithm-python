from cgitb import text
from email.message import Message
from faulthandler import disable
from fileinput import filename
from multiprocessing.connection import wait
from os import stat
import re
from time import sleep
import tkinter as tk
from tkinter import CENTER, END, RAISED, StringVar, filedialog, ttk
from tkinter.ttk import Style
from turtle import bgcolor, bgpic, color, st
from webbrowser import get
from django import conf

from numpy import pad

from apriori import Apriori

def browseFiles():
    global fileName
    fileName = filedialog.askopenfilename(  initialdir = "/", 
                                            title = "Select a File", 
                                            filetypes = (("Text files", "*.txt*"),("all files", "*.*")))
    explore_var.set(fileName)

def reset():
    conf_box.config(state='normal')
    freq_box.config(state='normal')
    dataset_box.delete(1.0, 'end')
    conf_box.delete(1.0, 'end')
    freq_box.delete(1.0, 'end')
    explore_entry.delete(first=1)
    confidence_entry.delete(first=1)
    support_entry.delete(first=1)
    select_btn.config(state='disabled')
    save_btn.config(state='disabled')
    rhs_choose.config(state='disabled')
    conf_box.config(state='disabled')
    freq_box.config(state='disabled')

def save():
    print()

def select():
    conf_box.config(state='normal')
    if rhs_var.get()!='': g_RHS = frozenset([rhs_var.get()])
    conf_box.delete(1.0, 'end')
    conf_box.place(x=550, y=py1+30)
    # print(objApriori.minConf)
    # print(g_RHS)
    rules = objApriori.getSpecRules(g_RHS)
    # print(rules)
    msg = ''
    msg += 'rules refer to {}'.format(list(g_RHS)) + '\n'
    for key, value in rules.items():
        msg += '{} -> {}: {}'.format(list(key), list(g_RHS), value) + '\n'
    conf_box.insert('end', msg)
    conf_box.config(state='disabled')
    save_btn.config(state='active')

    
def showFreqItems():
    freq_box.config(state='normal')
    msg = ''
    global objApriori
    objApriori = Apriori(minSup, minCon)
    itemCountDict, freqSet = objApriori.fit(dataset)
    for key, value in freqSet.items():
        msg += 'frequent {}-term set:'.format(key) + '\n'
        msg += '-'*20 +'\n'

        for itemset in value:
            msg += str(list(itemset)) + '\n'

        msg += '\n'
    freq_box.delete(1.0, 'end')
    freq_box.insert('end', msg)
    freq_Label.place(x=550, y=80)
    freq_box.place(x=550, y=110)
    freq_box.config(state='disabled')

def submit():
    global minSup, minCon, g_RHS, dataset, fileName
    input = dataset_box.get("1.0", END)
    if len(input) > 10 : 
        fileName = 'input_data.csv'
        newFile = open('input_data.csv','w+')
        print(input[:len(input)-1], file=newFile, end="")
        newFile.close()
    if support_var.get()!='' : minSup = float(support_var.get())
    if confidence_var.get()!='' : minCon = float(confidence_var.get())
    dataset = fileName
    # print(dataset)
    showFreqItems()
    data_file = open(dataset, 'r')
    item_set = set()
    for line in data_file:
        # print(line)
        tokens = line.split(',')
        # print(tokens)
        for token in tokens:
            if token.find('\n')!=-1: token = token[:-1]
            if token not in item_set:
                item_set.add(token)
    rhs_label.place(x=550, y=py1-5)
    select_btn.place(x=830, y=py1-8)
    rhs_choose['values'] = (list(sorted(item_set)))
    rhs_choose.place(x=620, y=py1-5)
    rhs_choose['state'] = 'readonly'
    rhs_choose.current(0)
    conf_box.config(state='normal')
    conf_box.delete(1.0, 'end')
    conf_box.config(state='disabled')
    select_btn.config(state='active')

objApriori = Apriori(0.2, 0.5) 

bg_primary_color = 'black'
bg_secondary_color = '#494949'
fg_primary_color = 'white'
fg_secondary_color = 'lightgray'

root=tk.Tk()
root.geometry("1000x850")
root.title("Input")
root.maxsize(width=1000, height=850)
root.minsize(width=1000, height=850)
root.config(bg=bg_primary_color)

title_label = tk.Label(root, text='The Apriori Algorithm', font=('Arial',35,'bold'), foreground='lightgrey', background=bg_primary_color)
title_label.place(x=275, y=0)
title_label = tk.Label(root, text='I\nN\nP\nU\nT', font=('Arial',30,'bold'), foreground='#4D4D4D', background=bg_primary_color)
title_label.place(x=0, y=300)
title_label = tk.Label(root, text='O\nU\nT\nP\nU\nT', font=('Arial',30,'bold'), foreground="#4D4D4D", background=bg_primary_color)
title_label.place(x=962, y=300)

minSup = 0.2
minCon = 0.5
g_RHS = frozenset(['Bread'])
dataset = ''
fileName = 'data\\transaction.csv'


px1= 90
px2, px3= px1+140, px1+327
py1 = 595

dataset_label = tk.Label(root, text='Type your dataset:', font=('bold'), fg=fg_primary_color, bg=bg_primary_color)
dataset_box =  tk.Text(root, font=('normal',10), height=28,width=52, borderwidth=2, fg=fg_primary_color, background=bg_secondary_color)
dataset_label.place(x=px1, y=80)
dataset_box.place(x=px1, y= 110)

explore_var=tk.StringVar()
explore_label = tk.Label(root, text = 'Dataset', font=('bold'), fg=fg_primary_color, background=bg_primary_color)
explore_entry = tk.Entry(root,textvariable = explore_var, font=('normal'), width=25, border=1.5, fg=fg_primary_color, background=bg_secondary_color)
button_explore = tk.Button(root, text = "Browse",command = browseFiles)
explore_label.place(x=px1, y=py1)
explore_entry.place(x=px2, y=py1)
button_explore.place(x=px3-2, y=py1)

support_var=tk.StringVar()
support_label = tk.Label(root, text = 'Min Support', font=('bold'), fg=fg_primary_color, background=bg_primary_color)
support_entry = tk.Entry(root,textvariable = support_var, font=('normal'), width=25, border=1.5, fg=fg_primary_color, background=bg_secondary_color)
support_label.place(x=px1, y=py1+40)
support_entry.place(x=px2, y=py1+40)

confidence_var=tk.StringVar()
confidence_label = tk.Label(root, text = 'Min Confidence', font = ('bold'), fg=fg_primary_color, background=bg_primary_color)
confidence_entry = tk.Entry(root, textvariable = confidence_var, font = ('normal'), width=25, border=1.5, fg=fg_primary_color, background=bg_secondary_color)
confidence_label.place(x=px1, y=py1+80)
confidence_entry.place(x=px2, y=py1+80)

sub_btn = tk.Button(root,text = 'Submit', font=('normal'), command = submit, height=1, width=6,border=1)
reset_btn = tk.Button(root,text = 'Reset', font=('normal'), command = reset, height=1, width=6, border=1)
save_btn = tk.Button(root,text = 'Save', font=('normal'), command = save, height=1, width=6, border=1)
save_btn.config(state='disabled')
sub_btn.place(x=px2, y=py1+130)
reset_btn.place(x=px2-100, y=py1+130)
save_btn.place(x=px2+100, y=py1+130)

canvas=tk.Canvas(root, width=0.5, height=700, background=fg_primary_color)
canvas.place(x=500, y=100)

freq_Label = tk.Label(root, text='Frequent Items:', font=('bold'), fg=fg_primary_color, background=bg_primary_color)
freq_box = tk.Text(root, height=28, font=('normal',10), width=52, border=2, fg=fg_primary_color, background=bg_secondary_color)
select_btn = tk.Button(root,text = 'Select', command = select, border=1)
rhs_var=tk.StringVar()
rhs_choose = ttk.Combobox(root, width=30, textvariable=rhs_var)
rhs_label = tk.Label(root, text='Product: ', font=('bold'), fg=fg_primary_color, background=bg_primary_color)
conf_box = tk.Text(root, height=10, font=('normal',10), width=52, border=2, fg=fg_primary_color, background=bg_secondary_color)

root.mainloop()
