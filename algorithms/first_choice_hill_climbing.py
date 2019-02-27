"""
    Class generates a neighborhood and explores it using
    first choice hill climbing algorithm.
"""

import random
import numpy as np
from gui.warehouse import Warehouse

class FirstChoiceHillClimbing(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)

    '''
        Return a list of all items from the order covered in the particular state
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
        Generate a neighborhood by setting 2 random psus to 0 with 100% probability
        and one of them to 1 with a 50% probability
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
        Given a state, look at the nearest neighbor and return it, if it improves the cost value
        If no neighbor improves it, return the initial state
    '''
    def explore(self, state):
        neighbor = self.get_neighbors(state)
        cost_current = self.get_cost(state)
        cost_neighbor = self.get_cost(neighbor)

        return neighbor if cost_current <= cost_neighbor else state


    '''
        Perform first choice hill climbing
        Return the output in the shape of a dictionary containing the number of used units, a tuple with
        their index and the items they contain, the items from the order covered and the number of iterations
    '''

    def first_choice_hill_climbing(self):
        length = len(self.warehouse.relevant_units)
        # generate the initial state as an array of 1s and 0s with probability based on the goal
        # 1 = PSU is used 0 = PSU is not used
        initial_state = np.random.choice([0, 1], size=(length,),
                                 p=[1 -  self.warehouse.goal / length,  self.warehouse.goal / length])
        step = 0
        # keep exploring until the number of covered items corresponds to the number of items in order
        while (len(self.get_covered_items(initial_state)) != self.warehouse.goal):
            initial_state = self.explore(initial_state)
            step += 1

        best_state = initial_state
        retrieved_units = self.retrieve_units(best_state)
        retrieved_items = len(self.get_covered_items(best_state))
        number_used_units = sum(best_state)
        #decode the items from numbers to natural language
        units = [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units]

        output = {"goal" : self.warehouse.goal,
                  "iterations": step,
                  "covered_items": retrieved_items,
                  "number_units" : number_used_units,
                  "units" : units
        }

        return output


