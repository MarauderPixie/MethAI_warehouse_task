import os
import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from algorithms.local_beam_search import BeamSearch
from algorithms.first_choice_hill_climbing import FirstChoiceHillClimbing
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.hill_climbing import HillClimbing
from algorithms.random_restart_hill_climbing import RandomRestart

# TODO [x] bind all algorithms to each option button
# TODO [] add button display stock and order (open file? print? open popup?)
# TODO [x] add test cases for 1. no file selected 2. missing arguments for algorithm option 3. missing warehouse or order file
# TODO [] add some information about what each button does
# TODO [x] find nice way to display output of each algorithm (messsage popup?)
# TODO [x] rename variables and give them better descriptive names
# TODO [x] fix initial frame size
# TODO [] fix position of processing, reset and exit buttons
# TODO [] fix bug where states entry box appears a million times if you click on the algorithm again
# TODO [] add this to ask user before quitting maybe?

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Warehouse")
        # dimensions of the Tk window and screen information
        self.width= 350
        self.height = 250
        screen_width = root.winfo_screenwidth()
        screen_height= root.winfo_screenheight()
        # calculate x and y coordinates for the Tk window
        self.x = (screen_width / 2) - (self.width / 2)
        self.y = (screen_height / 2) - (self.height / 2)
        # set the dimensions of the window and where it is placed
        root.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))


        self.order_file = ""
        self.warehouse_file = ""
        self.algorithm = ""
        self.number_states = 0

        self.description = tk.Label(root, text = "Here you can place a order:")
        self.description.pack()


        # self.firstframe = tk.Frame(root)
        # self.firstframe.pack()
        #self.stock_but = tk.Button(self.firstframe, text="here you can have a look at our stock", command=self.view_stock)
        #self.stock_but.pack(side=tk.TOP)


        # create the main frame that will contain all the buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.TOP)

        # load warehouse
        self.button_warehouse = tk.Button(self.main_frame, text='Click here to load your warehouse.', command=self.upload_warehouse_file)
        self.button_warehouse.pack()

        # load order
        self.button_order = tk.Button(self.main_frame, text='Click here to load your order.', command=self.upload_order_file)
        self.button_order.pack()

        # all the available algorithms
        OPTIONS = [
            "Hill-Climbing",
            "First-Choice Hill-Climbing",
            "Random Restart Hill-Climbing",
            "Simulated Annealing",
            "Local Beam Search"
        ]

        self.variable = tk.StringVar(self.main_frame)
        self.variable.set("Select an algorithm.")  # default value

        self.algorithm_button = tk.OptionMenu(self.main_frame, self.variable, *OPTIONS, command=self.enter_states)
        self.algorithm_button.pack()

        # this will be used to read in a number of states entered by the user
        variable = tk.IntVar()
        self.states_entry = tk.Entry(self.main_frame, state='disabled', textvariable=variable, text="variable")
        self.states_entry.pack()

        # tinkering
        self.description = tk.Label(self.main_frame, text="Set the number of states / restarts.")
        self.go_button = tk.Button(self.main_frame, text="Enter", command=self.states)
        self.go_button.pack()
        self.description.pack()

        # final start button
        self.bottom_frame = tk.Frame(root)  # TODO used for reset button and order
        self.bottom_frame.pack(side=tk.LEFT)

        # reset all variables, including warehouse and order
        self.resetbutton = tk.Button(self.bottom_frame, text='Reset', command=lambda: self.refresh())
        self.resetbutton.pack(side=tk.LEFT)

        # start processing the order according to the selected algorithm
        self.processing_button = tk.Button(self.bottom_frame, text="Retrieve Order", fg="red", command= self.start_processing)
        self.processing_button.pack(side = tk.LEFT)


        self.last_frame = tk.Frame(root)  # TODO used for exit button
        self.last_frame.pack(side=tk.BOTTOM)
        # Exit the program
        self.exit_button = tk.Button(self.last_frame, text="Exit", command=lambda: self.master.destroy())
        self.exit_button.pack(side=tk.BOTTOM)
   
    def refresh(self):
        # self.main_frame.forget()
        self.go_button.forget()
        self.description.forget()
        self.variable.set("Select an Algorithm")
        self.number_states = ""
        self.warehouse_file = ""
        self.order_file = ""
        self.button_warehouse.config(text="Load your warehouse here")


    '''
        if user selects random restart of beam search algorithm, prompt them to enter number of states
    '''
    def enter_states(self, variable):
        self.algorithm = variable

        if self.algorithm == "Random Restart Hill-Climbing" or self.algorithm == "Local Beam Search":
            if self.algorithm == "Random Restart Hill-Climbing":
                self.go_button.pack_forget()
                self.description.pack_forget()
                self.description = tk.Label(self.main_frame, text="Set the number of restarts.")
                self.go_button.pack()
                self.description.pack()
            if self.algorithm == "Local Beam Search":
                self.go_button.pack_forget()
                self.description.pack_forget()
                self.description = tk.Label(self.main_frame, text="Set the number of states.")
                self.go_button.pack()
                self.description.pack()
            self.states_entry.config(state='normal')

        else:
            self.go_button.pack_forget()
            self.description.pack_forget()
            self.states_entry.config(state='disabled')
            # print(variable)
            # self.top = tk.Toplevel()
            # self.top.title("Enter a number of states")
            # v = tk.IntVar()
            # self.number_button = tk.Entry(self.top, textvariable = v, text ="var")
            # self.number_button.pack()
            # self.go_button = tk.Button(self.top, text ="Enter", command = self.states)
            # self.go_button.pack()
            # self.exit_button = tk.Button(self.top, text = "Close", command = lambda: self.top.destroy())
            # self.exit_button.pack()


    '''
        this function reads in the number of states for Parallel HC and Simulated Annealing
    '''
    def states(self):
        number = self.states_entry.get()
        self.processing_button.focus()
        try:
            self.number_states = int(number)
            return self.number_states
        except ValueError:
            self.button_showinfo = tk.Button(self, text="Show Info", command=self.popup_message())
            self.button_showinfo.pack()
            return False

    '''
        Popup message if user did not enter an integer
    '''
    def popup_message(self):
        popup = tk.Tk()
        popup.wm_title("!")
        popup.geometry('%dx%d+%d+%d' % (150, 150, self.x, self.y))
        label = ttk.Label(popup, text='Enter an Integer, please!')
        label.pack(side="top", fill="x", pady=10)
        okay_button = ttk.Button(popup, text="Okay", command=popup.destroy)
        okay_button.pack()

    def format_output(self, dict):
        output_string = "Retrieved {} of {} items in your order using {} PSUs\n\n".format(dict["covered_items"],
                                                                                          dict["goal"],
                                                                                          dict["number_units"])
        for unit in dict["units"]:
            output_string = output_string + "Unit no. {} containing following items: \n {}\n\n".format(unit[0], ','.join(unit[1]))

        return output_string

    '''
        this function creates an object for each algorithm and performs the search
    '''
    def start_processing(self):
        # return an error message, if no warehouse is selected
        if not self.warehouse_file:
            self.stoptop = tk.Toplevel()
            self.stoptop.title("Error!")
            self.errorbutton = tk.Button(self.stoptop, text = "Ooops, you forgot to load your warehouse, try again!", command = lambda: self.stoptop.destroy())
            self.errorbutton.pack()
        # return an error message, ig no orderfile is selected
        elif not self.order_file:
            self.top = tk.Toplevel()
            self.top.title("Error!")
            self.errorbutton = tk.Button(self.top, text = "Ooops, you forgot to load your order, try again!",command= lambda: self.top.destroy())
            self.errorbutton.pack()

        # perform Local Beam Search
        if self.algorithm == "Local Beam Search":
            # check if a correct number of states is entered
            if self.number_states < 1:
                self.stoptop = tk.Toplevel()
                self.stoptop.title("Error!")
                self.errorbutton = tk.Button(self.stoptop, text = "Ooops, you forgot to enter a number of states, try again!", command = lambda: self.stoptop.destroy())
                self.errorbutton.pack()
            else:
                self.bs = BeamSearch(self.warehouse_file, self.order_file, self.number_states)
                output = self.bs.beam_search()
                self.endtop = tk.Toplevel()
                self.endtop.title("End of Process")
                # self.psuused = tk.Label(self.endtop, text = "You used %s PSUs" %output["number_units"] ) #... add %s total number of psu used
                # self.psuused.pack()
                self.output_message = tk.Label(self.endtop, text = self.format_output(output))# ... add %s list of the identifier number
                self.output_message.pack()
                self.end_button = tk.Button(self.endtop, text ="End", command = lambda: self.endtop.destroy())
                self.end_button.pack()


        # perform First Choice Hill Climbing
        if self.algorithm == "First-Choice Hill-Climbing":
            self.fc = FirstChoiceHillClimbing(self.warehouse_file, self.order_file)
            output = self.fc.first_choice_hill_climbing()

            self.endtop = tk.Toplevel()
            self.endtop.title("End of Process")
            self.output_message = tk.Label(self.endtop, text = self.format_output(output))# ... add %s list of the identifier number
            self.output_message.pack()

            self.end_button = tk.Button(self.endtop, text ="End", command = lambda: self.endtop.destroy())
            self.end_button.pack()


        # perform Random Restart Hill Climbing
        if self.algorithm == "Random Restart Hill-Climbing":
            # check if a correct number of states is entered
            if self.number_states < 1:
                self.stoptop = tk.Toplevel()
                self.stoptop.title("Error!")
                self.errorbutton = tk.Button(self.stoptop, text = "Ooops, you forgot to select a number of states, try again!", command = lambda: self.stoptop.destroy())
                self.errorbutton.pack()
            else:
                self.rr = RandomRestart(self.warehouse_file, self.order_file, self.number_states)
                output = self.rr.random_restart()

                self.endtop = tk.Toplevel()
                self.endtop.title("End of Process")
                self.output_message = tk.Label(self.endtop, text = self.format_output(output))# ... add %s list of the identifier number
                self.output_message.pack()

                self.end_button = tk.Button(self.endtop, text ="End", command = lambda: self.endtop.destroy())
                self.end_button.pack()

        # perform Simulated Annealing
        if self.algorithm == "Simulated Annealing":
            self.sa = SimulatedAnnealing(self.warehouse_file, self.order_file)
            output = self.sa.simulated_annealing()

            self.endtop = tk.Toplevel()
            self.endtop.title("End of Process")
            self.output_message = tk.Label(self.endtop, text = self.format_output(output))# ... add %s list of the identifier number
            self.output_message.pack()

            self.end_button = tk.Button(self.endtop, text ="End", command = lambda: self.endtop.destroy())
            self.end_button.pack()

        # perform Hill Climbing
        if self.algorithm == "Hill-Climbing":
            self.hc = HillClimbing(self.warehouse_file, self.order_file)
            output = self.hc.hill_climbing()

            self.endtop = tk.Toplevel()
            self.endtop.title("End of Process")
            self.output_message = tk.Label(self.endtop, text = self.format_output(output))# ... add %s list of the identifier number
            self.output_message.pack()

            self.end_button = tk.Button(self.endtop, text ="End", command = lambda: self.endtop.destroy())
            self.end_button.pack()


    # upload a warehouse file and assign the path to the warehouse_file variable
    def upload_warehouse_file(self, event=None):
        warehouse_file = tk.filedialog.askopenfile(title = "Select file", filetypes = [('Text files', '*.txt')])#TODO import filedialog not as fd, easier to read
        if warehouse_file:
            self.warehouse_file = warehouse_file.name
            filename = os.path.split(warehouse_file.name)[1]
            self.button_warehouse.config(text="Warehouse file: {}".format(filename))

    # upload an order file and assign the path to the order_file variable
    def upload_order_file(self, event=None):
        order_file = tk.filedialog.askopenfile(title="Select order file", filetypes = [('Text files', '*.txt')])  # TODO import filedialog not as fd, easier to read
        if order_file:
            self.order_file =  order_file.name
            filename = os.path.split(order_file.name)[1]
            self.button_order.config(text="Order file: {}".format(filename))


##################################
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