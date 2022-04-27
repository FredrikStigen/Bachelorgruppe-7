import numpy as np

def pos1( fcn(s,v,a,d,fs,clock):
    # Sampling time
    T = 1/fs;
    # Time usage on acceleration/deceleration
    t_a = v/a;
    t_d = v/d;
    # Distance used on acceleration/deceleration
    a_distance = (1/2) * a * t_a^2;
    d_distance = (1/2) * d * t_d^2;
    # Time usage in the constant velocity
    t_c = (s -(a_distance + d_distance))/v;
    # Total time
    t_tot = t_a + t_c + t_d;

    # Creating time vectors for each part of the motion
    t_ac = t_a+t_c;                             # time used on acceleration and constant velocity
    t1 = [0:T:t_a];                             # Acceleration
    t2 = [T*size(t1,2):T:t_ac];                 # Constant velocity
    t3 = [T*(size(t1,2)+size(t2,2)):T:t_tot];   # Deceleration
    t = [t1 t2 t3];                             # Total time vector

    # Creating position vectors for each part of the motion
    pos_a = 1/2 * a * t1.^2;                               # Acceleration
    pos_c = (v*(t2-t2(1))) + pos_a(size(pos_a,2)) + (v*T); # Constant velocity
    pos_d = (v*(t3-t3(1)))+(1/2 * -d * (t3-t3(1)).^2) + pos_c(size(pos_c,2)) + (v*T);            # Deceleration
    pos = [pos_a pos_c pos_d]; # Total position vector

    # Position output based on the clock
    x = 1+round(clock/T);

    if x >= size(pos,2):
        x = size(pos,2)

    pos1 = pos(x);

    if pos1 >= s:
        pos1 = s