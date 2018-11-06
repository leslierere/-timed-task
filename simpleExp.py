from threading import Thread, Timer



def timedTask():  # the task you want to run for every specific period
    print('you will achieve it as long as you believe it')
   

if __name__ == '__main__':
    while True:
    t = Thread(target= timedTask())#timedTask will be run in a separate thread of control
    t.start()# start the seperate thread of control, and the thread will stop being "alive" when the method terminates
    var = (random.random()*10)
    print(t.is_alive())# return bool, to know whether this thread is down
    print("接下来睡",var, "秒")
    time.sleep(var)


#ref: https://docs.python.org/3/library/threading.html
