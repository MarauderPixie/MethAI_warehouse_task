"""
    This module provides a way of easily processing the order and warehouse files
    It reads in .txt files with the corresponding format, encodes the items and stores them in appropriate lists
    It also prunes the number of PSUs according to the order for faster processing
"""
class Warehouse:
    def __init__(self, filepath_warehouse, filepath_order):
        self.stock, units = self.fill_up_warehouse(filepath_warehouse)
        self.stock_count = self.get_stock_count(self.stock)
        self.encoded_warehouse = [self.encode_items(self.stock_count, unit) for unit in units]
        self.order = self.read_in_order(filepath_order)
        self.encoded_order = self.encode_items(self.stock_count, self.order)
        self.goal = len(self.order)
        self.indices_relevant_units, self.relevant_units = self.prune()

    '''
        Helper functions to read in files, store and encode the input
    '''

    # read in the order file
    def read_in_order(self, filepath_order):
        with open(filepath_order) as f:
            for line in f:
                order = line.strip().split(" ")
        return order

    # read in the file with items contained in warehouse
    def fill_up_warehouse(self, filepath_warehouse):
        with open(filepath_warehouse) as f:
            line = f.readline()
            stock = line.split(" ")
            # break while statement if it is not a comment line
            # i.e. does not startwith #
            units = []

            for line in f:
                if line.strip():
                    units.append(line.strip().split(" "))
        return stock, units

    # return a dictionary where each item is assigned a number
    def get_stock_count(self, stock):
        stock_count = dict([(val, idx) for idx, val in enumerate(stock,1)])
        return stock_count

    # encode the list of string items to their assigned numbers according to the stock count
    def encode_items(self, stock, items_list):
        encoded = [stock.get(item) for item in items_list]
        return encoded

    # decode the list of number items to natural language
    def decode_items(self, encoded_items_list):
        stock_count = dict([v, k] for k, v in self.stock_count.items())
        decoded = [stock_count.get(item) for item in encoded_items_list]

        return decoded

    '''
        Prune the list of PSUs and Keep only those that contain at least one of the items in the order, with only the
        relevant item in them
        Returns a list whose length corresponds to the sum of all units containing relevant items
    '''
    def prune(self):
        relevant_units = []
        for unit in self.encoded_warehouse:
            relevant_units.append([item for item in unit if item in self.encoded_order])
        psu_index = [i for i, j in enumerate(relevant_units) if j]
        relevant_units = list(filter(None, relevant_units))

        return psu_index,relevant_units

