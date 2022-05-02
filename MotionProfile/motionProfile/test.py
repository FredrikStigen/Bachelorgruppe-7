import matplotlib.pyplot as plt
import numpy as np

fs = 1000
vel = 2 * np.pi / 3
acc = 6
pos = 2 * np.pi
pos_feedback = 0
clk = 0


def
tot_dist = pos - pos_feedback

T = 1 / fs
dacc = acc

t_acc = vel / acc
t_dacc = vel / dacc

acc_dist = (1 / 2) * acc * t_acc ** 2
dacc_dist = (1 / 2) * dacc * t_dacc ** 2

if acc_dist >= tot_dist / 2:
    acc_dist = tot_dist / 2
    vel = np.sqrt(2 * acc * acc_dist)
    t_acc = vel / acc
    t_tot = 2 * t_acc
    t1 = np.arange(0.0, t_acc, T)
    t3 = np.arange(T * len(t1), t_tot, T)
    pos_a = pos_feedback + (1 / 2 * acc * t1 ** 2)
    pos_d = (vel * (t3 - t3[0])) + (1 / 2 * -acc * (t3 - t3[0]) ** 2) + pos_a[(len(pos_a) - 1)] + (vel * T)
    fpos = np.hstack((pos_a, pos_d))

else:
    t_cons_vel = (tot_dist - (acc_dist + dacc_dist)) / vel
    t_tot = t_acc + t_cons_vel + t_dacc
    t_acc2 = t_acc + t_cons_vel

    # Start + size * step
    # t1 = 0 + np.arange(round(t_acc/T)) * T
    t1 = np.arange(0.0, t_acc, T)
    t2 = np.arange((T * len(t1)), t_acc2, T)
    t3 = np.arange(T * (len(t1) + len(t2)), t_tot, T)
    t = np.hstack((t1, t2, t3))
    # print(t1[1:-1])

    pos_a = pos_feedback + (1 / 2 * acc * t1 ** 2)
    pos_c = (vel * (t2 - t2[0])) + pos_a[(len(pos_a) - 1)] + (vel * T)
    pos_d = (vel * (t3 - t3[0])) + (1 / 2 * -acc * (t3 - t3[0]) ** 2) + pos_c[(len(pos_c) - 1)] + (vel * T)
    fpos = np.hstack((pos_a, pos_c, pos_d))

plt.plot(fpos, "o", markersize=1)
plt.grid()
plt.show()

