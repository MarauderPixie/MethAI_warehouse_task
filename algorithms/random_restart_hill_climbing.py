"""
    Class generates a neighborhood and explores it using
    random restart hill climbing algorithm with configurable number of states.
"""

import random
from warehouse import Warehouse
import numpy as np

class RandomRestart(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order, number_states):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)
        self.number_states = number_states
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
    def get_neighbor(self, state):
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
        Generate three neighbors, choose the best neighbor and compare it to the initial state
    '''
    def explore(self, state):
        nhb_1 = self.get_neighbor(state)
        nhb_2 = self.get_neighbor(state)
        nhb_3 = self.get_neighbor(state)
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
        Perform hill climbing starting with an random initial state
    '''
    def hill_climbing(self):
        length = len(self.warehouse.relevant_units)
        self.step = 0
        # generate the initial state as an array of 1s and 0s with probability based on the goal
        # 1 = PSU is used 0 = PSU is not used
        state = np.random.choice([0, 1], size=(length, ), p=[1-self.warehouse.goal/length, self.warehouse.goal/length])

        while len(self.get_covered_items(state)) != self.warehouse.goal:
            state = self.explore(state)
            self.step += 1

        return state

    '''
        Perform n random restarts, where n is a number chosen by the user
    '''
    def random_restart(self):
        new_state = self.hill_climbing()

        for _ in range(self.number_states):
            current_state = self.hill_climbing()
            # because fewer PSUs is better:
            if sum(current_state) <= sum(new_state):
                print(sum(current_state, sum(new_state)))
                new_state = current_state

        retrieved_units = self.retrieve_units(current_state)
        retrieved_items = len(self.get_covered_items(current_state))
        number_used_units = sum(current_state)
        units = [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units]
        output = {"goal": self.warehouse.goal,
                  "iterations": self.step,
                  "covered_items": retrieved_items,
                  "number_units": number_used_units,
                  "units": units,
                  }

        return output
