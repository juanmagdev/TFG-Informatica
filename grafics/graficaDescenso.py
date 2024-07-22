import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the function
def f(x, y):
    return np.maximum(0, 200*x - 2) + np.maximum(0, 100*y - 3)

# Create a meshgrid for x, y
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('f(X, Y)')
ax.set_title('Surface Plot of f(x, y) = max(0, x-0.5) + max(0, y-0.5)')

plt.show()

# guarda figura
plt.savefig('superficie.pdf', bbox_inches='tight')