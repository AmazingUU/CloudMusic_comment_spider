import time
from multiprocessing import Pool as ThreadPool
from multiprocessing import Manager as ThreadManager


def fun(msg,queue):
    print('msg: ', msg)
    # time.sleep(3)
    print('********')
    queue.put_nowait('fun_return %s' % msg)
    # return 'fun_return %s' % msg

def fun1(queue):
    while True:
        try:
            print(queue.get_nowait())  # 线程函数返回值
            queue.task_done()
        except Exception as e:
            # print('Exception:',e)
            print('queue is empty')
            # fun1(queue)

if __name__ == '__main__':
    # apply_async
    print('\n------apply_async-------')
    async_pool = ThreadPool(processes=4)
    async_pool1 = ThreadPool(processes=4)
    results =[]
    # res = []
    queue = ThreadManager().Queue()
    for i in range(5):
        msg = 'msg: %d' % i
        result = async_pool.apply_async(fun, (msg,queue))
        results.append(result)
        # r = async_pool1.apply_async(fun1,(queue,))
        # res.append(r)
    print('apply_async: 不堵塞')

    time.sleep(1)
    async_pool1.apply_async(fun1,(queue,))

    # for i in results:
    #     i.wait()

    queue.join()

    # for i in range(5):
    #     results[i].wait()  # 等待线程函数执行完毕
    #     res[i].wait()

    # for i in results:
    #     if i.ready():  # 线程函数是否已经启动了
    #         if i.successful():  # 线程函数是否执行成功
    #             print(i.get())  # 线程函数返回值
