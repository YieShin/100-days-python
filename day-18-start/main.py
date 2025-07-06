import random
from turtle import Turtle, Screen
from random import randint

tim = Turtle()
tim.shape("turtle")


#
# number_of_lines = 3
#
# while number_of_lines < 11:
#     tim.screen.colormode(255)
#     tim.pencolor(randint(0, 255), randint(0, 255), randint(0, 255))
#
#     for _ in range(number_of_lines):
#         tim.forward(100)
#         tim.right(360 / number_of_lines)
#
#     number_of_lines += 1
#

# direction = [0, 90, 180, 270]
#
#
def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    color = (r, g, b)
    return color

tim.speed("fastest")
tim.screen.colormode(255)

#
#
# for _ in range(200):
#     tim.pencolor(random_color())
#     angle = random.choice(direction)
#
#
#     tim.width(15)
#     tim.forward(30)
#     tim.setheading(angle)


def draw_spirograph(num_gap):
    for _ in range(int(360 / num_gap)):
        tim.pencolor(random_color())
        tim.left(num_gap)
        tim.circle(100)


draw_spirograph(8)

screen = Screen()
screen.exitonclick()
