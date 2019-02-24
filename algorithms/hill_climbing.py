import random
from warehouse import Warehouse
import numpy as np


class HillClimbing(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)

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

    '''
        calculate the cost of a state 
        cost is the number of covered items in that state minus the number of PSUs used 
    '''

    def get_cost(self, state):
        covered_items = self.get_covered_items(state)
        units_used = sum(state)
        cost = len(covered_items) - units_used

        return cost

    '''
        generate neighbors of a state by randomly setting two units to 0 with 100% probability, and one with 50% probability
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
        given a state, return a tuple containing the corresponding PSU and a list of the items inside it
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
        explore new states to improve the objective function
    '''
    def make_move_hill(self, state):
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
    perform hill climbing 
    '''
    def hill_climbing(self):
        L = len(self.warehouse.relevant_units)
        state = np.random.choice([0, 1], size=(L, ), p=[1-self.warehouse.goal/L, self.warehouse.goal/L])  #rendom array 0=PSU not used 1=PSUused
        k = 0

        while (len(self.get_covered_items(state)) != self.warehouse.goal):
            state = self.make_move_hill(state)
            k += 1


        retrieved_units = self.retrieve_units(state)

        retrieved_items = len(self.get_covered_items(state))

        number_used_units = sum(state)
        output = {"number_units": number_used_units,
                  "units": [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units],
                  "iterations": k,
                  "covered_items": retrieved_items,
                  "goal": self.warehouse.goal
                  }

        return output
        # print("iterations:", k,
        #       "\nPSUs used:", number_used_units,
        #       "\ncovered:", retrieved_items,
        #       "\nItems in order:", self.warehouse.goal,
        #       "\nContent of used PSUs:", retrieved_units)

