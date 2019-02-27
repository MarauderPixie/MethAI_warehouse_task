"""
    Class generates a neighborhood and explores it using
    local beam search algorithm.
"""
import random
import numpy as np
from gui.warehouse import Warehouse

class BeamSearch(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order, beam_width):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)
        self.beam_width = beam_width
        self.step = 0
    '''
        Return a list of all items from the order covered in the particular state
        For the goal to be reached, number of covered items must be equal to number of items in order
    '''
    def get_covered_items(self, state):
        items = []
        # if an index of the state is 1, retrieve the items from psu with the same index
        for i in range(len(state)):
            if state[i] == 1:
                items.append(self.warehouse.relevant_units[i])
        # flatten list of list and throw out duplicates
        items = set([item for sublist in items for item in sublist])

        return items

    '''
        Calculates how good a state is by subtracting the number of PSUs used from the number of covered items
        We want to have as many covered items with as few PSUs as possible
        Returns a tuple with the number of covered items, and the fitness value
    '''
    def get_fitness(self, state):
        covered = self.get_covered_items(state)
        y = sum(state)  # number of PSUs used
        # by multiplying y with a number we can set a bias for the psus/items
        # reducing y means getting the correct number of items is more important
        fit = round(len(covered) - (0.9 * y), 3)

        return (len(covered),fit)


    '''
        Generate neighbors of a state by randomly setting two units to 0 with 100% probability, and one with 50% probability
    '''
    def get_neighbors(self, states):
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


    '''
        Helper function for returning the smallest value of an array of tuples based on the second element 
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
        Compare the neighbors for each state. If no neighbor improves the fitness value, return the state
    '''
    def find_best_neighbors(self, states):
        updated_states = []
        for state in states:
            updated_states.append((state, self.get_fitness(state)))
        neighbors = self.get_neighbors(states)
        for neighbor in neighbors:
            updated_states.append((neighbor, self.get_fitness(neighbor)))
        best_fit = self.get_smallest_values(updated_states, self.beam_width)

        return best_fit

    '''
        Explore the neighborhood and return the best n states, where n = beam_width chosen by the user
    '''
    def explore(self, state, step=None):
        step = step
        if step is None:
            step = 1
        best_neighbors = self.find_best_neighbors(state)
        if self.warehouse.goal in [self.get_fitness(best_state)[0] for best_state in best_neighbors]:
            for b in best_neighbors:
                if self.get_fitness(b)[0] == self.warehouse.goal:   # or self.step == 10
                    self.step = step
                    return b
        else:
            step += 1
            return self.explore(best_neighbors, step)

    '''
        Given a state, return a tuple containing the corresponding PSU and a list of the items inside it
    '''
    def retrieve_units(self, state):
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved

    '''
        Perform local beam search
    '''
    def beam_search(self):
        length = len(self.warehouse.relevant_units)
        # generate the initial state as an array of 1s and 0s with probability based on the goal
        # 1 = PSU is used 0 = PSU is not used
        init_states = [np.random.choice([0, 1], size=(length,), p=[1 - self.warehouse.goal / length, self.warehouse.goal / length]) for i in range(self.beam_width)]
        best_state = self.explore(init_states)

        retrieved_items = len(self.get_covered_items(best_state))
        number_used_units = sum(best_state)
        retrieved_units = self.retrieve_units(best_state)
        # decode the items from numbers to natural language
        units = [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units]

        output = {"goal": self.warehouse.goal,
                  "iterations": self.step,
                  "covered_items": retrieved_items,
                  "number_units": number_used_units,
                  "units": units,
                  }

        return output

