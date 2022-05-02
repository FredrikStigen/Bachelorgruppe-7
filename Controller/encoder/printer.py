#import rotary_encoder
import time

pos = 0

def printer():
    global pos
    print(pos)

def update(x):
    global pos
    pos = x

if __name__ == '__main__':
    while True:
        update(3)
        printer()
        time.sleep(1)