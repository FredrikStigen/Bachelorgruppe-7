

f = open("position.txt", "w")
f.write("270")
f.close()

f = open("position.txt", "r")
pos = int(f.read())
print(pos)
f.close()