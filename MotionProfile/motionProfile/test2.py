import matplotlib.pyplot as plt
import numpy as np

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.1)

# red dashes, blue squares and green triangles
plt.plot(t**1.5, "go", t**2, "ro", t**3, "bo")
plt.show()