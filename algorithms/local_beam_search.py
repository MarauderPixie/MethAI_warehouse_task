import random
import numpy as np
import copy
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
        self.relevant_units = self.prune()

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
        fit = round(len(covered) - (0.9 * y), 3) # fit is the number of covered items minus the number of PSUs
        return (len(covered),fit)


    #neighborhood is obtained by randomly picking units from within an n-window from the PSU units already retrieved in that state
    def get_neighbors(self, states, relevant):
        neighborhood = []
        window = 3
        for state in states:
            #indices of the units that contain the relevant items
            indices = [index for index, value in enumerate(state) if value == 1]
            for i in range(self.beam_width):
                succesor = copy.deepcopy(state)
                #for each relevant unit, look at the units in an n-window around it and randomly change some of them
                for index in indices:
                    if index - window > 0 and index + window < len(relevant)-1:
                        #randomly pick one unit in the window and change it to 0 if it's 1 and to 1 otherwise
                        k = random.choice(range(index-window, index+window))
                        succesor[k] = 1 if succesor[k] == 0 else 0
                neighborhood.append(succesor)

        return neighborhood


    #get best fit
    def get_smallest_values(self, arr, n):
        # Sort the given array arr in reverse
        # order.
        #arr.sort(reverse=True)
        best_fit = []
        arr.sort(key=lambda tup: tup[1][1])
        # Print the first kth largest elements
        if len(arr) < n:
            return  [n[0] for n in arr]
        else:
            for i in range(n):
                best_fit.append(arr[i][0])
            return best_fit


    def find_best_neighbors(self, states):
        updated_states = []
        neighbors = self.get_neighbors(states, relevant)
        for neighbor in neighbors:
            fitness_neighbor = self.get_fitness(neighbor, relevant)
            if fitness_neighbor[1] < any([self.get_fitness(state, relevant)[1] for state in states]):
                updated_states.append((neighbor, fitness_neighbor))
        # if no neighbor improves the values, return the initial states
        if not updated_states:
            print("no neigbor improved value")
            return states
        #print(updated_states)
        best_fit = self.get_smallest_values(updated_states, self.beam_width)
        print("bestfit", [self.get_fitness(best_state, relevant) for best_state in best_fit])
        print(12 in [self.get_fitness(best_state, relevant)[0] for best_state in best_fit])
        return best_fit

    def explore(self, state, step=None):
        if step is None:
            step = 1
        goal = len(self.order)
        best_neighbors = self.find_best_neighbors(state)
        if goal in [self.get_fitness(best_state, relevant)[0] for best_state in best_neighbors] or step == 10:
            goal_states = []
            for b in best_neighbors:
                if self.get_fitness(b, relevant)[0] == goal:
                    goal_states.append(self.get_fitness(b, relevant)[1])
            print("fouund best", best_neighbors[goal_states.index(min(goal_states))])
        else:
            step += 1
            self.explore(best_neighbors, step) #TODO this is the wrooongngnngng function

    def beam_search(self):
        L = len(relevant)
        goal = len(self.order)
        init_states = [np.random.choice([0, 1], size=(L,), p=[1 - goal / L, goal / L]) for i in range(self.beam_width)]
        print(self.explore(init_states))
# def explore(self, states, step=None):
    #     updated_states = []
    #     if step == None:
    #         step = 1
    #     print("step", step)
    #     neighbors = self.get_neighbors(states, relevant)
    #     for neighbor in neighbors:
    #         fitness_neighbor = self.get_fitness(neighbor, relevant)
    #         if fitness_neighbor[1] < any([self.get_fitness(state, relevant)[1] for state in states]):
    #             updated_states.append((neighbor, fitness_neighbor))
    #     #if no neighbor improves the values, return the initial states
    #     if not updated_states:
    #         print("no neigbor improved value")
    #         return states
    #
    #     best_fit = self.get_smallest_values(updated_states, self.beam_width)
    #     print("bestfit", [self.get_fitness(best_state, relevant) for best_state in best_fit])
    #     print(12 in [self.get_fitness(best_state, relevant)[0] for best_state in best_fit])
    #     if 12 in [self.get_fitness(best_state, relevant)[0] for best_state in best_fit] or step == 10:
    #         for b in best_fit:
    #             # print(self.get_fitness(b, relevant))
    #             if self.get_fitness(b, relevant)[0] == 12:
    #                 print("found best")
    #     else:
    #         step += 1
    #         self.explore(best_fit, step)
    #


    # def beam_search(self, relevant, order):
    #     L = len(relevant)
    #     goal = len(order)
    #     print(goal)
    #     print(order)
    #     #start with 3 random states
    #     init_states = [np.random.choice([0,1], size=(L,), p=[1 - len(order) / L, len(order) / L]) for i in range(self.beam_width)]
    #     # self.explore(init_states)
    #     self.find_best_neighbors(init_states)
        # neighbors = self.get_neighbors(init_states, relevant)
        # steps = 0
        # updated_states = []
        # print("fit initial states", [self.get_fitness(state, relevant)[1] for state in init_states])
        # for neighbor in neighbors:
        #     fitness = self.get_fitness(neighbor, relevant)
        #     #if any neighbor is a better fit than the current state
        #     if fitness[1] < any([self.get_fitness(state, relevant)[1] for state in init_states]):
        #         if fitness[0] == 12:
        #             return neighbor
        #         else:
        #         # print("better", self.get_fitness(neighbor, relevant))
        #             updated_states.append((neighbor, fitness[1]))
        #             print("covered items", fitness[0], fitness[1])
        # best_fit = self.get_smallest_values(updated_states, self.beam_width)
        # print("best fits", best_fit)
        # new_neighbors = self.get_neighbors(best_fit, relevant)
        # print("len neigh", len(new_neighbors))
        #
        # for state in init_states:
        #     covered_items, current_state = self.get_fitness(state, relevant)
        #     #print("state", current_state, "covered", covered_items)
        #     for neighbor in neighbors:
        #         new_covered, new_state = self.get_fitness(neighbor, relevant)
        #         #print(current_state, new_state)
        #         if new_state < current_state:
        #             updated_states.append(neighbor)
        #             # print("new", new_state)
        #         else:
        #             updated_states.append(state)
        #         cov = self.get_covered_items(neighbor, relevant)
        #         cov = set([u for sublist in cov for u in sublist])
        #         #print("state", cov, "len:", len(cov), "fitness:", new_state)

       # for neighbor in neighbors:
       #      fitness = self.get_fitness(neighbor, relevant)
       #      cov = self.get_covered_items(state, relevant)
       #      cov = set([u for sublist in cov for u in sublist])
       #      print("neighbor", cov, "len:", len(cov), "fitness:", fitness)
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

bs.beam_search()
