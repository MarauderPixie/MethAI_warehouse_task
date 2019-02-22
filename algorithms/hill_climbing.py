import random
from warehouse import Warehouse
import numpy as np
# --------- Hill Climbing --------------

def get_covered_items_hill(state, R):
    cov = []
    for i in range(len(state)):
        if state[i] == 1:
            cov.append(R[i])
    cov = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
    print(cov)
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
    print(cov)
    cov = len(cov)
    print("covr", cov)
    Noused = sum(state)
    print("iterations:", k, "PSUs used:", Noused,"covered:", cov, "Items in order:", goal, "items", li)

    return state, Noused, li

hill_climbing(relevant, NoOrder12)
