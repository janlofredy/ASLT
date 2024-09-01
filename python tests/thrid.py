import threading
import time

def threaded_worker():
    for r in range(10):
        print('Other: ', r)
        time.sleep(2)
    return 1

sudlanan = 0
thread_ = threading.Timer(1, threaded_worker, sudlanan)
thread_.daemon = True  # If the main thread kills, this thread will be killed too. 
thread_.start()

flag = True

for i in range(10):
    print('Main: ', i)
    time.sleep(2)
    if flag and i > 4:
        print(
            '''
            Threaded_worker() joined to the main thread. 
            Now we have a sequential behavior instead of concurrency.
            ''')
        thread_.join()
        flag = False
print(sudlanan)