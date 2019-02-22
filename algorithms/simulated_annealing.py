"""Progamming Task Methods of AI"""
import random
import numpy as np
import math
from warehouse import Warehouse


class SimulatedAnnealing(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)

    def get_covered_items(self, state):
        cov = []
        for i in range(len(state)):
            if state[i] == 1:
                cov.append(self.warehouse.relevant_units[i])
        return cov

    def get_fitness(self, state):
        cov = self.get_covered_items(state)
        covered = set(
            [item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
        y = sum(state)  # number of PSUs used
        fit = round(len(covered) - (0.9 * y), 3)  # fit is the number of covered items minus the number of PSUs
        return len(covered), fit

    # with every step, the temperature decreases by 0.0005
    def update_temperature(self, t):
        return t - 0.0005

    # one neighbor or more neighbors?
    def get_neighbors(self, test):
        nhb = test.copy()
        x = random.choice(range(0, len(nhb) - 1))
        y = random.choice(range(0, len(nhb) - 1))
        z = np.random.choice([0, 1], 1)
        nhb[x] = 0
        if z == 0:
            nhb[y] = 0
        else:
            nhb[y] = 1
        return nhb


    # look at the neighbor of a state and return it if it increases the value
    def make_move(self, state, temperature):
        neighbor = self.get_neighbors(state)
        current_state = self.get_fitness(state)[1]
        new_state = self.get_fitness(neighbor)[1]
        delta = new_state - current_state

        if delta > 0:
            return neighbor
        else:
            p = math.exp(delta / temperature)
            return neighbor if random.random() < p else state


    # takes a state as an input and returns the corresponding PSUs with their indices and the items they contain
    def translate_state(self, state): #TODO rename retrieve_psus() or smth? lookup_state and move into Warehouse?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved


    ## call function on order
    def simulated_annealing(self): #A= relevant, O = order
        len_relevant_units = len(self.warehouse.relevant_units)
        goal = len(self.warehouse.order)
        temperature = 3
        step = 0

        #generate a random initial state with probability TODO p = ?
        state_0 = np.random.choice([0, 1], size=(len_relevant_units, ), p=[1-goal/len_relevant_units, goal/len_relevant_units]) #rendom array 0=PSU not used 1=PSUused

        state = state_0.copy()
        state_best = state_0.copy()

        while temperature > 1e-3:
            fitness_best_state = self.get_fitness(state_best)
            state = self.make_move(state, temperature)
            if self.get_fitness(state)[1] > fitness_best_state[1]:
                state_best = state.copy()
            temperature = self.update_temperature(temperature)
            step += 1

        cov = self.get_fitness(state_best)[0]
        print("iterations:", step, "PSUs used:", sum(state_best),"covered:", cov, "Items in order:", goal, "items", self.translate_state(state_best))
        # return state_best, sum(state_best), self.translate_state(state_best)


path_w = "../data/problem1.txt"
path_o = "../data/order11.txt"
sa = SimulatedAnnealing(path_w,path_o)
sa.simulated_annealing()



        # ##################################################
# ######important importing#########################
# #import qt
# ##################################################
# #GOAL: we want a psu carry as many items possible of our order
#
# # find items in problem:
# # first line all the items there are but without numbers in stock
# # each line is one psu and whtas inside, seperated by comma
#
#
# #1. read in the text file with the warehouse information
# warehouse = []
# for line in open("../data/problem1.txt"):
#         psu = line.strip().split(" ")
#         warehouse.append(psu)
# stock = warehouse[0] #the first line, what is in stock
# warehouse = warehouse[2:] #now we have a list of the psus
#
# #2. open the order11, store in list
# for item in open("../data/order11.txt"):
#     order11 = item.split(" ")
#
# #3. open the order12
# for item in open("../data/order12.txt"):
#     order12 = item.split(" ")
#
# # Dictionary items to numbers
# dictionary_stock = {}
# i: int
# for i in range(len(stock)):
#     dictionary_stock[stock[i]] = i
#
# # convert the items in the PSUs to Numbers.
# def replace_matched_PSU(word_list, dictionary):
#     new_list = [[dictionary.get(item, item) for item in lst] for lst in word_list]
#     return new_list
# NoWarehouse = replace_matched_PSU(warehouse, dictionary_stock)
# #print(NoWarehouse)
#
# # convert the items in the order to Numbers
# def convert_item_in_order(word_list, dictionary):
#     new_list = [dictionary.get(item) for item in word_list]
#     return new_list
# NoOrder11 = convert_item_in_order(order11,dictionary_stock)
# NoOrder12 = convert_item_in_order(order12,dictionary_stock)
#
#
# ## define function to get only those PSUs containing at least one of the ordered items
# def get_relevant_psus(order, PSU):
#     psu_list = []
#     for rob in PSU:
#         bob = [item for item in rob if item in order]
#         psu_list.append(bob)
#     return psu_list
#
# ## call function on order
# relevant = get_relevant_psus(NoOrder12, NoWarehouse)
#
# ## get indices of relevant PSUs and remove "empty" PSUs from list
# psu_index = [i for i, j in enumerate(relevant) if j]
# relevant = list(filter(None, relevant))
#
# #dictionary relevant PSU
# dictionary_rel_PSU = {}
# i: int
# for i in range(len(psu_index)):
#     dictionary_rel_PSU[i] = psu_index[i]
#
# def PSU_used(S):
#     cov = []
#     for i in range(len(S)):
#         if S[i] == 1:
#             cov.append(i)
#     return cov
#
# def get_item_of_used_PSU(idx): # gets list of index of PSU and what it caries
#     new_list = []
#     for i in idx:
#         new_list.append((i, NoWarehouse[i]))
#     return new_list
#
# # get idices of PSUs with more than one item
# def get_cool_PSU(rel):
#     new = []
#     for items in rel:
#         if len(items) > 1:
#             new.append(rel.index(items))
#     return new
#
# cool_psu = get_cool_PSU(relevant)
#

#simulated annealing
#INITIALIZE search state s, temperature t