# colliding_blocks.py
"""
Simulates and animates the motion of blocks in a room.  Assumes the blocks are
correctly initialized (not overlapped and all fit inside the bounding box).  
All units are metric: the length unit is meter, the mass unit is kilogram, and 
the time unit is second.


In order to see the animation, in the Spyder Python Console, type
    %matplotlib qt
to send the graphics to the qt graphical user interface.  You only need to do
this once in a session (unless you restart the kernel).
"""
# DO NOT MODIFY the given function docstrings.

import shapes
import numpy as np
import matplotlib.pyplot as plt


def draw_blocks(xs, ws, hs, cs, w, h, title):
    """
    Draws the blocks in a bounding box of width w and height h and shows them 
    for at least 0.01 seconds. 
    xs[i] is the x-coordinate of the left edge of the i'th block.
    ws[i], hs[i] are the width and height of the i'th block.
    cs[i] is the color of the i'th block (e.g. 'blue' or 'brown').
    xs, ws, hs, cs all have the same length.
    You may assume that all blocks fit inside the bounding box.

    Parameters:
        xs (1D numpy array): x positions of the left edge of the blocks, in
                             ascending order                              
        ws (1D numpy array): widths of the blocks
        hs (1D numpy array): heights of the blocks
        cs (list of strings): colors of the blocks
        w (float): room width
        h (float): room height
        title (str): diagram title
    """
    floor= 0               # y-coordinate of the floor
    plt.cla()              # Clears current axes (removes all drawn objects).
    plt.xlim(floor, w)     # Sets the x-axis to range from 0 to w.
    plt.ylim(floor, h)     # Sets the y-axis to range form 0 to h.
    ax = plt.gca()         # Get current axes
    ax.set_aspect('equal') # Set current axes to equal scaling
    plt.xticks([])         # Removes the tick marks from the x-axis.
    plt.yticks([])         # Removes the tick marks from the y-axis.
    
    #######################################################
    ### DO NOT modify the function code above this line ###
    
    # module shapes doesn't compute with arrays, it needs floats
    for i in range(len(xs)):
        shapes.draw_rect(xs[i], floor, ws[i], hs[i], cs[i])
    plt.title(title)
    
    #####################################################################
    ### DO NOT delete the function code below this line               ###
    ### OK to change the pause time (pause longer) during development ###
    
    plt.show()       # Shows the plot.
    plt.pause(0.01)  # Pauses 0.01 seconds in code execution; this is not the 
                     #   simulation time of the blocks model.


def next_timestep(xs, vxs, ws, hs, ms, w, h, dt, mu_k, e):
    """
    Returns the positions and velocities of the blocks at the next timestep,
    updated via the equations of motion, collisions between blocks and walls,
    and collisions between blocks.

    Parameters:
        xs (1D numpy array): x positions of the left edge of the blocks, in
                             ascending order                              
        vxs (1D numpy array): current x velocities of the blocks
        ws (1D numpy array): widths of the blocks
        hs (1D numpy array): heights of the blocks
        ms (1D numpy array): masses of the blocks
        w (float): room width
        h (float): room height
        dt (float): increment of time of simulate
        mu_k (float): Coefficient of kinetic friction
        e (float): Coefficient of restitution (Inelastic collision)
    Returns as a tuple:
        xs (1D numpy array): x positions of blocks after 1 timestep
        vxs (1D numpy array): x velocities of blocks after 1 timestep
        
    xs, vxs, ws, hs, ms all have the same length.
    """
    # account for kinetic friction first
    g = 9.81 # meters per second
    dvf = mu_k * g * dt
    for k in range(len(vxs)):
        v = vxs[k]
        # does friction stop the block?
        if abs(v) <= dvf:
            vxs[k] = 0.
        # is the block moving right?
        elif v > 0:
            vxs[k] = v - dvf
        # is the block moving left?
        else:
            vxs[k] = v + dvf
        
    # then update x position of every block
    x_new = xs + vxs * dt
    # switch direction of block when collide with wall
    # and account for inelastic collision
    for i in range(len(x_new)):
        # check left wall collision
        if x_new[i] <= 0.:
            # start x position at left wall
            x_new[i] = 0
            vxs[i] = e * vxs[i] * -1 # switch velocity direction
        # check right wall collision
        elif (x_new + ws)[i] >= w:
            # start x + ws position at right wall
            x_new[i] = w - ws[i]
            vxs[i] = e * vxs[i] * -1 # switch velocity direction
            
    # switch direction of block if collides with block
    for j in range(len(xs)-1):
        # check two adjacent elements at a time
        adj_xs = x_new[j:j+2]
        adj_vxs = vxs[j:j+2]
        adj_ws = ws[j:j+2]
        adj_ms = ms[j:j+2]
        # and send them into check_collision to return two variables
        updated_vxs, collided = check_collision(adj_xs, adj_vxs, adj_ws, adj_ms, e)
        if collided:
            vxs[j:j+2] = updated_vxs
    return x_new, vxs

