import time
import matplotlib.pyplot as plt

import numpy as np

def generate(vel, acc, pos, fs, clk):
    T = 1/fs

    t_acc = vel/acc
    t_dacc = vel/acc

    acc_dist = (1/2) * acc * t_acc**2
    dacc_dist = (1/2) * acc * t_dacc**2

    t_cons_vel = (pos - (acc_dist + dacc_dist)) / vel

    t_tot = t_acc + t_cons_vel + t_dacc


    t_acc2 = t_acc + t_cons_vel

    # Start + size * step
    #t1 = 0 + np.arange(round(t_acc/T)) * T
    t1 = np.arange(0.0, t_acc, T)
    t2 = np.arange((T*len(t1)), t_acc2, T)
    t3 = np.arange(T*(len(t1) + len(t2)), t_tot, T)
    t = np.hstack((t1, t2, t3))
    #print(t1[1:-1])

    pos_a = 1/2 * acc * t1**2
    pos_c = (vel * (t2 - t2[1])) + pos_a[(len(pos_a)-1)] + (vel * T)
    pos_d = (vel * (t3 - t3[1])) + (1/2 * -acc * (t3 - t3[1])**2) + pos_c[(len(pos_c)-1)] + (vel * T)
    fpos = np.hstack((pos_a, pos_c[0:-1], pos_d))

    #print(pos_a)
    #print(pos_c)
    #print(pos_d)
    #print(fpos)

    print(t1[0], "-", t1[len(t1) - 1])
    print(t2[0], "-", t2[len(t2) - 1])
    print(t3[0], "-", t3[len(t3) - 1])
    print(pos_a[0], "-", pos_a[len(pos_a)-1])
    print(pos_c[0], "-", pos_c[len(pos_c)-1])
    print(pos_d[0], ":", pos_d[len(pos_d)-1])
    print(fpos)


    x = 1+round(clk/T)

    if x >= len(fpos):
        x = len(fpos)

    pos1 = fpos[x-1]

    if pos1 >= pos:
        pos1 = pos

    timer = np.arange(0, len(t2), 1)
    plt.plot(fpos, "o", markersize=1)
    plt.grid()
    plt.show()



generate((2/3)*np.pi, 6, np.pi, 100, time.time())