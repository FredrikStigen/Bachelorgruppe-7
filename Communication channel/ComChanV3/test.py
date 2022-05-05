import threading

vel = 1
acc = 2
pos = 3

def test(vel, acc, pos):
    print(vel)
    print(acc)
    print(pos)

if __name__ == '__main__':
    t1 = threading.Thread(target=test(5, 6, 7))

    t1.start()

    print("Running")

    print("Done")