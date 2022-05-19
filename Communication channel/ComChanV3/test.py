import matplotlib.pyplot as plt

fpos = []
fb = []

with open('fposlog.txt', 'r') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        fpos.append(currentPlace)

with open('thetafblog.txt', 'r') as filehandle:
    for line in filehandle:
        currentPlace = line[:-1]
        fb.append(currentPlace)

for i in range(len(fpos)):
    fpos[i] = round(float(fpos[i]), 2)

for j in range(len(fb)):
    fb[j] = round(float(fb[j]), 2)
    if fb[j] > 200:
        fb[j] = 0
plt.plot(fb, 'g-', fpos, 'r-')
plt.xlabel('Points')
plt.ylabel('Degrees')
plt.legend(['Feedback', 'Theta'], loc ="lower right")
plt.show()
