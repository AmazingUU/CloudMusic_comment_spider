import time
from multiprocessing import Pool as ThreadPool
def fun(msg):
    print('msg: ', msg)
    time.sleep(1)
    print('********')
    return 'fun_return %s' % msg

if __name__ == '__main__':
    # apply_async
    print('\n------apply_async-------')
    async_pool = ThreadPool(processes=4)
    results =[]
    for i in range(5):
        msg = 'msg: %d' % i
        result = async_pool.apply_async(fun, (msg, ))
        results.append(result)
    print('apply_async: 不堵塞')
    # async_pool.close()
    # async_pool.join()
    for i in results:
        if i.ready():  # 线程函数是否已经启动了
            if i.successful():  # 线程函数是否执行成功
                print(i.get())  # 线程函数返回值
    for i in results:
        i.wait()  # 等待线程函数执行完毕
