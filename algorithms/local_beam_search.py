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

    '''
        return a list of all items from the order covered in the particular state
        for the goal to be reached, number of covered items must be equal to number of items in order
    '''
    def get_covered_items(self, state):
        items = []
        # if an index of the state is 1, retrieve the items from psu with the same index
        for i in range(len(state)):
            if state[i] == 1:
                items.append(self.warehouse.relevant_units[i])
        # flatten list of list and throw out duplicats
        items = set([item for sublist in items for item in sublist])

        return items
    # def get_covered_items(self, state):
    #     cov = []
    #     for i in range(len(state)):
    #         if state[i] == 1:
    #             cov.append(self.warehouse.relevant_units[i])
    #     return cov


    def get_fitness(self, state):
        covered = self.get_covered_items(state)
        # covered = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
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


    '''
        helper function for returning the smallest value of an array of tuples based on the second element 
    '''
    def get_smallest_values(self, arr, n):
        best_fit = []
        arr.sort(key=lambda tup: tup[1][1], reverse=True)
        if len(arr) < n:
            return  [n[0] for n in arr]
        else:
            for i in range(n):
                best_fit.append(arr[i][0])
            return best_fit

    '''
        generate neighbors for each state and return the n best states. 
        if no neighbor improves the value, return the state
    '''
    def find_best_neighbors(self, states):
        updated_states = []
        for state in states:
            updated_states.append((state, self.get_fitness(state)))
        neighbors = self.get_nhb(states)
        for neighbor in neighbors:
            updated_states.append((neighbor, self.get_fitness(neighbor)))
        best_fit = self.get_smallest_values(updated_states, self.beam_width)

        return best_fit

    def explore(self, state, step=None):
        if step is None:
            step = 1
        best_neighbors = self.find_best_neighbors(state)
        if self.warehouse.goal in [self.get_fitness(best_state)[0] for best_state in best_neighbors]:
            for b in best_neighbors:
                if self.get_fitness(b)[0] == self.warehouse.goal or step == 10:
                    return b
        else:
            step += 1
            return self.explore(best_neighbors, step)


        # takes a state as an input and returns the corresponding PSUs with their indices and the items they contain
    def retrieve_units(self, state):  # TODO rename retrieve_psus() or smth?
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

        cov = self.get_fitness(state_best)[0]
        retrieved_items = len(self.get_covered_items(state_best))
        retrieved_units = self.retrieve_units(state_best)

        Noused = sum(state_best)
        print("beam search PSUs used:", Noused, "covered:", cov, "Items in order:", self.warehouse.goal, "items", self.retrieve_units(state_best))

        output = {"number_units": Noused,
                  "units": [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units],
                  "covered_items": retrieved_items,
                  "goal": self.warehouse.goal
                  }
        # print(output)
        return output
        # for i in self.translate_state(state_best):
        #     print(self.warehouse.decode_items(i[1]))
