from tkinter import *

window = Tk()
window.title("Mile to Km Converter")
# window.minsize(400, 200)
window.config(pady=20, padx=20)


# Button
def button_clicked():
    my_sum = float(text_input.get()) * 1.609
    print(my_sum)
    text_km.config(text=my_sum)
    # my_label.config(text=input.get())


text = StringVar()
text.set("0")
text_input = Entry(width=10, textvariable=text)
text_input.grid(column=1, row=0)
text = StringVar()

miles_label = Label(text="Miles")
miles_label.grid(column=2, row=0)

is_equal_to_label = Label(text="is equal to")
is_equal_to_label.grid(column=0, row=1)

text_km = Label(text="0")
text_km.grid(column=1, row=1)

km_label = Label(text="Km")
km_label.grid(column=2, row=1)

button = Button(text="Calculate", command=button_clicked)
button.grid(column=1, row=2)

window.mainloop()
