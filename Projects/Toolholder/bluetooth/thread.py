import threading
from time import ctime, sleep

def music(func):
    for i in range(2):
        print("listening %s.%s"%(music, ctime()))
        sleep(2)

def movie(func):
    for i in range(2):
        print("listening %s.%s"%(movie, ctime()))
        sleep(5)


threads = []
t1 = threading.Thread(target=music, args=("music",))
threads.append(t1)
t2 = threading.Thread(target=movie, args=("movie",))
threads.append(t2)

if __name__ == "__main__":
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print("all over")
