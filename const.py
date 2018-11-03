class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

const = _const()

const.DB_CONFIGS = {'host': '127.0.0.1', 'user': 'root', 'password': 'admin', 'db': 'cloud_music'}
const.DAY_LIST_URL = 'http://music.163.com/api/playlist/detail?id=19723756'
const.HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# 下面四个参数对应JS中的四个输入参数
const.FIRST_PARAM = '{rid: "", offset: "0", total: "true", limit: "20", csrf_token: ""}'  # 经试验rid这个字段无用，本项目只爬取第一页即前20条评论，如果想爬取更多数据，可将limit改大，并且total需改为false
const.SECOND_PARAM = '010001'
const.THIRD_PARAM = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
const.FORTH_PARAM = '0CoJUm6Qyw8W8jud'
