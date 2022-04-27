import os.path
import time as tm
from os.path import exists
import datetime

def createFile(fp, fn):
    f = open(os.path.join(fp, fn), "x")


def x(data, filepath, filename):


    if exists(filepath+filename):
        f = open(filepath+filename, "a")
        f.write("{}\n".format(data))
        f.close()
    else:
        createFile(filepath, filename)
        x(data, filepath, filename)


'''time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
time = time.replace(":", ".")
filename = str(("{}.txt".format(time)))
filepath = "C:/Users/Stigen/Documents/GitHub/Python/Bachelor 2022/CommunicationChannelV2/logs/"
for i in range(10):
    x(i, filepath, filename)
    tm.sleep(2)'''

