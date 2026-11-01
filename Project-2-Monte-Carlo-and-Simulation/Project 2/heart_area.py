"""
NetID: st2268

This program finds the difference in area between two 
hearts with size 3 and 1 using Monte-Carlo approximation
"""

import random
from random import uniform
import matplotlib.pyplot as plt

# area of shape / area of dartboard =~ no. darts in shape / no. darts thrown

# Parameters
n = 10000  # no. of darts to throw
s = 1      # radius of inner heart inscribed in square dart board

# Set up figure window
plt.figure()            # creates a new figure window
ax= plt.gca()           # gets current axes
ax.set_aspect('equal')  # unit lengths on x- and y-axis are equal (equal scaling)
plt.axis((-2.5, 2.5, -2.5, 2.5))  # x-axis limits -2.5 to 2.5; y-axis limits -2.5 to 2.5.
                                  # dart board is centered over the origin

# Simulate dart throwing
inner_hits= 0   # no. of darts in inner heart so far
outer_hits= 0   # no. of darts in outer heart so far
for k in range(n):
    # Throw kth dart
    x = uniform(-2.5, 2.5)
    y = uniform(-2.5, 2.5)
    # Is dart in the inner heart?
    if (x**2 + y**2 - 1)**3 <= (x**2)*(y**3):
        inner_hits = inner_hits + 1
        plt.plot(x, y, 'r*')
    # Is dart in the outer heart?
    elif (x**2 + y**2 - 3)**3 <= (x**2)*(y**3):
        outer_hits = outer_hits + 1
        plt.plot(x, y, 'm*')
    else:
        plt.plot(x, y, 'b*')

# area of outer heart
outer_heart = 25*outer_hits/n

# Outer heart approximation title
new_message = f'Outer heart (magenta part) has area {outer_heart} units squared'
plt.title(new_message)

plt.show()
