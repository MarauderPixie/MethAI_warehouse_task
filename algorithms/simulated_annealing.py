"""
    Class generates a neighborhood and explores it using
    simulated annealing algorithm.
"""

import random
import numpy as np
import math
from warehouse import Warehouse

#TODO iterations is always 5998, is that a problem? seems like a lot

class SimulatedAnnealing(Warehouse):
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
        cov = self.get_covered_items(state)
        covered = set([item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
        y = sum(state)  # number of PSUs used
        # by multiplying y with a number we can set a bias for the psus/items
        # reducing y means getting the correct number of items is more important
        fit = round(len(covered) - (0.9 * y), 3)

        return (len(covered), fit)

    # with every step, the temperature decreases by 0.0005
    def update_temperature(self, t):
        return t - 0.001

    '''
       Generate neighbors of a state by randomly setting two units to 0 with 100% probability, and one with 50% probability
   '''
    def get_neighbors(self, test):
        nhb = test.copy()
        x = random.choice(range(0, len(nhb) - 1))
        y = random.choice(range(0, len(nhb) - 1))
        z = np.random.choice([0, 1], 1)
        nhb[x] = 0
        if z == 0:
            nhb[y] = 0
        else:
            nhb[y] = 1
        return nhb


    '''
        Look at the neighbor of a state and return it if it increases the value
    '''
    def make_move(self, state, temperature):
        neighbor = self.get_neighbors(state)
        current_state = self.get_fitness(state)[1]
        new_state = self.get_fitness(neighbor)[1]
        delta = new_state - current_state
        # if the difference between the states is larger than 0, the neighbor improves the objective function
        if delta > 0:
            return neighbor
        else:
            p = math.exp(delta / temperature)
            return neighbor if random.random() < p else state

    '''
        takes a state as an input and returns the corresponding PSUs with their indices and the items they contain
    '''
    def retrieve_units(self, state):  # TODO rename retrieve_psus() or smth?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved

    ## call function on order
    def simulated_annealing(self):
        length = len(self.warehouse.relevant_units)
        temperature = 3
        step = 0
        # generate the initial state as an array of 1s and 0s with probability based on the goal
        # 1 = PSU is used 0 = PSU is not used
        init_state = np.random.choice([0, 1], size=(length, ),
                                      p=[1-self.warehouse.goal/length, self.warehouse.goal/length])

        state = init_state.copy()
        best_state = init_state.copy()

        while temperature > 1e-3:
            fitness_best_state = self.get_fitness(best_state)
        while self.warehouse.goal > self.get_fitness(best_state)[0]:
            fitness_best_state = self.get_fitness(best_state)
            state = self.make_move(state, temperature)
            if self.get_fitness(state)[1] > fitness_best_state[1]:
                best_state = state.copy()
            temperature = self.update_temperature(temperature)
            step += 1

        retrieved_units = self.retrieve_units(best_state)
        retrieved_items = len(self.get_covered_items(best_state))
        units = [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units]
        output = {"goal": self.warehouse.goal,
                  "iterations": step,
                  "number_units": sum(best_state),
                  "covered_items": retrieved_items,
                  "units": units,
        retrieved_units = self.retrieve_units(state_best)
        retrieved_items = len(self.get_covered_items(state_best))

        cov = self.get_fitness(state_best)[0]

        # print("\niterations:", step,
        #       "\nPSUs used:", sum(state_best),
        #       "\ncovered:", cov,
        #       "\nItems in order:", goal,
        #       "\nContent of used PSUs:", self.translate_state(state_best))
        # return state_best, sum(state_best), self.translate_state(state_best)
        output = {"number_units": sum(state_best),
                  "units": [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units],
                  "covered_items": cov,
                  "goal": self.warehouse.goal
                  }

        return output

