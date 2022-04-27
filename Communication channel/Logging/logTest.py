import time
import os.path
import datetime

fp = "C:/Users/47954/Documents/logs"

x = 1
y = 2
z = 3


print(datetime.datetime.now())

time = str(datetime.datetime.now())
time = time.replace(":", ".")

f = open(os.path.join(fp, "{}.txt".format(time)), "x")

f.write("[{}] Executed with parameters: {} {} {}".format(datetime.datetime.now(), x, y, z))
f.close()
