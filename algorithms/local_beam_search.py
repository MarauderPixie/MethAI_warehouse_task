import random
import numpy as np
import copy
from warehouse import Warehouse

#TODO store indices of psus for access at the end
#TODO select neighbors
class BeamSearch(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order, beam_width):
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
        fit = round(len(covered) - (0.9 * y), 3) # fit is the number of covered items minus the number of PSUs
        return (len(covered),fit)

    def get_nhb(self, states):
        neighborhood = []
        for state in states:
            nhb = state.copy()
            x = random.choice(range(0, len(nhb) - 1))
            y = random.choice(range(0, len(nhb) - 1))
            z = np.random.choice([0, 1], 1)
            nhb[x] = 0
            if z == 0:
                nhb[y] = 0
            else:
                nhb[y] = 1
            neighborhood.append(nhb)
        print("psus", [sum(n) for n in neighborhood])
        return neighborhood

    #neighborhood is obtained by randomly picking units from within an n-window from the PSU units already retrieved in that state
    def get_neighbors(self, states):
        neighborhood = []
        window = 3
        for state in states:
            #indices of the units that contain the relevant items
            indices = [index for index, value in enumerate(state) if value == 1]
            for i in range(self.beam_width):
                succesor = copy.deepcopy(state)
                #for each relevant unit, look at the units in an n-window around it and randomly change some of them
                for index in indices:
                    if index - window > 0 and index + window < len(self.warehouse.relevant_units)-1:
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
        neighbors = self.get_nhb(states)
        for neighbor in neighbors:
            fitness_neighbor = self.get_fitness(neighbor)
            if fitness_neighbor[1] < any([self.get_fitness(state)[1] for state in states]):
                updated_states.append((neighbor, fitness_neighbor))
        # if no neighbor improves the values, return the initial states
        if not updated_states:
            print("no neigbor improved value")
            return states
        #print(updated_states)
        best_fit = self.get_smallest_values(updated_states, self.beam_width)
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

    def PSU_used(self, S):
        cov = []
        for i in range(len(S)):
            if S[i] == 1:
                cov.append(i)
        return cov

    def convert_item_in_order(self, word_list, dictionary):
        new_list = [dictionary.get(item) for item in word_list]
        return new_list

    def get_item_of_used_PSU(self, idx):  # gets list of index of PSU and what it caries
        new_list = []
        for i in idx:
            new_list.append((i, self.warehouse.encoded_warehouse[i]))
        return new_list

    def dic_rel_psu(self):
        psu_index = [i for i, j in enumerate(self.warehouse.stock) if j]

        dictionary_rel_PSU = {}
        i: int
        for i in range(len(psu_index)):
            dictionary_rel_PSU[i] = psu_index[i]
        return dictionary_rel_PSU

    def beam_search(self):
        L = len(self.warehouse.relevant_units)
        init_states = [np.random.choice([0, 1], size=(L,), p=[1 - self.warehouse.goal / L, self.warehouse.goal / L]) for i in range(self.beam_width)]
        state_best = self.explore(init_states)
        index = self.PSU_used(state_best)  # index of used PSUs
        idxPSU = self.convert_item_in_order(index, self.dic_rel_psu())
        li = self.get_item_of_used_PSU(idxPSU)  # list of index of PSU and what it caries
        print(li)

        cov = self.get_covered_items(state_best)
        print(cov)
        cov = set([u for sublist in cov for u in sublist])
        cov = len(cov)
        print("covr", cov)
        Noused = sum(state_best)
        print("PSUs used:", Noused, "covered:", cov, "Items in order:", self.warehouse.goal, "items", li)
        # for l in li:
        #     self.warehouse.decode_items(self.warehouse.stock_count,l[1])


# path_w = "/../data/problem1.txt"
# path_o = "/../data/order11.txt"
# w = warehouse.Warehouse(path_w,path_o)
# # bs = BeamSearch(w)
# # bs = BeamSearch(NoWarehouse, NoOrder12)
# # print("all psus with the items inside:", bs.warehouse)
# # print("order:", bs.order)
# # print("prune:", len(bs.prune()), bs.prune())
# #
# bs.beam_search()
