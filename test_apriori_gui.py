from email.message import Message
from fileinput import filename
from os import stat, system
import re
import tkinter as tk
from tkinter import CENTER, RAISED, StringVar, filedialog
from turtle import st

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
    if support_var.get()!='' : minSup = float(support_var.get())
    if confidence_var.get()!='' : minCon = float(confidence_var.get())
    if rhs_var.get()!='' : g_RHS = frozenset([rhs_var.get()])
    dataset = fileName
    root.destroy()

root=tk.Tk()
root.geometry("1200x800")
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



explore_label = tk.Label(root, text = 'Dataset', font=('bold'))
explore_entry = tk.Entry(root,textvariable = explore_var, font=('normal'))
button_explore = tk.Button(root, text = "Select",command = browseFiles)

support_label = tk.Label(root, text = 'Min Support', font=('bold'))
support_entry = tk.Entry(root,textvariable = support_var, font=('normal'))

confidence_label = tk.Label(root, text = 'Min Confidence', font = ('bold'))
confidence_entry=tk.Entry(root, textvariable = confidence_var, font = ('normal'))

rhs_label = tk.Label(root, text = 'Right Destination', font = ('bold'))
rhs_entry=tk.Entry(root, textvariable = rhs_var, font = ('normal'))

sub_btn=tk.Button(root,text = 'Submit', font=('normal'), command = submit, bg="green")
  
px1, py1 = 450, 300

msg = 'The APRIORI Algorithm'
title_label = tk.Label(root, text=msg, font=("Arial",30, "bold"))
title_label.place(x=400, y=20)

explore_label.place(x=px1, y=py1)
explore_entry.place(x=px1+150, y=py1)
button_explore.place(x=px1+350, y=py1)


support_label.place(x=px1, y=py1+40)
support_entry.place(x=px1+150, y=py1+40)


confidence_label.place(x=px1, y=py1+80)
confidence_entry.place(x=px1+150, y=py1+80)

rhs_label.place(x=px1, y=py1+120)
rhs_entry.place(x=px1+150, y=py1+120)

# sub_btn.grid(row=4,column=1, pady=5, padx=10)
sub_btn.place(x=px1+150, y=py1+200, anchor=CENTER)


root.mainloop()


res = tk.Tk()
res.title("Results")
res.geometry("1200x800")

msg = 'The APRIORI Algorithm'
title_label = tk.Label(res, text=msg, font=("Arial",30, "bold"))
title_label.place(x=400, y=20)

msg = ''

msg += """Parameters: \n - filePath: {} \n - mininum support: {} \n - mininum confidence: {} \n - rhs: {}\n""".format(dataset,minSup,minCon, g_RHS) + '\n'
par_box = tk.Text(res, height=6, width=65)
par_box.insert('end', msg)

msg=''
objApriori = Apriori(minSup, minCon)
itemCountDict, freqSet = objApriori.fit(dataset)
for key, value in freqSet.items():
    msg += 'frequent {}-term set:'.format(key) + '\n'
    msg += '-'*20 +'\n'

    for itemset in value:
        msg += str(list(itemset)) + '\n'

    msg += '\n'



rules = objApriori.getSpecRules(g_RHS)
msg += '-'*20 + '\n'
freq_box = tk.Text(res, height=40, width=65)
freq_box.insert('end', msg)
msg = ''
msg += 'rules refer to {}'.format(list(g_RHS)) + '\n'
for key, value in rules.items():
    msg += '{} -> {}: {}'.format(list(key), list(g_RHS), value) + '\n'

rule_box = tk.Text(res, height=32, width=65)
rule_box.insert('end', msg)

py1=100
par_box.place(x=50, y=py1)
freq_box.place(x=620, y=py1)
rule_box.place(x=50, y=py1+130)
par_box.config(state='disabled')
rule_box.config(state='disabled')
freq_box.config(state='disabled')

res.mainloop()
