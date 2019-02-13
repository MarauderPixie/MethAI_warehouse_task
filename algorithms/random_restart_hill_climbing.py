# -------difference to hill climbing is just the junction at the bottom where you use the hill climb N times-------
# --------  random_restart_hill_climbing(relevant, NoOrder12, N)  -----------

"""Progamming Task Methods of AI"""
import random
import numpy as np
import itertools
import math
##################################################
######important importing#########################
#import qt
##################################################
#GOAL: we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma


#1. read in the text file with the warehouse information
warehouse = []
for line in open("problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[0] #the first line, what is in stock
warehouse = warehouse[2:] #now we have a list of the psus

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
    dictionary_stock[stock[i]] = i

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


## define function to get only those PSUs containing at least one of the ordered items
def get_relevant_psus(order, PSU):
    psu_list = []
    for rob in PSU:
        bob = [item for item in rob if item in order]
        psu_list.append(bob)
    return psu_list

## call function on order
relevant = get_relevant_psus(NoOrder12, NoWarehouse)

## get indices of relevant PSUs and remove "empty" PSUs from list
psu_index = [i for i, j in enumerate(relevant) if j]
relevant = list(filter(None, relevant))

#dictionary relevant PSU
dictionary_rel_PSU = {}
i: int
for i in range(len(psu_index)):
    dictionary_rel_PSU[i] = psu_index[i]

def PSU_used(S):
    cov = []
    for i in range(len(S)):
        if S[i] == 1:
            cov.append(i)
    return cov

def get_item_of_used_PSU(idx): # gets list of index of PSU and what it caries
    new_list = []
    for i in idx:
        new_list.append((i, NoWarehouse[i]))
    return new_list

# --------- Hill Climbing --------------

def get_covered_items_hill(state, R):
    cov = []
    for i in range(len(state)):
        if state[i] == 1:
            cov.append(R[i])
    cov = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
    return cov

def get_fitness_hill(state, R):
    covered = get_covered_items_hill(state, R)
    y = sum(state)  # number of PSUs used
    fit = len(covered) - y  # fit is the number of covered items minus the number of PSUs
    return fit

def get_neighbor_hill(state):
    nhb = state.copy()
    x = random.choice(range(0, len(nhb) - 1))
    y = random.choice(range(0, len(nhb) - 1))
    u = random.choice(range(0, len(nhb) - 1))
    z = np.random.choice([0, 1], 1)
    nhb[x] = 0
    nhb[u] = 0
    if z == 0:
        nhb[y] = 0
    else:
        nhb[y] = 1

    return nhb

def make_move_hill(state, R):
    nhb_1 = get_neighbor_hill(state)
    nhb_2 = get_neighbor_hill(state)
    nhb_3 = get_neighbor_hill(state)
    current = get_fitness_hill(state, R)
    new_1 = get_fitness_hill(nhb_1, R)
    new_2 = get_fitness_hill(nhb_2, R)
    new_3 = get_fitness_hill(nhb_3, R)
    y = max(new_1, new_2, new_3)
    u = (new_1, new_2, new_3).index(y)
    if u == 0:
        new = new_1
        nhb = nhb_1
    elif u == 1:
        new = new_2
        nhb = nhb_2
    else:
        new = new_3
        nhb = nhb_3
    return nhb if current <= new else state


def hill_climbing(R, O):  # R= relevant, O = order
    L = len(R)
    goal = len(O)
    state = np.random.choice([0, 1], size=(L, ), p=[1-len(O)/L, len(O)/L])  #rendom array 0=PSU not used 1=PSUused
    k = 0

    while (len(get_covered_items_hill(state, R)) != goal):
        state = make_move_hill(state, R)
        k += 1

    index = PSU_used(state)  # index of used PSUs
    idxPSU = convert_item_in_order(index, dictionary_rel_PSU)
    li = get_item_of_used_PSU(idxPSU)  # list of index of PSU and what it caries
    cov = get_covered_items_hill(state, R)
    #print(cov)
    cov = len(cov)
    #print("covr", cov)
    Noused = sum(state)
    #print("iterations:", k, "PSUs used:", Noused,"covered:", cov, "Items in order:", goal, "items", li)

    return state, Noused, li

f = hill_climbing(relevant, NoOrder12)


#  -------------- Random restart hill climbing ---------------

def random_restart_hill_climbing(rel, order, Noresets):
    state = hill_climbing(rel, order)
    for _ in itertools.repeat(None, Noresets):
        reset = hill_climbing(rel, order)
        if reset[1] <= state[1]:
            state = reset
    return state


random_restart_hill_climbing(relevant, NoOrder12, 5)
