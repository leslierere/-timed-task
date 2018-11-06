from threading import Thread, Timer



def timedTask():  # the task you want to run for every specific period
    print('you will achieve it as long as you believe it')#where you put the codes what you really need to run
    t = Timer(10, timedTask)
    #after 10 seconds, timedTask will be started
    #timedTask will be run in a separate thread of control
    t.start()# start the seperate thread of control, and the thread will stop being "alive" when the method terminates



if __name__ == '__main__':
    timedTask()

#Notes
#this is applicable to pretty easy task
#"The interval the timer will wait before executing its action may not be exactly the same as the interval specified by the user."
#ref: https://docs.python.org/3/library/threading.html
