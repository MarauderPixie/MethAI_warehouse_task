"""Progamming Task Methods of AI"""
##################################################
######important importing#########################
import sys
from tkinter import *
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
print(len(stock)) #286

#2. open the order11, store in list
for item in open("order11.txt"):
    order11 = item.split(" ")

#3. open the order12
for item in open("order12.txt"):
    order12 = item.split(" ")

#print(order11)
#print(order12)

#creating a GPU

#1. creating a window
root = Tk()
firstlabel = Label(root, text = "Here you can place a order:")
firstlabel.pack()
#how many frames do we need
#first frame that should somehow show the stock
firstframe = Frame(root)
firstframe.pack()
stock_but = Button(firstframe, text = "here you can have a look at our stock", command = open("stock.txt"))
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
#read in your order button
#selectbut = Button(secframe, text = "this should be a button to select your order somehow", fg = "green")
#if we need to read in an order (as a text file)
order = Entry(secframe, text = "read in your order file here: ") # ,command =
order.pack()

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
orderbut = Button(forframe, text = "Start Order", fg = "red")
orderbut.pack()
root.mainloop()

##look for a GPU

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
