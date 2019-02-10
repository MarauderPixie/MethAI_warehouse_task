import tkinter as tk
from tkinter import filedialog as fd
# class MainApplication(tk.Frame):

#creating a GUI

#1. creating a window
root = tk.Tk()
firstlabel = tk.Label(root, text = "Here you can place a order:")
firstlabel.pack()
#how many frames do we need
#first frame that should somehow show the stock
firstframe = tk.Frame(root)
firstframe.pack()


##define here where to open the file,
def openInstruktion():
    from os import startfile
    startfile("stock.txt")

stock_but = tk.Button(firstframe, text = "here you can have a look at our stock", command = openInstruktion)
stock_but.pack(side = tk.TOP)

#second frame to select an order
secframe = tk.Frame(root)
secframe.pack(side = tk.TOP)

#third frame to choose from search algorithms
thirdframe = tk.Frame(root)
thirdframe.pack(side = tk.LEFT)

#fourth frame with a order now Button
forframe = tk.Frame(root)
forframe.pack(side = tk.BOTTOM)

#fith frame to print in the psu used
fifframe = tk.Frame(root)
fifframe.pack(side = tk.BOTTOM)
psuus = tk.Label(forframe, text = "you used ... psus")
psuus.pack(side = tk.BOTTOM)

#creating buttons
#read in your order button as a text file
def UploadAction(event=None):
    selected_order = fd.askopenfile()
    print('Selected:', selected_order)
    order = selected_order.read()
    print(order)
    return order


button = tk.Button(secframe, text='Load your orderfile here', command=UploadAction)
button.pack()


#choose the algo button
OPTIONS = [
"Hill-Climbing",
"First-Choice Hill-Climbing",
"Parallel Hill-Climbing",
"Simulated Annealing",
"Local Beam Search"
]

variable = tk.StringVar(secframe)
variable.set(OPTIONS[0]) # default value

algobut = tk.OptionMenu(secframe, variable, *OPTIONS)
algobut.pack()

if algobut == OPTIONS[2] or algobut == OPTIONS[4]:
    stat_num = tk.Entry(secframe, text = "select number of states: ")
    stat_num.pack()
#hier fehlt die verknüfung und für parallel hill,
#local beam search brauchen wir config numb of states
sel_order = UploadAction()
#final start button
orderbut = tk.Button(forframe, text = "Start Order", fg = "red", command = lambda: sel_order.start_processing())
orderbut.pack()
root.mainloop()
