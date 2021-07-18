from threading import Timer

def clock(t):
    print(t)
    print(t.is_alive())

t = Timer(10, lambda: clock(t))

t.start()
t.is_alive() #








