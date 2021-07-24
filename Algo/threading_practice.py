import threading
import time 


def sleeper(n,name):
    print('Hi,sleep for {}'.format(name))
    time.sleep(n)
    print('woke up after {}'.format(n))


player = threading.Thread(target=sleeper, name='tread1', args=(5, 'player'))
pause = threading.Thread(target=sleeper, name='tread2', args=(2, 'pause'))
contiue = threading.Thread(target=sleeper, name='tread3', args=(2.5, 'continu'))

player.start()
pause.start()
contiue.start()

print('hello')