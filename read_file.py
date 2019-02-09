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
NoWarehouse = replace_matched_PSU(warehouse, dictionary_stock)
#print(NoWarehouse)

# convert the items in the order to Numbers
def convert_item_in_order(word_list, dictionary):
    new_list = [dictionary.get(item) for item in word_list]
    return new_list
NoOrder11 = convert_item_in_order(order11,dictionary_stock)
NoOrder12 = convert_item_in_order(order12,dictionary_stock)

#---------this does not work!--------------

#simulated annealing
#INITIALIZE search state s, temperature t

def update_temperature(T):
    return T - 0.001

def get_covered_items(S, R):
    cov = []
    for i in range(len(S)):
        if S[i] == 1:
            cov.append(R[i])
    return cov

def get_fitness(S, R):
    covered = get_covered_items(S, R)
    covered = set([item for sublist in covered for item in sublist]) #flattens list of list and throws out duplicats
    y = sum(S) #number of PSUs used
    #print("sum:", y)
    fit = len(covered) - y #fit is the number of covered items minus the number of PSUs
    return fit

def get_neighbors(test):
    #print("checkstate", test)
    nhb = test.copy()
    x = random.choice(range(0, len(nhb) - 1))
    y = random.choice(range(0, len(nhb) - 1))
    m = random.choice(range(0, len(nhb) - 1))
    z = np.random.choice([0, 1], 1)

    nhb[x] = 1
    nhb[m] = 0
    if z == 0:
        nhb[y] = 1
    else:
        nhb[y] = 0
    nhb = nhb
    return nhb

def make_move(state, R, T):
    test = state
    nhb = get_neighbors(test)
    current = get_fitness(state, R)
    new = get_fitness(nhb, R)
    delta = new - current
    print("ngb: ", get_fitness(nhb, R))
    print("state: ", get_fitness(state, R))
    print("delta", delta)


    if delta > 0:
        return nhb
    else:
        print("time",T)
        p = math.exp(-delta / T)
        return nhb if random.random() > p else state

def simulated_annealing(R,O): #A= relevant, O = order
    L = len(R)
    goal = len(O)
    state_0 = np.random.choice([0, 1], size=(L, ), p=[1-len(O)/L, len(O)/L]) #rendom array 0=PSU not used 1=PSUused
    T = 5
    state = state_0.copy()
    state_best = state_0.copy()
    k = 0
    print("start")

    while T > 1e-3:
        state = make_move(state, R, T)
        if get_fitness(state, R) > get_fitness(state_best, R):
            state_best = state.copy() #in theory this should only take if the next state is better but somehow i just takes it always
        print("best", get_fitness(state_best, R))
        T = update_temperature(T)
        k += 1

    cov = get_covered_items(state_best, R)
    cov = len(set([item for sublist in cov for item in sublist]))
    used = sum(state_best)
    other = sum(state)
    print("iterations:", k, "PSUs used:",used,"covered:", cov, "Items in order:", goal, "state:", state_best, "other", other)
    return state, state_best, state_0

simulated_annealing(relevant,NoOrder12)





