
import numpy as np
import matplotlib.pyplot as plt
import sympy

# function to test:
# x^2 + 5

function = "5*x^2 - x^3"

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
        new_expression *= np.double(char)
    elif char == "+":
        if index != 0:
            added_expressions.append(new_expression)
        new_expression = 1

    elif char == "-":
        if index != 0:
            added_expressions.append(new_expression)
        new_expression = -1

    index += 1


print(str(new_expression))
full_expression = 0
for expression in added_expressions:
    full_expression += expression

x_axis = []
y_axis = []
for i in range(1, 11):
    new_y = full_expression.subs(x, i)
    if new_y == sympy.zoo:
        break
    x_axis.append(i)
    y_axis.append(new_y)

print(full_expression)
print(added_expressions)
print(x_axis)
print(y_axis)

plt.plot(x_axis, y_axis)
plt.show()

print(np.linspace(1.2, 3, 20))
