#crud.py основные функции для работы с базой данных


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def generate_lightning(ax, color, num_lines=10):
    for _ in range(num_lines):
        x_start = np.random.uniform(-1, 1)
        y_start = np.random.uniform(-1, 1)
        x_end = np.random.uniform(-1, 1)
        y_end = np.random.uniform(-1, 1)
        ax.plot([x_start, x_end], [y_start, y_end], color=color, lw=1.5, alpha=0.7)

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.axis('off')

# Create spheres
blue_circle = plt.Circle((-1, 0), 0.5, color='blue', alpha=0.7)
red_circle = plt.Circle((1, 0), 0.5, color='red', alpha=0.7)

ax.add_patch(blue_circle)
ax.add_patch(red_circle)

def update(frame):
    ax.patches = []  # Clear existing patches (circles)

    angle = frame * np.pi / 180
    blue_circle = plt.Circle((-1 * np.cos(angle), np.sin(angle)), 0.5, color='blue', alpha=0.7)
    red_circle = plt.Circle((1 * np.cos(angle), -np.sin(angle)), 0.5, color='red', alpha=0.7)

    ax.add_patch(blue_circle)
    ax.add_patch(red_circle)
    
    generate_lightning(ax, 'blue')
    generate_lightning(ax, 'red')

ani = animation.FuncAnimation(fig, update, frames=360, interval=50, repeat=True)

# Save animation
ani.save('animation.gif', writer='pillow')
