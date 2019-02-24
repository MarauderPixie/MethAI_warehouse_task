import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.button.pack()
        self.entry.pack()

    def on_button(self):
        print(self.entry.get())

app = SampleApp()
app.mainloop()

#try the resetbutton
self.resetbutton = tk.Button(self.fifframe, text = 'Reset', command = self.refresh)
def refresh():
    self.variable.set("Select an Algorithm")
    self.number_button.set(0)
    self.warehouse_file.set("")
    self.order_file.set("")
