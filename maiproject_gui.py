"""Progamming Task Methods of AI"""
##################################################
######important importing#########################
import sys
from tkinter import *
from tkinter import filedialog
import numpy as np
##################################################
#GOAL: we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma

#atom.project.setPath(C:\Users\schmuri\Documents\Master\Methods AI\Programming_Task)
#1. read in the text file with the warehouse information
warehouse = []
for line in open("problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[0] #the first line, what is in stock
warehouse = warehouse[1:] #now we have a list of the psus
#print(warehouse)
#print(stock)
#print(len(stock)) #286

#2. open the order11, store in list
for item in open("order11.txt"):
    order11 = item.split(" ")

#3. open the order12
for item in open("order12.txt"):
    order12 = item.split(" ")

# Dictionary items to numbers
dictionary_stock = {}
i: int
for i in range(len(stock)):
    dictionary_stock[stock[i]] = i+1

# convert the items in the PSUs to Numbers.
def replace_matched_PSU(word_list, dictionary):
    new_list = [[dictionary.get(item, item) for item in lst] for lst in word_list]
    return new_list
NoWarehouse = replace_matched_PSU(warehouse, dictionary_stock)


#print(order11)
#print(order12)

#creating a GUI

#1. creating a window
root = Tk()
firstlabel = Label(root, text = "Here you can place a order:")
firstlabel.pack()
#how many frames do we need
#first frame that should somehow show the stock
firstframe = Frame(root)
firstframe.pack()


##define here where to open the file,
def openInstruktion():
    from os import startfile
    startfile("stock.txt")

stock_but = Button(firstframe, text = "here you can have a look at our stock", command = openInstruktion)
stock_but.pack(side = TOP)

#second frame to select an order
secframe = Frame(root)
secframe.pack(side = TOP)

#third frame to choose from search algorithms
thirdframe = Frame(root)
thirdframe.pack(side = LEFT)

#fourth frame with a order now Button
forframe = Frame(root)
forframe.pack(side = BOTTOM)

#fith frame to print in the psu used
fifframe = Frame(root)
fifframe.pack(side = BOTTOM)
psuus = Label(forframe, text = "you used ... psus")
psuus.pack(side = BOTTOM)

#creating buttons
#read in your order button as a text file
def UploadAction(event=None):
    selected_order = filedialog.askopenfile()
    print('Selected:', selected_order)
    order = selected_order.read()
    print(order)
    return order


button = Button(secframe, text='Load your orderfile here', command=UploadAction)
button.pack()


#choose the algo button
OPTIONS = [
"Hill-Climbing",
"First-Choice Hill-Climbing",
"Parallel Hill-Climbing",
"Simulated Annealing",
"Local Beam Search"
]

variable = StringVar(secframe)
variable.set(OPTIONS[0]) # default value

algobut = OptionMenu(secframe, variable, *OPTIONS)
algobut.pack()

if algobut == OPTIONS[2] or algobut == OPTIONS[4]:
    stat_num = Entry(secframe, text = "select number of states: ")
    stat_num.pack()
#hier fehlt die verknüfung und für parallel hill,
#local beam search brauchen wir config numb of states

#final start button
orderbut = Button(forframe, text = "Start Order", fg = "red", command = lambda: selected_order.start_processing())
orderbut.pack()
root.mainloop()

############################reshape the input order############################
def start_processing(order, convert_item_in_order):
    for item in order:
        order = item.split(" ")
    convert_item_in_order(order,dictionary_stock)
    print(num_order)
    return num_order


# 1. store order in list
#for item in selected_order:
#    selected_order = item.split(" ")

# convert the items in the order to Numbers
def convert_item_in_order(word_list, dictionary):
    num_order = [dictionary.get(item) for item in word_list]
    return num_order
order = convert_item_in_order(rder,dictionary_stock)
print(order)
print(num_order)
###################################################################

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Order Now\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")
#
#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")
#
#     def say_hi(self):
#         print("You just ordered ")
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()
#
# # print how many PSU were used
# # print identifier of the PSU and items stored in the PSU
