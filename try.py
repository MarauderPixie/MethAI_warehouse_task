import tkinter as tk

#output = {"units" : (681,['mouse', 'keyboard']), (543, ['bli', 'bleeh'])}
dict = {'number_units': 7, 'units': [(162, ['magnificient-computer', 'magnificient-record-player', 'hip-laptop', 'awesome-laptop-battery']), (189, ['hip-keyboard', 'awesome-laptop', 'magnificient-phone-charger']), (223, ['infamous-record-player', 'super-tv', 'hip-computer', 'magic-dryer']), (374, ['magnificient-webcam', 'infamous-laptop-charger', 'glamorous-cd-player', 'superextraordinary-cd-player', 'trendy-record-player', 'famous-keyboard']), (494, ['magnificient-camera-battery', 'magic-tv', 'hip-dvd-player', 'awesome-dryer', 'trendy-oven', 'hip-tv']), (879, ['extraordinary-camera-battery', 'awesome-computer', 'super-camera', 'trendy-mouse']), (880, ['awesome-phone-battery', 'superfamous-laptop', 'awesome-cd-player', 'hip-dvd-player'])], 'iterations': 108, 'covered_items': 8, 'goal': 8}
print(type(dict["units"]))
print(len(dict['units']))
print(dict["units"])
#print(dict["units"][1])
for i in (dict["units"]):
    print("()".format())
#lines = dict["units"].Split(Environment.NewLine.ToCharArray(), StringSplitOptions.RemoveEmptyEntries)
#lines = text.Split(Einviroment.NewLine.ToCharArray())
#info = lines[0].Split(',').Zip(lines[1].Split(','), (key, value)# => new { key, value }).Where(x => !String.IsNullOrEmpty(x.value)).ToDictionary(x => x.key, x => x.value);
#
#print(lines)


#input = output["units"]
#print(type(output))

# class SampleApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         #self.entry = tk.Entry(self)
#         #self.button = tk.Button(self, text="Get", command=self.on_button)
#         #self.button.pack()
#         #self.entry.pack()
#         self.printing = tk.Label(self, text = "You used PSU %s" %input)
#         self.printing.pack()
# #self.endtop, text = "The PSUs you used are: %s they carried the following items" %ident_new
# #    def on_button(self):
# #        print(self.entry.get())
#
# app = SampleApp()
# app.mainloop()




#dict_items([('number_units', 7), ('units', [(162, ['magnificient-computer', 'magnificient-record-player', 'hip-laptop', 'awesome-laptop-battery']), (189, ['hip-keyboard', 'awesome-laptop', 'magnificient-phone-charger']), (223, ['infamous-record-player', 'super-tv', 'hip-computer', 'magic-dryer']), (374, ['magnificient-webcam', 'infamous-laptop-charger', 'glamorous-cd-player', 'superextraordinary-cd-player', 'trendy-record-player', 'famous-keyboard']), (494, ['magnificient-camera-battery', #'magic-tv', 'hip-dvd-player', 'awesome-dryer', 'trendy-oven', 'hip-tv']), (879, ['extraordinary-camera-battery', 'awesome-computer', 'super-camera', 'trendy-mouse']), (880, ['awesome-phone-battery', 'superfamous-laptop', 'awesome-cd-player', 'hip-dvd-player'])]), ('iterations', 108), ('covered_items', 8), ('goal', 8)])

#<class 'dict'>
