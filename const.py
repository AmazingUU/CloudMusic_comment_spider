# 常量类
class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = _const()

# 数据库配置
const.DB_CONFIGS = {'host': '***', 'user': '***', 'password': '***', 'db': '***'}
# 排行榜api，本项目爬取云音乐飙升榜
# http://music.163.com/api/playlist/detail?id=2884035 # 网易原创歌曲榜
# http://music.163.com/api/playlist/detail?id=19723756 # 云音乐飙升榜
# http://music.163.com/api/playlist/detail?id=3778678 # 云音乐热歌榜
# http://music.163.com/api/playlist/detail?id=3779629 # 云音乐新歌榜
# 歌单api
# http://music.163.com/api/playlist/detail?id=123415635 # 云音乐歌单——【华语】中国风的韵律，中国人的印记
# http://music.163.com/api/playlist/detail?id=122732380 # 云音乐歌单——那不是爱，只是寂寞说的谎
const.DAY_LIST_URL = 'http://music.163.com/api/playlist/detail?id=19723756'
const.HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# 下面四个参数对应JS中的四个输入参数
const.FIRST_PARAM = '{rid: "", offset: "0", total: "true", limit: "20", csrf_token: ""}'  # 经试验rid这个字段无用，本项目只爬取第一页即前20条评论，如果想爬取更多数据，可将limit改大，并且total需改为false
const.SECOND_PARAM = '010001'
const.THIRD_PARAM = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
const.FORTH_PARAM = '0CoJUm6Qyw8W8jud'
