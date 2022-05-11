from more_itertools import first
import numpy as np
import matplotlib.pyplot as plt
import sympy

# function to test:
# x^2 + 5

function = "5+5"

# first check
# check if all the equation has numbers, operators, and x nothimg more

operators = ["^", "*", "/", "+", "-"]


def equation_validation_check(equation):
    first_char = equation[0]
    last_char = equation[-1]
    if first_char in operators or last_char in operators:
        print("Invalid")


added_expressions = []

new_expression = 1
x = sympy.symbols("x")
index = 0

while True:
    if index == len(function):
        added_expressions.append(new_expression)
        break

    char = function[index]
    if char == "x":
        new_expression *= x
    # if having a power character
    elif char == "^":
        index += 1
        power = np.double(function[index])

        while(power > 1):
            if function[index-2] == "x":
                new_expression *= x
            elif function[index-2].isdigit():
                new_expression *= np.double(function[index-2])
            power -= 1
    elif char == "*":
        index += 1
        if(function[index] == "x"):
            new_expression *= x
        elif(function[index].isdigit()):
            new_expression *= np.double(function[index])

    elif char == "/":
        index += 1
        if(function[index] == "x"):
            new_expression /= x
        elif(function[index].isdigit()):
            new_expression /= np.double(function[index])

    elif char.isdigit():
        first_index = index
        while True:
            # print(index)
            index += 1
            if index == len(function):
                break
            next_char = function[index]
            if next_char.isdigit() or next_char == ".":
                continue
            else:
                break

        last_index = index
        index -= 1
        if first_index == last_index:
            new_expression *= np.double(function[first_index])
        else:
            new_expression *= np.double(function[first_index:last_index])

    elif char == "+":
        if index != 0:
            added_expressions.append(new_expression)
        new_expression = 1

    elif char == "-":
        if index != 0:
            added_expressions.append(new_expression)
        new_expression = -1

    index += 1


full_expression = 0
for expression in added_expressions:
    full_expression += expression

print(isinstance(full_expression, float))
print(added_expressions)

x_axis = []
y_axis = []

if not(isinstance(full_expression, float)):
    for i in range(1, 11):
        new_y = full_expression.subs(x, i)
        if new_y == sympy.zoo:
            break
        x_axis.append(i)
        y_axis.append(new_y)
else:
    x_axis = range(1, 11)
    y_axis = np.repeat(full_expression, len(range(1, 11)))
print(x_axis)
print(y_axis)

plt.plot(x_axis, y_axis)
plt.show()

strr = "hello"
print(strr[0:0])
