import matplotlib.pyplot as plt
import numpy as np
import Motion_Profile_AtoB_Test

a = Motion_Profile_AtoB_Test.motionProfile(2*np.pi/3, 6, 11*np.pi/6)

print(len(a))

for i in range(len(a)):
    print(a[i])

