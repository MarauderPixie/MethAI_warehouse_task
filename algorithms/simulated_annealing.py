import random
import numpy as np
import math
from warehouse import Warehouse


class SimulatedAnnealing(Warehouse):
    def __init__(self, filepath_warehouse, filepath_order):
        self.warehouse = Warehouse(filepath_warehouse, filepath_order)

    def get_covered_items(self, state):
        cov = []
        for i in range(len(state)):
            if state[i] == 1:
                cov.append(self.warehouse.relevant_units[i])
        return cov

    def get_fitness(self, state):
        cov = self.get_covered_items(state)
        covered = set(
            [item for sublist in cov for item in sublist])  # flattens list of list and throws out duplicats
        y = sum(state)  # number of PSUs used
        fit = round(len(covered) - (0.9 * y), 3)  # fit is the number of covered items minus the number of PSUs
        return len(covered), fit

    # with every step, the temperature decreases by 0.0005
    def update_temperature(self, t):
        return t - 0.0005

    # one neighbor or more neighbors?
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


    # look at the neighbor of a state and return it if it increases the value
    def make_move(self, state, temperature):
        neighbor = self.get_neighbors(state)
        current_state = self.get_fitness(state)[1]
        new_state = self.get_fitness(neighbor)[1]
        delta = new_state - current_state

        if delta > 0:
            return neighbor
        else:
            p = math.exp(delta / temperature)
            return neighbor if random.random() < p else state


    # takes a state as an input and returns the corresponding PSUs with their indices and the items they contain
    def translate_state(self, state): #TODO rename retrieve_psus() or smth? lookup_state and move into Warehouse?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved
    def retrieve_units(self, state):  # TODO rename retrieve_psus() or smth?
        retrieved = []
        for i in range(len(state)):
            if state[i] == 1:
                index = self.warehouse.indices_relevant_units[i]
                items = self.warehouse.encoded_warehouse[index]
                retrieved.append((index, items))
        return retrieved

    ## call function on order
    def simulated_annealing(self): #A= relevant, O = order
        len_relevant_units = len(self.warehouse.relevant_units)
        goal = len(self.warehouse.order)
        temperature = 3
        step = 0

        #generate a random initial state with probability TODO p = ?
        state_0 = np.random.choice([0, 1], size=(len_relevant_units, ), p=[1-goal/len_relevant_units, goal/len_relevant_units]) #rendom array 0=PSU not used 1=PSUused

        state = state_0.copy()
        state_best = state_0.copy()

        while temperature > 1e-3:
            fitness_best_state = self.get_fitness(state_best)
            state = self.make_move(state, temperature)
            if self.get_fitness(state)[1] > fitness_best_state[1]:
                state_best = state.copy()
            temperature = self.update_temperature(temperature)
            step += 1
        retrieved_units = self.retrieve_units(state_best)
        retrieved_items = len(self.get_covered_items(state_best))

        cov = self.get_fitness(state_best)[0]
        # print("iterations:", step,
        #       "\nPSUs used:", sum(state_best),
        #       "\ncovered:", cov,
        #       "\nItems in order:", goal,
        #       "\nContent of used PSUs:", self.translate_state(state_best))
        # return state_best, sum(state_best), self.translate_state(state_best)
        output = {"number_units": sum(state_best),
                  "units": [(i[0], self.warehouse.decode_items(i[1])) for i in retrieved_units],
                  "covered_items": retrieved_items,
                  "goal": self.warehouse.goal
                  }
        return output

# path_w = "../data/problem1.txt"
# path_o = "../data/order11.txt"
# sa = SimulatedAnnealing(path_w,path_o)
# sa.simulated_annealing()
