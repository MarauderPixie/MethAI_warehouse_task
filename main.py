from warehouse_gui import GUI
from tkinter import Tk


def main():
    # root = Tk()
    # my_gui = GUI(root)
    # my_gui.mainloop()
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
if __name__ == "__main__":
    main()