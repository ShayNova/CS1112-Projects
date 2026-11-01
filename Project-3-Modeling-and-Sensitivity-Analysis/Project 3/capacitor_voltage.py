"""
This code explores the sensitivity of the blinking
light model to changes in the parameters C, the
capacitance of the capacitor, and tC, the charging
time.
"""

import math
import matplotlib.pyplot as plt

def approx_voltage(v0, R, C, tC): 
    """
    Return the voltage of the capacitor over time
    
    Parameters
    v0: (float or int) voltage of the batter in volts
    R: (float or int) resistance of the resistor in ohms
    C: (float or int) capacitance of the capacitor in farads
    tC: (float or int) charging time of the capacitor in seconds
    
    Returns as a tuple
    t: a list of numbers of time values in seconds from 0 to tf
    v: a list of numbers of capacitor voltage in volts, corresponding
       to time values in t
    """
    C = C*(10**(-6))
    v_min = 0.01
    t = 0           # initialize t for while loop
    time = []
    volt = []
    
    # max voltage that can be reached
    v_max = v0 * (1 - math.exp((-tC)/(R*C)))
    
    # total charge and discharge time
    tf = tC - R * C * math.log(v_min/v_max)
    
    # complete cycle of charge and discharge of capacitor
    while t <= tf:
        if t <= tC:
            # capacitor is charging
            vt = v0 * (1 - math.exp((-t)/(R*C)))
        else:
            # capacitor is discharging
            vt = v_max * math.exp(-(t-tC)/(R*C))
        t = t + 0.001     # increment t to simulate increasing time
        time.append(t)    # append both lists to store as coordinates
        volt.append(vt)
    return (time, volt)

v0 = 10      # voltage of battery (volts)
R = 10*10**3 # resistance of the resistor (ohms)

# Graph with C changed, each line in plotted
plt.figure(1)
tC = 0.4
(t, v) = approx_voltage(v0, R, 5, tC)
legend_text = f'C = {5:.1f} uF'
plt.plot(t, v, 'r-', label=legend_text)

(t, v) = approx_voltage(v0, R, 7.5, tC)
legend_text = f'C = {7.5:.1f} uF'
plt.plot(t, v, 'b-', label=legend_text)

(t, v) = approx_voltage(v0, R, 10, tC)
legend_text = f'C = {10:.1f} uF'
plt.plot(t, v, 'm-', label=legend_text)

(t, v) = approx_voltage(v0, R, 12.5, tC)
legend_text = f'C = {12.5:.1f} uF'
plt.plot(t, v, 'g-', label=legend_text)

(t, v) = approx_voltage(v0, R, 15, tC)
legend_text = f'C = {15:.1f} uF'
plt.plot(t, v, 'k-', label=legend_text)
plt.legend()

# title and x and y labels
plt.title('Capacitor Voltage vs Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (volts)')
plt.grid()

plt.show(1)

# Graph with tC changed, each line is plotted
plt.figure(2) 
C = 10
(t, v) = approx_voltage(v0, R, C, 0.1)
legend_text = 'tC = 0.1 s'
plt.plot(t, v, 'm-', label=legend_text)

(t, v) = approx_voltage(v0, R, C, 0.2)
legend_text = 'tC = 0.2 s'
plt.plot(t, v, 'g-', label=legend_text)

(t, v) = approx_voltage(v0, R, C, 0.3)
legend_text = 'tC = 0.3 s'
plt.plot(t, v, 'b-', label=legend_text)

(t, v) = approx_voltage(v0, R, C, 0.4)
legend_text = 'tC = 0.4 s'
plt.plot(t, v, 'k-', label=legend_text)

(t, v) = approx_voltage(v0, R, C, 0.5)
legend_text = 'tC = 0.5 s'
plt.plot(t, v, 'r-', label=legend_text)
plt.legend()

# title and x and y labels
plt.title('Capacitor Voltage vs Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (volts)')
plt.grid()

plt.show(2)

