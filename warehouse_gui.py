import tkinter as tk
from tkinter import Tk
from tkinter import filedialog as fd
from os import startfile
from warehouse import Warehouse
from algorithms.local_beam_search import BeamSearch
# class MainApplication(tk.Frame):

#creating a GUI
# TODO [] bind all algorithms to each option button
# TODO [] display stock and order (open file? print? open popup?)
# TODO [] add test cases for 1. no file selected 2. missing arguments for algorithm option 3. missing warehouse or order file
# TODO [] add some information about what each button does
# TODO [] find nice way to display output of each algorithm (messsage popup?)
# TODO [] rename variables and give them better descriptive names
# TODO [] fix initial frame size

#1. creating a window
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Warehouse")
        self.order_file = ""
        self.warehouse_file = ""
        self.bs = None
        self.firstlabel = tk.Label(root, text = "Here you can place a order:")
        self.firstlabel.pack()
        #how many frames do we need
        #first frame that should somehow show the stock
        self.firstframe = tk.Frame(root)        #TODO frame = Frame(root, width=100, height=100)
        self.firstframe.pack()
        #self.stock_but = tk.Button(self.firstframe, text="here you can have a look at our stock", command=self.view_stock)
        #self.stock_but.pack(side=tk.TOP)
        # second frame to select an order
        self.secframe = tk.Frame(root)

        self.secframe.pack(side=tk.TOP)
        # third frame to choose from search algorithms
        self.thirdframe = tk.Frame(root)
        self.thirdframe.pack(side=tk.LEFT)

        # fourth frame with a order now Button
        self.forframe = tk.Frame(root)
        self.forframe.pack(side=tk.BOTTOM)

        # fith frame to print in the psu used
        self.fifframe = tk.Frame(root)
        self.fifframe.pack(side=tk.BOTTOM)
        self.psuus = tk.Label(self.forframe, text="you used ... psus")
        self.psuus.pack(side=tk.BOTTOM)
        #load warehouse
        self.button = tk.Button(self.secframe, text='Load your warehouse here', command= self.upload_warehouse_file)
        self.button.pack()
        # load order
        self.buttonorder = tk.Button(self.secframe, text='Load your order here', command=self.upload_order_file)
        self.buttonorder.pack()
        # choose the algo button
        OPTIONS = [
            "Hill-Climbing",
            "First-Choice Hill-Climbing",
            "Parallel Hill-Climbing",
            "Simulated Annealing",
            "Local Beam Search"
        ]

        self.variable = tk.StringVar(self.secframe)
        self.variable.set(OPTIONS[0])  # default value

        self.algobut = tk.OptionMenu(self.secframe, self.variable, *OPTIONS, command = self.change_states)
        self.algobut.pack()
    #    self.variable.trace("w", self.change_states)
    #    if self.variable.get() == "Parallel Hill-Climbing":      # About window
    #        top.title("Parallel Hill-Climbing")
    #        toplabel = Label(top,text= "Select number of states")
    #        toplabel.pack()
    #        button = tk.Entry(top)
    #        button.grid()
    #        top.grid()
    #    if self.variable.get() == "Local Beam Search":
    #        top

        #if self.algobut == OPTIONS[2] or self.algobut == OPTIONS[4]:
        #    stat_num = tk.Entry(self.secframe, text="select number of states: ")
        #    stat_num.pack()
        #self.select_steps = tk.Entry(self.secframe, text = "select number of steps")
        #self.select_steps.pack()
        # local beam search brauchen wir config numb of states

        #sel_order = self.upload_warehouse_file() #thats why it is always opening a window before anything
        # final start button
        self.orderbut = tk.Button(self.forframe, text="Start Order", fg="red", command= self.start_processing)
        self.orderbut.pack()

    def change_states(self, variable):
        if variable == "Parallel Hill-Climbing" or variable == "Local Beam Search":
            print(variable)
            self.top = tk.Toplevel()
            self.top.title("Enter a number of states")
            v = tk.IntVar()
            self.number_button = tk.Entry(self.top, textvariable = v, text ="var")
            self.number_button.pack()
            self.go_button = tk.Button(self.top, text ="Enter", command = self.states)
            self.go_button.pack()
            self.exit_button = tk.Button(self.top, text = "Close", command = lambda: self.top.destroy())
            self.exit_button.pack()

# this function reads in the number of states for Parallel HC and Simulated Annealing
    def states(self):
        number = self.number_button.get()
        #print(number)
        try:
            state_numbers = int(number)
            return state_numbers
        except ValueError:
            print("Enter an Integer, please!")
            return False


    def start_processing(self):
        print("starting processing")
        if wh is None: #is not defined
            self.stoptop = tk.Toplevel()
            self.stoptop.title("Error!")
            self.errorbutton = tk.Button(self.stoptop, text = "Ooops, you forgot to load your warehouse, try again!", command = lambda: self.stoptop.destroy())
            self.errorbutton.pack()
        elif order is None:
            self.top = tk.Toplevel()
            self.top.title("Error!")
            self.errorbutton = tk.Button(self.top, text = "Ooops, you forgot to load your warehouse, try again!",command= lambda: self.top.destroy())
            self.errorbutton.pack()
        self.bs = BeamSearch(self.warehouse_file, self.order_file, 3)
        self.bs.beam_search()

    ##define here where to open the file,
    #def view_stock(self):
        startfile("stock.txt")
        #TODO open file?




    def upload_order_file(self):
        self.wh.order



    #creating buttons
    #read in your order button as a text file
    def upload_warehouse_file(self, event=None):
        warehouse_file = fd.askopenfile(title = "Select file")#TODO import filedialog not as fd, easier to read
        #TODO ,filetypes = (("jpeg files","*.txt"),("all files","*.*"))
        if warehouse_file:
            print('Selected:', warehouse_file.name)  #print(self.wh.stock)
            self.warehouse_file = warehouse_file.name
            wh = warehouse_file.read()
            print(wh)

    def upload_order_file(self, event=None):
        order_file = fd.askopenfile(title="Select order file")  # TODO import filedialog not as fd, easier to read
        # TODO ,filetypes = (("jpeg files","*.txt"),("all files","*.*"))
        #TODO do not create warehouse object, just read from the file
        if order_file:
            print('Selected:', order_file.name)
            self.order_file =  order_file.name
            order = order_file.read()


################################## #TODO add this to ask user before quitting
# from Tkinter import *
# import tkMessageBox
#
# def callback():
#     if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
#         root.destroy()
#
# root = Tk()
# root.protocol("WM_DELETE_WINDOW", callback)
#
# root.mainloop()
#######################################
root = Tk()
my_gui = GUI(root)
root.mainloop()
