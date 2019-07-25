import sys
import time

def pros(now, all):
    n = now/all*100//2
    sys.stdout.write('\r')
    sys.stdout.write('|')
    for i in range(1, 51):
        if i <= n:
            sys.stdout.write('█')
        else:
            sys.stdout.write(' ')
    sys.stdout.write('|已完成{0:3.0f}% {1}/{2}'.format(n*2, now, all))
    sys.stdout.flush()

if __name__ == '__main__':
    for i in range(50):
        time.sleep(0.1)
        pros(i, 50)