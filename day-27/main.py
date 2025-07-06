from tkinter import *


# Button
def button_clicked():
    print(input.get())
    my_label.config(text=input.get())


window = Tk()
window.title("My First GUI Program")
window.minsize(500, 300)
window.config(padx=20, pady=20)

# Label
my_label = Label(text="I am a Label", font=("Arial", 24, "bold"))
my_label.grid(column=0, row=0)

my_label.config(text="New text")

button = Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)

button = Button(text="New Click Me", command=button_clicked)
button.grid(column=2, row=0)

# Entry

input = Entry()
input.grid(column=3, row=2)

window.mainloop()
