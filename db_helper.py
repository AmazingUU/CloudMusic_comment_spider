import time

import pymysql


class DbHelper(object):
    def __init__(self):
        self.mutex = 0  # 锁信号
        self.db = None

    def connenct(self, configs):
        try:
            self.db = pymysql.connect(
                host=configs['host'],
                user=configs['user'],
                password=configs['password'],
                db=configs['db'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print('db connect success')
            return self.db
        except Exception as e:
            print('db connect fail,error:', str(e))
            return None

    def close(self):
        if self.db:
            self.db.close()
            print('db close')

    def save_one_data_to_day_hot_song(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into day_hot_song(ranking,song_id,name,singer,create_time) values(%s,%s,%s,%s,now())'
                cursor.execute(sql, (data['ranking'], data['song_id'], data['name'], data['singer']))
                self.db.commit()
                # self.mutex = 0  # 解锁
                print('{}\t{}\t{}\t{} insert into day_hot_song'.format(data['ranking'], data['song_id'], data['name'],
                                                                       data['singer']))
        except Exception as e:
            print('save_one_data_to_day_hot_song fail,error:' + str(e))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_hot_comment(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into hot_comment(song_id,username,content,like_count,comment_time,create_time) values(%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['song_id'], data['username'], data['content'], data['like_count'], data['comment_time']))
                self.db.commit()
                # self.mutex = 0  # 解锁
                print(
                    '{}\t{}\t{}\t{} insert into hot_comment'.format(data['song_id'], data['username'], data['content'],
                                                                    data['like_count'],
                                                                    data['comment_time']))
        except Exception as e:
            print('save_one_data_to_hot_comment,error:', str(e))
        finally:
            self.mutex = 0  # 解锁

    def save_one_data_to_comment(self, data):
        while self.mutex == 1:  # connetion正在被其他线程使用，需要等待
            time.sleep(1)
            print('db connect is using...')
        self.mutex = 1  # 锁定
        try:
            with self.db.cursor() as cursor:
                sql = 'insert into comment(song_id,username,content,like_count,comment_time,beReplied_content,beReplied_user,create_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
                cursor.execute(sql, (
                    data['song_id'], data['username'], data['content'], data['like_count'], data['comment_time'],
                    data['beReplied_content'], data['beReplied_user']))
                self.db.commit()
                # self.mutex = 0  # 解锁
                print('{}\t{}\t{}\t{}\t{}\t{}\t{} insert into comment'.format(data['song_id'], data['username'],
                                                                                  data['content'], data['like_count'],
                                                                                  data['comment_time'],
                                                                                  data['beReplied_content'],
                                                                                  data['beReplied_user']))
        except Exception as e:
            print('save_one_data_to_comment,error:', str(e))
        finally:
            self.mutex = 0  # 解锁

    # def find_all_detail(self):
    #     try:
    #         with self.db.cursor() as cursor:
    #             sql = 'select url,filename from detail limit 10'
    #             cursor.execute(sql)
    #             res = cursor.fetchall()
    #             return res
    #     except Exception as e:
    #         print('find_all_detail fail,error:', str(e))
    #         return None
