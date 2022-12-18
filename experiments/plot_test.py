import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# Set the figure and axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the vectors
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# Set the initial plot
ax.plot([0, v1[0]], [0, v1[1]], [0, v1[2]], 'r')
ax.plot([0, v2[0]], [0, v2[1]], [0, v2[2]], 'b')
ax.set_xlim([-1, 5])
ax.set_ylim([-1, 5])
ax.set_zlim([-1, 5])

# Set the angle of rotation
angle = 0

# Define a function to update the plot
def update(angle):
    # Create rotation matrix
    R = np.array([[np.cos(angle), -np.sin(angle), 0],
                  [np.sin(angle), np.cos(angle), 0],
                  [0, 0, 1]])

    # Rotate the vectors
    v1_rotated = R @ v1
    v2_rotated = R @ v2

    # Clear the current plot
    ax.clear()

    # Plot the rotated vectors
    ax.plot([0, v1_rotated[0]], [0, v1_rotated[1]], [0, v1_rotated[2]], 'r')
    ax.plot([0, v2_rotated[0]], [0, v2_rotated[1]], [0, v2_rotated[2]], 'b')
    ax.set_xlim([-1, 5])
    ax.set_ylim([-1, 5])
    ax.set_zlim([-1, 5])

    # Redraw the plot
    fig.canvas.draw()

# Use matplotlib's animation API to animate the plot
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 2*np.pi, 0.1), interval=10)
plt.show()