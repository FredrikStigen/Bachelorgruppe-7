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


plt.plot(fpos)
plt.show()
