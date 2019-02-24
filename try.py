import tkinter as tk

output = {"units" : (681,['mouse', 'keyboard']), (543, ['bli', 'bleeh'])}
var lines = input.Split(
    Environment.NewLine.ToCharArray(),
    StringSplitOptions.RemoveEmptyEntries);

var INFO =
    lines[0].Split(',')
        .Zip(lines[1].Split(','), (key, value) => new { key, value })
        .Where(x => !String.IsNullOrEmpty(x.value))
        .ToDictionary(x => x.key, x => x.value);

print INFO

for value in output["units"]:

input = output["units"]
print(type(output))

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #self.entry = tk.Entry(self)
        #self.button = tk.Button(self, text="Get", command=self.on_button)
        #self.button.pack()
        #self.entry.pack()
        self.printing = tk.Label(self, text = "You used PSU %s" %input)
        self.printing.pack()
#self.endtop, text = "The PSUs you used are: %s they carried the following items" %ident_new
#    def on_button(self):
#        print(self.entry.get())

app = SampleApp()
app.mainloop()
