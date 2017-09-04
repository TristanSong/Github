import urllib
from threading import Thread, Lock
from queue import Queue
import time

class Fetcher:
    def __init__(self, threads):
        self.lock = Lock() # 线程锁
        self.q_req = Queue() # 任务队列
        self.q_ans = Queue() # 完成队列
        self.threads = threads # 线程数
        for i in range(threads):
            t = Thread(target = self.threadget) # 线程任务
            t.setDaemon(True) # 设置子线程是否随主线程一起结束，在start前设置，默认为false
            t.start() # 启动线程
        self.running = 0 # 设置运行中的线程个数

    def __del__(self): # 解构时等两个队列完成
        time.sleep(0.5)
        self.q_req.join()  # queue队列为空后再执行其他操作
        self.q_ans.join()

    # 返回仍在运行的线程个数，为0表示全部完毕
    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running

    def push(self, req):
        return self.q_req.put(i)

    def pop(self):
        return self.q_ans.get()

    def threadget(self):
        while True:
            req = self.q_req.get()
            # threading.Lock(), 使用with可以不用显式调用acquire, release
            with self.lock:
                self.running += 1
            try:
                ans = i**2
                if ans<20:
                    ans = -1
            except Exception as e:
                ans = 'fail'
                print(e)
            self.q_ans.put((i, ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1)

if __name__ == '__main__':
    links = list(range(23))
    f = Fetcher(threads=5)
    file = open('myThread.txt', 'a+')
    i = 0
    while len(links) > 0:
        # 用于处理返回值不合格的情况
        # 如爬虫时HTTPError等， 可将其存入失败列表用于继续爬取
        failLinks = []
        for i in links:
            f.push(i)
            while f.taskleft():
                j, content = f.pop()
                if content == -1:
                    failLinks.append(j)
                else:
                    file.write(str(content) + '\n')
        links = failLinks
        # 仅仅为了避免死循环，实际爬虫时不需要
        links.pop()
    file.close()
