"""Progamming Task Methods of AI"""
##################################################
######important importing#########################
#import qt
##################################################
#GOAL: we want a psu carry as many items possible of our order

# find items in problem:
# first line all the items there are but without numbers in stock
# each line is one psu and whtas inside, seperated by comma


#1. read in the text file with the warehouse information
warehouse = []
for line in open("problem1.txt"):
        psu = line.strip().split(" ")
        warehouse.append(psu)
stock = warehouse[2] #the first line, what is in stock
warehouse = warehouse[1:] #now we have a list of the psus
#print(warehouse)
#print(stock)

#2. open the order11, store in list
for item in open("order11.txt"):
    order11 = item.split(" ")

#3. open the order12
for item in open("oder12.txt"):
    order12 = item.split(" ")

#print(order11)
#print(order12)



# print how many PSU were used
# print identifier of the PSU and items stored in the PSU
