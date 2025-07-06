# import turtle
# from turtle import Turtle, getscreen
#
# timmy = Turtle()
# timmy.shape("turtle")
# timmy.color("blue1")
# timmy.forward(100)
#
# my_screen = getscreen()
#
# print(my_screen.canvheight)
# turtle.exitonclick()

from prettytable import PrettyTable

table = PrettyTable()

table.add_column(
    "Pokemon Name", ["Pikachu", "Squirtle", "Charmander"])
table.add_column("Type", ["Electric", "Water", "Fire"])

table.align = "l"

print(table)

