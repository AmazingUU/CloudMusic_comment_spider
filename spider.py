import base64
import binascii
import datetime
import json
import time
from multiprocessing.dummy import Manager as ThreadManager
from multiprocessing.dummy import Pool as ThreadPool
from random import random

import requests
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from const import const
from db_helper import DbHelper


def AES_encrypt(text, key):  # AES加密
    iv = '0102030405060708'
    pad = 16 - (len(text) % 16)  # 明文补足为16的倍数，如果正好是16的倍数，再补16位
    text += pad * chr(pad)  # chr()返回对应数值的ascii码，如果少一位，补充一个数值1对应的ascii，如果少两位，补充两个数字2对应的ascii，以此类推
    encryptor = AES.new(key, AES.MODE_CBC, iv)  # key为密钥，iv为初始偏移量
    encrypt_text = encryptor.encrypt(text)  # 加密
    encrypt_text = base64.b64encode(encrypt_text)  # 二级制编码，用64个字符来表示任意二进制数据
    return encrypt_text


def create_random_str(num):  # 生成num位随机字符串
    char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    str = ''
    for i in range(num):
        index = int(random() * len(char_list))
        str += char_list[index]
    return str


def get_params(first_param, forth_param, random_str):  # 产生POST的第一个参数
    encText = AES_encrypt(first_param, forth_param).decode('utf-8')  # AES加密出来是byte类型，再次加密时需要先将其转为String
    params = AES_encrypt(encText, random_str)
    return params


def RSA_encrypt(n_str, e_str, random_str):  # RSA加密
    n = int(n_str, 16)  # RSA modulus,RSA算法中大素数相乘的结果，16进制
    e = int(e_str, 16)  # RSA算法中的e，和n一起组成公钥(n,e)，16进制
    cryptor = RSA.construct((n, e))  # 构造加密器
    # 网易云JS中的encryptedString()将16位随机字符串倒序了，所以要生成与JS一样的密文，这里也要倒序，而且下面加密时，要求为字节，所以编码为ascii码
    text = random_str[::-1].encode('ascii')
    encrypt_text = cryptor.encrypt(text, '')[0]  # 网易云JS中第二个参数为空，这里也为空。查看encrypt()源码发现会返回两个值，第一个是密文，第二个值总为空
    encrypt_text = binascii.b2a_hex(encrypt_text).decode('utf-8')  # encrypt_text为二进制，转为十六进制然后再解码成字符串才是最后要post的密文
    return encrypt_text


def get_encSecKey(random_str, second_params, third_params):  # 产生POST的第二个参数
    encSecKey = RSA_encrypt(third_params, second_params, random_str)
    return encSecKey


def get_html(url):
    r = requests.get(url, headers=const.HEADERS)
    response = json.loads(r.text)
    return response


def post(url, form_data):  # POST请求获取评论数据
    r = requests.post(url, data=form_data, headers=const.HEADERS)
    response = json.loads(r.text)
    return response


