import random
import numpy as np
import math
##################################################
######important importing#########################
#import qt
##################################################
#GOAL: we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma

warehouse = []
for line in open("../data/problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[0] #the first line, what is in stock
warehouse = warehouse[2:] #now we have a list of the psus
#(warehouse[0])
#print(stock)

#2. open the order11, store in list
for item in open("../data/order11.txt"):
    order11 = item.split(" ")

#3. open the order12
for item in open("../data/order12.txt"):
    order12 = item.split(" ")
    #order_new = order12[2:]

# Dictionary items to numbers
dictionary_stock = {}
for i in range(len(stock)):
    dictionary_stock[stock[i]] = i+1


# convert the items in the PSUs to Numbers.
def replace_matched_PSU(word_list, dictionary):
    new_list = [[dictionary.get(item, item) for item in lst] for lst in word_list]
    return new_list
NoWarehouse = replace_matched_PSU(warehouse, dictionary_stock)

#print(NoWarehouse)

# convert the items in the order to Numbers
def convert_item_in_order(word_list, dictionary):
    new_list = [dictionary.get(item) for item in word_list]
    return new_list
NoOrder11 = convert_item_in_order(order11,dictionary_stock)
NoOrder12 = convert_item_in_order(order12,dictionary_stock)

#1. read in the text file with the warehouse information

#TODO store indices of psus for access at the end
#TODO select neighbors
class BeamSearch:
    def __init__(self, warehouse, order):
        self.warehouse = warehouse
        self.order = order
        self.beam_width = 2

    #keep only the PSUs that contain at least one of the items in the order
    def prune(self):
        relevant_units = []
        for unit in self.warehouse:
            if any(item in unit for item in self.order):
                relevant_units.append(unit)
        return relevant_units


    def get_fitness(self):
        for item in self.prune():
            pass


    def beam_search(self):
       #k_current - select k random states
        start_state = random.sample(self.prune(), self.beam_width)
        print(start_state)
       #neighbors - select all neighbours of all current states
       #k_best neighbors - best k states from neighbors
       #if no neighbor improves current value
        #return k_current
       #k_current = k_best neighbors
        #until termination condition is met



    # ## get indices of relevant PSUs and remove "empty" PSUs from list
    # psu_index = [i for i, j in enumerate(relevant) if j]
    # relevant = list(filter(None, relevant))
    # print(len(relevant))
    # # get idices of PSUs with more than one item
    # def get_cool_PSU(rel):
    #     new = []
    #     for items in rel:
    #         if len(items) > 1:
    #             new.append(rel.index(items))
    #     return new
    #
    # cool_psu = get_cool_PSU(relevant)
    # print(len(cool_psu))
    #
    # beam_width = 2 #configurable by user
    # print("order:", order12)
    # print(NoOrder12)
    # # for i in cool_psu:
    # #     print(relevant[i])
    # print(relevant)

bs = BeamSearch(NoWarehouse, NoOrder12)
print("all psus with the items inside:", bs.warehouse)
print("order:", bs.order)
print("prune:", bs.prune(), len(bs.prune()))
bs.beam_search()