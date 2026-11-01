"""
NetID: st2268

This program calculates how many seconds it takes the
capacitor to reach a user-specified voltage given a 
user-specified charging time for max voltage
"""

import math

v_0 = 10         # voltage of the battery (volts)
R = 10*10**3     # resistance of the resistor (ohms)
v_min = 0.01     # lowest voltage of the battery (volts)
C = 10*10**(-6)  # capacitance of the capacitor (farads)
t = 0            # time variable (s)

# user-specified voltage and charging time
target_v = float(input('Enter a target voltage (v): '))
t_c = float(input('Enter the charging time (s): '))

# re-prompt user if input values are <=0
while target_v <= 0 or t_c <= 0:
    target_v = float(input('Enter a postive target voltage (v): '))
    t_c = float(input('Enter a postive charging time (s): '))

# after charging, the capacitor voltage reaches maximum (v_max) given by:
v_max = v_0 * (1 - math.exp((-t_c)/(R*C))) 
# compute v_max to compare against targe t_v

v_t = 0
if target_v > v_max:
    print('The capacitor cannot reach that voltage')
else:
    while v_t < target_v:
        # voltage (v) as a function of time (t) of capacitor while charging
        t = t + 0.001
        v_t = v_0 * (1 - math.exp((-t)/(R*C)))
# after the target voltage is reached
print(f'With a max charging time of {t_c} seconds, it takes about {t:.3f} seconds to reach {target_v} volts')