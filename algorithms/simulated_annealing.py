"""Progamming Task Methods of AI"""
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

# get idices of PSUs with more than one item
def get_cool_PSU(rel):
    new = []
    for items in rel:
        if len(items) > 1:
            new.append(rel.index(items))
    return new

cool_psu = get_cool_PSU(relevant)


#simulated annealing
#INITIALIZE search state s, temperature t

def update_temperature(T):
    return T - 0.0005

def get_covered_items(S, R):
    cov = []
    for i in range(len(S)):
        if S[i] == 1:
            cov.append(R[i])
    return cov

def get_fitness(S, R):
    cov = get_covered_items(S, R)
    covered = set([item for sublist in cov for item in sublist]) #flattens list of list and throws out duplicats
    y = sum(S) #number of PSUs used
    fit = len(covered) - (0.9* y) #fit is the number of covered items minus the number of PSUs
    return fit

def get_neighbors(test):
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

def make_move(state, R, T):
    nhb = get_neighbors(state)
    current = get_fitness(state, R)
    new = get_fitness(nhb, R)
    delta = new - current

    if delta > 0:
        return nhb
    else:
        p = math.exp(delta / T)
        return nhb if random.random() < p else state

def simulated_annealing(R,O): #A= relevant, O = order
    L = len(R)
    goal = len(O)
    state_0 = np.random.choice([0, 1], size=(L, ), p=[1-len(O)/L, len(O)/L]) #rendom array 0=PSU not used 1=PSUused
    T = 3
    state = state_0.copy()
    state_best = state_0.copy()
    k = 0

    while T > 1e-3:
        state = make_move(state, R, T)
        if get_fitness(state, R) > get_fitness(state_best, R):
            state_best = state.copy()
        T = update_temperature(T)
        k += 1
    index = PSU_used(state_best)  # index of used PSUs
    idxPSU = convert_item_in_order(index, dictionary_rel_PSU)
    li = get_item_of_used_PSU(idxPSU)  # list of index of PSU and what it caries
    cov = get_covered_items(state_best, R)
    print(cov)
    cov = set([u for sublist in cov for u in sublist])
    cov=len(cov)
    print("covr", cov)
    Noused = sum(state_best)
    print("iterations:", k, "PSUs used:", Noused,"covered:", cov, "Items in order:", goal, "items", li)
    return state_best, Noused, li

simulated_annealing(relevant,NoOrder12)