def check_collision(xs, vxs, ws, ms, e):
    """
    Returns the velocities of two blocks and True/False to indicate whether a
    collision occurred. The velocities are updated if the blocks have collided;
    otherwise, the velocities are unchanged.

    Parameters:
        xs (1D numpy array of length 2): x positions of the left edge of two blocks
        vxs (1D numpy array of length 2): x velocities of the two blocks
        ws (1D numpy array of length 2): widths of the two blocks
        ms (1D numpy array of length 2): masses of the two blocks
        e (float): Coefficient of restitution (Inelastic collision)

    Returns as a tuple:
        vxs_new (1D numpy array of length 2): x velocities, possibly updated, of 
                                             the two blocks
        collision_occurred (bool): True if a collision occured; otherwise False
    """
    # Call index 0 and 1 in length 2 array
    m1, m2 = ms[0], ms[1]
    v1, v2 = vxs[0], vxs[1]
    x1, x2 = xs[0], xs[1]
    w1 = ws[0]
    
    # check if blocks collide, heading toward each other
    # and account for inelastic collision
    if (x1 + w1) >= x2 and v1 > v2:
        # calculate new velocity
        v1_new = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / (m1 + m2)
        v2_new = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / (m1 + m2)
        # apply new value to array index
        vxs[0] = v1_new
        vxs[1] = v2_new
        return vxs, True
    return vxs, False


def simulate_motion(xs, vxs, ws, hs, ms, cs, dt, w, h, T, mu_k, e):
    """
    Simulates and visualizes the motion of the blocks over a total time T.

    Parameters:
        xs (1D numpy array): initial x positions of the left edge of the blocks, 
                             in ascending order
        vxs (1D numpy array): initial x velocities of the blocks
        ws (1D numpy array): widths of the blocks
        hs (1D numpy array): heights of the blocks
        ms (1D numpy array): masses of the blocks
        cs (list of str): colors of the blocks
        dt (float): time step for each simulation update
        w (float): width of the room
        h (float): height of the room
        T (float): total simulation time
        mu_k (float): Coefficient of kinetic friction
        e (float): Coefficient of restitution (Inelastic collision)
    """
    # Set up figure window
    plt.close()
    plt.figure(1)
    plt.pause(2)
    plt.show()

    # Calculate the total number of simulation steps and display frames
    frames_per_second = 12
    num_steps = int(T // dt)  # Total number of simulated time-steps
    num_frames = min(
        num_steps, 
        int(T * frames_per_second)
    )  # Total displayed frames
    show_every = max(
        1, num_steps // num_frames
    )  # Display blocks every 'show_every' steps

    #######################################################
    ### DO NOT modify the function code above this line ###
    
    t = 0.0 # initalize time for title
    title = f'Time = {t:.1f} seconds'
    draw_blocks(xs, ws, hs, cs, w, h, title) # initialize blocks
    for i in range(num_steps):
        # save new x position
        xs, vxs = next_timestep(xs, vxs, ws, hs, ms, w, h, dt, mu_k, e)
        # draw blocks at every "show_every" step (8 steps)
        if (i + 1) % show_every == 0:
            # time increment = steps completed * change in time
            t = (i + 1) * dt
            title = f'Time = {t:.1f} seconds'
            draw_blocks(xs, ws, hs, cs, w, h, title)

    
    
#### Script code
if __name__ == '__main__':
    # Code in this if-block executes only if this file is run as a script.
    # Code in this if-block will not execute if this module is imported.
    
    plt.close('all')  # Close all currently opened figure windows
    ### Add code below to test your functions ###
    # For each simulation case, set the initial conditions such that
    #  - the position of the blocks are in ascending order in the x positions array
    #  - the blocks initially do not overlap
    #  - the blocks should fit inside the bounding box
    
    xs = np.array([1., 5., 8., 9.])
    ws = np.array([2., 2.5, 0.5, 3])
    hs = np.array([2., 4., 3., 1.])
    cs = ['brown', 'slateblue', 'green', 'magenta']
    vxs = np.array([2.0, -2.0, -1.0, 2.5])
    ms = np.array([1.5, 1.0, 0.5, 2.0])
    dt = 0.01
    w = 15.0
    h = 5.0
    T = 15.0

    #### Include Simulation in testing
    mu_k = 0.01 # Kinetic friction
    e = 0.8     # Elastic collisions
    simulate_motion(xs, vxs, ws, hs, ms, cs, dt, w, h, T, mu_k, e)