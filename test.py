from ast import operator
import numpy as np
import matplotlib.pyplot as plt
import sympy

# function to test:
# x^2 + 5

function = "5/x"

# first check
# check if all the equation has numbers, operators, and x nothimg more

operators = ["^", "*", "/", "+", "-"]


def equation_validation_check(equation):
    first_char = equation[0]
    last_char = equation[-1]
    if first_char in operators or last_char in operators:
        print("Invalid")


added_expressions = []
subtracted_expressions = []
new_expression = 1
x = sympy.symbols("x")
index = 0

while True:
    if index == len(function):
        break
    char = function[index]
    if char == "x":
        new_expression *= x
    # if having a power character
    elif char == "^":
        index += 1
        power = int(function[index])
        while(power > 1):
            new_expression *= x
            power -= 1
    elif char == "*":
        index += 1
        if(function[index] == "x"):
            new_expression *= x
        elif(function[index].isdigit()):
            new_expression *= int(function[index])

    elif char == "/":
        index += 1
        if(function[index] == "x"):
            new_expression /= x
        elif(function[index].isdigit()):
            new_expression /= int(function[index])

    elif char.isdigit():
        new_expression *= int(char)
    index += 1


print(str(new_expression))
x_axis = []
y_axis = []
for i in range(1, 11):
    new_y = new_expression.subs(x, i)
    if new_y == sympy.zoo:
        print("asdnasnd")
        break
    x_axis.append(i)
    y_axis.append(new_y)

print(x_axis)
print(y_axis)

plt.plot(x_axis, y_axis)
plt.show()
