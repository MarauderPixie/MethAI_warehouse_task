"""Progamming Task Methods of AI"""
##################################################
######        important importing        #########
# import qt
##################################################

# GOAL: 
# we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma


# 1. read in the text file with the warehouse information
warehouse = []
for line in open("problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[2]        # the first line, what is in stock
warehouse = warehouse[1:]   # now we have a list of the psus
# print(warehouse)
# print(stock)

# 2. open the order11, store in list
for item in open("order11.txt"):
    order11 = item.split(" ")

# 3. open the order12
for item in open("oder12.txt"):
    order12 = item.split(" ")

# print how many PSU were used
# print identifier of the PSU and items stored in the PSU
# print(order11)
# print(order12)

# Dictionary items to numbers
dictionary_stock = {}
i: int
for i in range(len(stock)):
    dictionary_stock[stock[i]] = i+1
print(dictionary_stock) 

# convert the items in the PSUs to Numbers. 
def replace_matched_PSU(word_list, dictionary):
    new_list = [[dictionary.get(item, item) for item in lst] for lst in word_list]
    return new_list
NoWarehouse = replace_matched_items(warehouse, dictionary_stock)
#print(NoWarehouse)

# convert the items in the order to Numbers
def convert_item_in_order(word_list, dictionary):
    new_list = [dictionary.get(item) for item in word_list]
    return new_list
NoOrder11 = convert_item_in_order(order11,dictionary_stock)
NoOrder12 = convert_item_in_order(order12,dictionary_stock)





