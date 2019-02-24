import random
import numpy as np
import copy
from warehouse import Warehouse

#TODO store indices of psus for access at the end
#TODO select neighbors
class BeamSearch(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order, beam_width = 3):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)
        self.beam_width = beam_width

    def get_covered_items(self, state):
        cov = []
        for i in range(len(state)):
            if state[i] == 1:
                cov.append(self.warehouse.relevant_units[i])
        return cov


    def get_fitness(self, state):
        cov = self.get_covered_items(state)
        covered = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats

        y = sum(state)  # number of PSUs used
        # by multiplying y with a number we can set a bias for the psus/items
        # reducing y means higher weight for number of items
        fit = round(len(covered) - (0.9 * y), 3) # fit is the number of covered items minus the number of PSUs
        return (len(covered),fit)

    # def get_nhb(self, states):
    #     neighborhood = []
    #     for state in states:
    #         nhb = state.copy()
    #         x = random.choice(range(0, len(nhb) - 1))
    #         y = random.choice(range(0, len(nhb) - 1))
    #         z = np.random.choice([0, 1], 1)
    #         nhb[x] = 0
    #         if z == 0:
    #             nhb[y] = 0
    #         else:
    #             nhb[y] = 1
    #         neighborhood.append(nhb)
    #     print("psus", [sum(n) for n in neighborhood])
    #     return neighborhood

    def get_nhb(self, states):
        neighborhood = []
        for state in states:
            nhb = state.copy()
            x = random.choice(range(0, len(nhb) - 1))
            y = random.choice(range(0, len(nhb) - 1))
            u = random.choice(range(0, len(nhb) - 1))
            v = random.choice(range(0, len(nhb) - 1))
            z = np.random.choice([0, 1], 1)
            nhb[v] = 0
            nhb[x] = 0
            nhb[u] = 0
            if z == 0:
                nhb[y] = 0
            else:
                nhb[y] = 1
            neighborhood.append(nhb)

        return neighborhood
    #neighborhood is obtained by randomly picking units from within an n-window from the PSU units already retrieved in that state
    def get_neighbors(self, states):
        neighborhood = []
        window = 3
        for state in states:
            #indices of the units that contain the relevant items
            indices = [index for index, value in enumerate(state) if value == 1]
            print("indices", indices)
            for i in range(self.beam_width):
                succesor = state.copy()
                #for each relevant unit, look at the units in an n-window around it and randomly change some of them
                for index in indices:
                    if index - window > 0 and index + window < len(self.warehouse.relevant_units)-1:
                        #randomly pick one unit in the window and change it to 0 if it's 1 and to 1 otherwise
                        k = random.choice(range(index-window, index+window))

                        succesor[k] = 1 if succesor[k] == 0 else 1

                neighborhood.append(succesor)

        return neighborhood


    #get best fit
    def get_smallest_values(self, arr, n):
        # Sort the given array arr in reverse
        # order.
        #arr.sort(reverse=True)
        best_fit = []
        arr.sort(key=lambda tup: tup[1][1], reverse=True)
        # Print the first kth largest elements
        if len(arr) < n:
            return  [n[0] for n in arr]
        else:
            for i in range(n):
                best_fit.append(arr[i][0])
            return best_fit


    def find_best_neighbors(self, states):
        updated_states = []
        neighbors = self.get_nhb(states)
        for neighbor in neighbors:
            print("sum", sum(neighbor))
            fitness_neighbor = self.get_fitness(neighbor)
            print("fitess neigh", fitness_neighbor)
            if fitness_neighbor[1] < any([self.get_fitness(state)[1] for state in states]):
                updated_states.append((neighbor, fitness_neighbor))
        # if no neighbor improves the values, return the initial states
        if not updated_states:
            print("no neigbor improved value")
            return states
        #print(updated_states)
        best_fit = self.get_smallest_values(updated_states, self.beam_width)
        # print("sum", [sum(n) for n in best_fit])
        return best_fit

    def explore(self, state, step=None):
        if step is None:
            step = 1
        print("Step", step)
        best_neighbors = self.find_best_neighbors(state)
        if self.warehouse.goal in [self.get_fitness(best_state)[0] for best_state in best_neighbors]:
            for b in best_neighbors:
                if self.get_fitness(b)[0] == self.warehouse.goal or step == 10:
                    return b
        else:
            step += 1
            return self.explore(best_neighbors, step)


        # takes a state as an input and returns the corresponding PSUs with their indices and the items they contain
    def translate_state(self, state):  # TODO rename retrieve_psus() or smth?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved

    def beam_search(self):
        L = len(self.warehouse.relevant_units)
        init_states = [np.random.choice([0, 1], size=(L,), p=[1 - self.warehouse.goal / L, self.warehouse.goal / L]) for i in range(self.beam_width)]
        state_best = self.explore(init_states)
        # index = self.PSU_used(state_best)  # index of used PSUs
        # idxPSU = self.convert_item_in_order(index, self.dic_rel_psu())
        # li = self.get_item_of_used_PSU(idxPSU)  # list of index of PSU and what it caries
        # print(li)
        #
        cov = self.get_fitness(state_best)[0]

        Noused = sum(state_best)
        print("order", self.warehouse.encoded_order)
        print("beam search PSUs used:", Noused, "covered:", cov, "Items in order:", self.warehouse.goal, "items", self.translate_state(state_best))
        for i in self.translate_state(state_best):
            print(self.warehouse.decode_items(i[1]))




path_w = "data/problem1.txt"
path_o = "data/order11.txt"
bs = BeamSearch(path_w, path_o)
bs.beam_search()
