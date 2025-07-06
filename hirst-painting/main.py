# import colorgram
#
# colors = colorgram.extract("image.jpg", 30)
# rgb_colors = []
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     rgb_color = (r, g, b)
#     rgb_colors.append(rgb_color)
#
# print(rgb_colors)
from turtle import Turtle, Screen
import random
tim = Turtle()
tim.getscreen()

color_list = [(1, 9, 30), (121, 95, 41), (72, 32, 21), (238, 212, 72), (220, 81, 59), (226, 117, 100), (93, 1, 21), (178, 140, 170), (151, 92, 115), (35, 90, 26), (6, 154, 73), (205, 63, 91), (168, 129, 78), (3, 78, 28), (1, 64, 147), (221, 179, 218), (4, 220, 218), (80, 135, 179), (130, 157, 177), (81, 110, 135), (120, 187, 164), (11, 213, 220), (118, 18, 36), (243, 205, 7), (132, 223, 209), (229, 173, 165)]

tim.screen.colormode(255)

tim.up()
tim.hideturtle()
tim.speed("fastest")
tim.setheading(250)
tim.forward(250)
tim.setheading(0)

# # SHIN's ANSWER
# for _ in range(10):
#     for _ in range(10):
#         tim.dot(20, random.choice(color_list))
#         tim.forward(50)
#
#     tim.up()
#     tim.left(90)
#     tim.forward(50)
#     tim.left(90)
#     tim.forward(500)
#     tim.left(180)

# ANGELA's ANSWER
number_of_dots = 100
for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)


Screen().exitonclick()
