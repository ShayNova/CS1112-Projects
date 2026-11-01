"""
NetID: st2268

This program determines the duration that the light
stays on (during the period 0.01<=t<=0.5) as a function
of the charging time t_c
"""
import math
import matplotlib.pyplot as plt

v_0 = 10         # voltage of the battery (volts)
R = 10*10**3     # resistance of the resistor (ohms)
v_min = 0.01     # lowest voltage of the battery (volts)
C = 10*10**(-6)  # capacitance of the capacitor (farads)
t_c = 0.01       # initialize charging time (s)

# user-specified target voltage
target_v = float(input('Enter a target voltage: '))

# re-prompting user if v <= 0
while target_v <= 0:
    target_v = float(input('The value must be positive, enter a new target voltage: '))

# the function for v_t when charging and discharging as a loop
while t_c <= 0.5:
    t = 0
    on_dur = 0
    k = True
    # calculate max voltage for charging limit
    # after charging, the capacitor voltage reaches maximum (v_max) given by:
    v_max = v_0 * (1 - math.exp((-t_c)/(R*C)))

    # calculate total time of charge and discharge
    # after charging, the capacitor discharges until minimum voltagte given by:
    t_f = t_c - R * C * math.log(v_min/v_max)
    # loop will simulate full cycle
    while t <= t_f and k == True:
        if t <= t_c:
            # capacitor is charging
            # voltage (v) as a function of time (t) of capacitor while charging
            v_t = v_0 * (1 - math.exp((-t)/(R*C)))
        else:
            # capacitor is discharging
            # after charging, the capacitor immediately discharges, given by:
            v_t = v_max * math.exp(-(t-t_c)/(R*C))
            if v_t < target_v:
                k = False
        if v_t > target_v:
            on_dur = on_dur + 0.001
        t = t + 0.001
    # denote coordinates for time and duration
    x = t_c
    y = on_dur
    plt.plot(x, y, 'm*')
    t_c = t_c + 0.01
        
# title and x and y labels
plt.title(f'Duration above {target_v:.2f} volts')
plt.xlabel('Charging Time (seconds)')
plt.ylabel('Duration (seconds)')
plt.show()

"""
The second algorithm is more efficient because we don't
need to simulate the full discharge duration, it stops 
the loop once the voltage is below the target
"""