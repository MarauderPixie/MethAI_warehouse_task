import random
import numpy as np
from warehouse import Warehouse

class FirstChoiceHillClimbing(Warehouse):
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
    def retrieve_units(self, state):  # TODO rename retrieve_psus() or smth?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved

    '''
        given a state, look at the nearest neighbor and return it if it improves the cost value 
        if no neighbor improves it, return the initial state
    '''
    def make_move_hill(self, state):
        neighbor = self.get_neighbor(state)
        cost_current = self.get_cost(state)
        cost_neighbor = self.get_cost(neighbor)

        return neighbor if cost_current <= cost_neighbor else state

    '''
        perform first choice hill climbing
        return 
    '''

    def first_choice_hill_climbing(self):  # R= relevant, O = order
        l = len(self.warehouse.relevant_units)
        # generate the initial state as an array of 1s and 0s with probability TODO how was p chosen
        initial_state = np.random.choice([0, 1], size=(l,),
                                 p=[1 -  self.warehouse.goal / l,  self.warehouse.goal / l])  # rendom array 0=PSU not used 1=PSUused
        step = 0
        # keep exploring until the number of covered items corresponds to the number of items in order
        while (len(self.get_covered_items(initial_state)) != self.warehouse.goal):
            initial_state = self.make_move_hill(initial_state)
            step += 1

        best_state = initial_state
        retrieved_units = self.retrieve_units(best_state)
        retrieved_items = len(self.get_covered_items(best_state))
        number_used_units = sum(best_state)
        print("iterations:", step, 
              "\nPSUs used:", number_used_units, 
              "\ncovered:", retrieved_items, 
              "\nItems in order:", self.warehouse.goal, 
              "\nContent of used PSUs:", retrieved_units)



path_w = "data/problem1.txt"
path_o = "data/order11.txt"
fchc = FirstChoiceHillClimbing(path_w, path_o)
fchc.first_choice_hill_climbing()
