from threading import Thread, Timer



def timedTask():  # the task you want to run for every specific period
    print('you will achieve it as long as you believe it')
    t = Timer(10, timedTask)
    #after 10 seconds, timedTask will be started
    #timedTask will be run in a separate thread of control
    t.start()# start the seperate thread of control, and the thread will stop being "alive" when the method terminates



if __name__ == '__main__':
    timedTask()
