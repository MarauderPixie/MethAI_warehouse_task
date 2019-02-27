"""
    Class generates a neighborhood and explores it using
    first choice hill climbing algorithm.
"""

import random
from gui.warehouse import Warehouse
import numpy as np

class HillClimbing(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)

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
        # flatten list of list and throw out duplicats
        items = set([item for sublist in items for item in sublist])

        return items

    '''
        Calculate the cost of a state 
        Cost is the number of covered items in that state minus the number of PSUs used 
    '''
    def get_cost(self, state):
        covered_items = self.get_covered_items(state)
        units_used = sum(state)
        cost = len(covered_items) - units_used

        return cost

    '''
        Generate neighbors of a state by randomly setting two units to 0 with 100% probability, and one with 50% probability
    '''
    def get_neighbors(self, state):
        neighbor = state.copy()
        x = random.choice(range(0, len(neighbor) - 1))
        y = random.choice(range(0, len(neighbor) - 1))
        u = random.choice(range(0, len(neighbor) - 1))
        z = np.random.choice([0, 1], 1)
        neighbor[x] = 0
        neighbor[u] = 0
        if z == 0:
            neighbor[y] = 0
        else:
            neighbor[y] = 1

        return neighbor

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
        Explore new states to improve the objective function
    '''
    def explore(self, state):
        nhb_1 = self.get_neighbors(state)
        nhb_2 = self.get_neighbors(state)
        nhb_3 = self.get_neighbors(state)
        current = self.get_cost(state)
        new_1 = self.get_cost(nhb_1)
        new_2 = self.get_cost(nhb_2)
        new_3 = self.get_cost(nhb_3)
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

    '''
        Perform hill climbing 
        Return the output in the shape of a dictionary containing the number of used units, a tuple with
        their index and the items they contain, the items from the order covered and the number of iterations
    '''
    def hill_climbing(self):
        length = len(self.warehouse.relevant_units)
        # generate the initial state as an array of 1s and 0s with probability based on the goal
        # 1 = PSU is used 0 = PSU is not used
        state = np.random.choice([0, 1], size=(length, ), p=[1-self.warehouse.goal/length, self.warehouse.goal/length])
        step = 0

        while (len(self.get_covered_items(state)) != self.warehouse.goal):
            state = self.explore(state)
            step += 1

        retrieved_units = self.retrieve_units(state)
        retrieved_items = len(self.get_covered_items(state))
        number_used_units = sum(state)
        #decode the items from numbers to natural language
        units = [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units]
        output = {"goal": self.warehouse.goal,
                  "iterations": step,
                  "covered_items": retrieved_items,
                  "number_units": number_used_units,
                  "units": units,
                  }

        return output
