# Methods of AI 18/19 Final Project

A graphical user interface to apply several local search algorithms on a warehouse file containing PSUs and their content to find the least possible number of PSUs to fulfill an order, also given via text file by the user.

The user can choose different warehouse and order files, provided they're having the same structure, and between algorithms, as well as reset the application. 

When executing a search, the user will be given results in the form of a popup window containing the number of PSUs used, if all oredered items could be found, the ID of the required PSUs and their content.

## Overall structure of the code

The user is only required to execute `main.py` in order to start the program.

### `warehouse.py`

This script defines a `Warehouse` class, which is used to read warehouse and order files, translates items to numbers and defines the neighborhood used by the algorithms.

### `warehouse_gui.py`

The code defining the UI, calling the methods defined in `algorithms/`.

### `algorithms/`

This folder contains the available search algorithms - one script defining a method for every algorithm respectively.

## Used Modules

This project was written with *Python 3.7* and uses the following modules (version numbers given if available):

- `copy`
- `numpy`, 1.14.3
- `math`
- `os`
- `random`
- `tkinter`