def get_hot_comment(response):  # 从返回的评论JSON中分析出热门评论的相关数据
    hot_comment_list = response['hotComments']
    for hot_comment in hot_comment_list:
        data = {}
        data['username'] = hot_comment['user']['nickname']
        data['content'] = hot_comment['content']
        data['like_count'] = hot_comment['likedCount']
        time = int(hot_comment['time'] / 1000)  # 返回的时间戳在python中后三位为毫秒数，可以舍弃
        dateArray = datetime.datetime.fromtimestamp(time)
        data['comment_time'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        yield data


def get_comment(response):  # 从返回的评论JSON中分析出最新评论的相关数据
    comment_list = response['comments']
    for comment in comment_list:
        data = {}
        data['username'] = comment['user']['nickname']
        data['content'] = comment['content']
        data['like_count'] = comment['likedCount']
        time = int(comment['time'] / 1000)
        dateArray = datetime.datetime.fromtimestamp(time)
        data['comment_time'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        try:
            data['beReplied_content'] = comment['beReplied'][0]['content']  # 最新评论中经常有回复别人评论的情况，所以记录下被回复的内容和用户名
            data['beReplied_user'] = comment['beReplied'][0]['user']['nickname']
        except:
            data['beReplied_content'] = '无'
            data['beReplied_user'] = '无'

        yield data


def get_day_hot_song(response):  # 获取云音乐飙升榜的歌曲相关信息
    song_list = response['result']['tracks']
    for i in range(len(song_list)):
        data = {}
        data['ranking'] = i + 1
        data['name'] = song_list[i]['name']
        data['song_id'] = song_list[i]['id']
        data['singer'] = song_list[i]['artists'][0]['name']
        yield data


# 不使用线程池pool，只使用线程thread实现多线程
# def put_into_queue(links,song_ids,form_data,queue):
#     for i in range(len(links)):
#         resp = post(links[i],form_data)
#         dict = {'song_id':song_ids[i],'resp':resp}
#         queue.put_nowait(dict)
#
# def get_from_queue(db,queue):
#     while True:
#         try:
#             dict = queue.get_nowait()
#             for data in get_hot_comment(dict['resp']):
#                 data['song_id'] = dict['song_id']
#                 db.save_one_data_to_hot_comment(data)
#             queue.task_done()
#         except:
#             print("queue is empty wait for a while")
#             time.sleep(1)


def put_into_pool(link, song_id, form_data, queue):  # 生产线程池
    resp = post(link, form_data)
    dict = {'song_id': song_id, 'resp': resp}  # 返回的数据中没有song_id，需要添加一下
    queue.put_nowait(dict)


def get_from_pool(db, queue):  # 消费线程池
    while True:
        try:
            dict = queue.get_nowait()
            for data in get_hot_comment(dict['resp']):
                data['song_id'] = dict['song_id']
                db.save_one_data_to_hot_comment(data)  # 存储热门评论
            for d in get_comment(dict['resp']):
                d['song_id'] = dict['song_id']
                db.save_one_data_to_comment(d)  # 存储最新评论
            queue.task_done()  # 标记该数据已从队列中取出
        except:
            print("queue is empty wait for a while")
            time.sleep(1)


if __name__ == '__main__':
    # start_time = time.time()
    db = DbHelper()
    db.connenct(const.DB_CONFIGS)

    put_thread_pool = ThreadPool(3)
    get_thread_pool = ThreadPool(3)
    queue = ThreadManager().Queue()  # 线程池之间通信需要用Manager().Queue()，线程间通信用Queue()

    comment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='  # 评论接口
    random_str = create_random_str(16)
    params = get_params(const.FIRST_PARAM, const.FORTH_PARAM, random_str)
    encSecKey = get_encSecKey(random_str, const.SECOND_PARAM, const.THIRD_PARAM)
    form_data = {'params': params,
                 'encSecKey': encSecKey}

    response = get_html(const.DAY_LIST_URL)
    links = []
    song_ids = []
    # 先将云音乐飙升榜中的一百首歌曲相关信息存入数据库
    for data in get_day_hot_song(response):
        db.save_one_data_to_day_hot_song(data)
        song_id = data['song_id']
        link = comment_url.format(song_id)
        links.append(link)
        song_ids.append(song_id)

    # 再处理对应歌曲的评论信息
    for i in range(len(links)):
        # 利用线程池的优点在于便于控制线程数量，生产线程池中最多有三个生产线程，提高了生产效率，又不会在线程间切换花费太多时间
        put_thread_pool.apply_async(put_into_pool, (links[i], song_ids[i], form_data, queue))

    time.sleep(1)  # 让生产者先生产1s，保证queue中有初始数据量

    for i in range(3):  # 三个消费线程
        get_thread_pool.apply_async(get_from_pool, (db, queue))

    # 不使用线程池pool，只使用线程thread实现多线程
    # 这种方式生产线程只有一个，如果要启多个生产线程，需要将输入数据分成几组，传给对应的线程处理，写起来比较麻烦
    # put_thread = Thread(target=put_into_queue,args=(links,song_ids,form_data,queue))
    # put_thread.setDaemon(True)
    # put_thread.start()
    #
    # time.sleep(2)
    #
    # for i in range(3):
    #     get_thread = Thread(target=get_from_queue,args=(db,queue))
    #     get_thread.setDaemon(True)
    #     get_thread.start()

    queue.join()  # 将程序阻塞，等待队列中所有数据都标记为task_done，且queue中无数据时再放通

    db.close()
    # end_time = time.time()
    # print('total time:',str(end_time - start_time))

# 下面都是一些本项目的参考资料
# 建表语句
# create table if not exists day_hot_song(id int primary key auto_increment,ranking int(4),song_id int(15),name varchar(50),singer varchar(20),create_time datetime);

# create table if not exists hot_comment(id int primary key auto_increment,song_id int(15),username varchar(30),content text,like_count int(7),comment_time varchar(30),create_time datetime);

# create table if not exists comment(id int primary key auto_increment,song_id int(15),username varchar(30),content text,like_count int(7),comment_time varchar(30),beReplied_content text,beReplied_user varchar(30),create_time datetime);

# 网易云JS中的关键代码
# var bZH3x=window.asrsea(JSON.stringify(i2x),
# 	bwx3x(["流泪","强"]),
# 	bwx3x(XD3x.md),
# 	bwx3x(["爱心","女孩","惊恐","大笑"]));
# e2x.data=k2x.cJ5O({params:bZH3x.encText,
# 	encSecKey:bZH3x.encSecKey})}cQx5C(Z3x,e2x)};v2x.bm3x.redefine=true})();
#
# window.asrsea=d
#
# function(){
# 	function a(a){ 生成a位随机数
# 		var d,e,b="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
# 		c="";
# 		for(d=0;a>d;d+=1)
# 			e=Math.random()*b.length,e=Math.floor(e),c+=b.charAt(e);
# 		return c}
# 	function b(a,b){ AES加密
# 		var c=CryptoJS.enc.Utf8.parse(b),
# 		d=CryptoJS.enc.Utf8.parse("0102030405060708"),
# 		e=CryptoJS.enc.Utf8.parse(a),
# 		f=CryptoJS.AES.encrypt(e,c,{iv:d,mode:CryptoJS.mode.CBC});
# 		return f.toString()}
# 	function c(a,b,c){ RSA加密
# 		var d,e;
# 		return setMaxDigits(131),d=new RSAKeyPair(b,"",c),e=encryptedString(d,a)}
# 	function d(d,e,f,g){ 主函数
# 		var h={},i=a(16);
# 		return h.encText=b(d,g),h.encText=b(h.encText,i),h.encSecKey=c(i,e,f),h}
# 	function e(a,b,d,e){
# 		var f={};
# 		return f.encText=c(a+e,b,d),f}
# 	window.asrsea=d,window.ecnonasr=e}();
#
#
#  d中的四个参数
# {rid: "R_SO_4_186315", offset: "0", total: "true", limit: "20", csrf_token: ""}
#
# 010001
#
# 00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
#
# 0CoJUm6Qyw8W8jud


# https://www.cnblogs.com/nienie/p/8511999.html

# https://www.jianshu.com/p/069e88181488

# https://juejin.im/post/5aa20d03518825558358d047

# https://www.cnblogs.com/yysbolg/p/9060070.html
