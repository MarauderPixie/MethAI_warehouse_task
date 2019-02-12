import random
import numpy as np
import math
##################################################
######important importing#########################
#import qt
##################################################
#GOAL: we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma

warehouse = []
for line in open("../data/problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[0] #the first line, what is in stock
warehouse = warehouse[2:] #now we have a list of the psus
#(warehouse[0])
#print(stock)

#2. open the order11, store in list
for item in open("../data/order11.txt"):
    order11 = item.split(" ")

#3. open the order12
for item in open("../data/order12.txt"):
    order12 = item.split(" ")
    #order_new = order12[2:]

# Dictionary items to numbers
dictionary_stock = {}
for i in range(len(stock)):
    dictionary_stock[stock[i]] = i+1


# convert the items in the PSUs to Numbers.
def replace_matched_PSU(word_list, dictionary):
    new_list = [[dictionary.get(item, item) for item in lst] for lst in word_list]
    return new_list
NoWarehouse = replace_matched_PSU(warehouse, dictionary_stock)

#print(NoWarehouse)

# convert the items in the order to Numbers
def convert_item_in_order(word_list, dictionary):
    new_list = [dictionary.get(item) for item in word_list]
    return new_list
NoOrder11 = convert_item_in_order(order11,dictionary_stock)
NoOrder12 = convert_item_in_order(order12,dictionary_stock)

#1. read in the text file with the warehouse information



# define function to get only those PSUs containing at least one of the ordered items
def get_relevant_psus(order, PSU):
    psu_list = []
    for rob in PSU:
        bob = [item for item in rob if item in order]
        psu_list.append(bob)
    return psu_list #

## call function on order
relevant = get_relevant_psus(NoOrder12, NoWarehouse)

## get indices of relevant PSUs and remove "empty" PSUs from list
psu_index = [i for i, j in enumerate(relevant) if j]
relevant = list(filter(None, relevant))     #list of relevant items in psus[[254],[168,251]...]

#dictionary relevant PSU
dictionary_rel_PSU = {}
i: int
for i in range(len(psu_index)):
    dictionary_rel_PSU[i] = psu_index[i]

print(dictionary_rel_PSU)
def PSU_used(state):
    cov = []
    for i in range(len(state)):
        if state[i] == 1:
            cov.append(i)
    return cov

def get_item_of_used_PSU(idx): # gets list of index of PSU and what it caries
    new_list = []
    for i in idx:
        new_list.append((i,NoWarehouse[i]))
    return new_list

# get idices of PSUs with more than one item
def get_cool_PSU(rel):
    new = []
    for items in rel:
        if len(items) > 1:
            new.append(rel.index(items))
    return new

cool_psu = get_cool_PSU(relevant)

#TODO store indices of psus for access at the end
#TODO select neighbors
class BeamSearch:
    def __init__(self, warehouse, order):
        self.warehouse = warehouse
        self.order = order
        self.beam_width = 3 #TODO do not hardcode this

    #keep only the PSUs that contain at least one of the items in the order, with only the relevant item in them
    #equivalent to get_relevant_psus()
    def prune(self):
        relevant_units = []
        for unit in self.warehouse:
            relevant_units.append([item for item in unit if item in self.order])
            relevant_units = list(filter(None, relevant_units))

            ## get indices of relevant PSUs and remove "empty" PSUs from list TODO where is this used?
            # psu_index = [i for i, j in enumerate(relevant) if j]
        return relevant_units


    def get_covered_items(self, state, relevant):
        cov = []
        for i in range(len(state)):
            if state[i] == 1:
                cov.append(relevant[i])
        return cov


    def get_fitness(self, state, relevant):
        cov = self.get_covered_items(state, relevant)
        covered = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
        y = sum(state)  # number of PSUs used
        fit = len(covered) - (0.9 * y)  # fit is the number of covered items minus the number of PSUs
        return fit


    #neighborhood is obtained by looking at an n-window distance from the PSU units already retrieved in that state
    def get_neighbors(self, states, relevant):
        neighborhood = []
        window = 3

        for state in states:
            #indices of the units that contain the relevant items
            indices = [index for index, value in enumerate(state) if value == 1]

            for i in range(self.beam_width):
                succesor = state[:]
                #for each relevant unit, look at the units in an n-window around it and randomly change some of them
                for index in indices:
                    if index - window > 0 and index + window < len(relevant)-1:
                        #randomly pick one unit in the window and change it to 0 if it's 1 and to 1 otherwise
                        k = random.choice(range(index-window, index+window))
                        succesor[k] = 1 if succesor[k] == 0 else 0
                neighborhood.append(succesor)

        return neighborhood


    def beam_search(self, relevant, order):
       #k_current - select k random states
       #start_state = random.sample(self.prune(), self.beam_width)
       L = len(relevant)
       goal = len(order)
       print(goal)
       #start with 3 random states
       init_states = [np.random.choice([0,1], size=(L,), p=[1 - len(order) / L, len(order) / L]) for i in range(self.beam_width)]
       print("len", len(self.get_neighbors(init_states, relevant)))
       # self.get_neighbors(init_states, relevant)
       for state in init_states:
            fitness = self.get_fitness(state, relevant)
            cov = self.get_covered_items(state, relevant)
            cov = set([u for sublist in cov for u in sublist])
            print("cov2", cov, "len:", len(cov))
    # state_0 = np.random.choice([0, 1], size=(L,),
    #                            p=[1 - len(O) / L, len(O) / L])  # rendom array 0=PSU not used 1=PSUused

        #print(start_state)
       #neighbors - select all neighbours of all current states
       #k_best neighbors - best k states from neighbors
       #if no neighbor improves current value
        #return k_current
       #k_current = k_best neighbors
        #until termination condition is met



    # ## get indices of relevant PSUs and remove "empty" PSUs from list
    # psu_index = [i for i, j in enumerate(relevant) if j]
    # relevant = list(filter(None, relevant))
    # print(len(relevant))
    # # get idices of PSUs with more than one item
    # def get_cool_PSU(rel):
    #     new = []
    #     for items in rel:
    #         if len(items) > 1:
    #             new.append(rel.index(items))
    #     return new
    #
    # cool_psu = get_cool_PSU(relevant)
    # print(len(cool_psu))
    #
    # beam_width = 2 #configurable by user
    # print("order:", order12)
    # print(NoOrder12)
    # # for i in cool_psu:
    # #     print(relevant[i])
    # print(relevant)

bs = BeamSearch(NoWarehouse, NoOrder12)
print("all psus with the items inside:", bs.warehouse)
print("order:", bs.order)
print("prune:", len(bs.prune()), bs.prune())

bs.beam_search(relevant, bs.order)
