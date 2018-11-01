import base64
import binascii
import json
from random import random

import requests
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


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


def get_params(first_param, forth_param, random_str):
    # first_param = '{rid: "", offset: "0", total: "true", limit: "20", csrf_token: ""}'
    # forth_param = '0CoJUm6Qyw8W8jud'
    # random_str = 'AmazingUU1234567'
    encText = AES_encrypt(first_param, forth_param).decode('utf-8')
    params = AES_encrypt(encText, random_str)
    return params


def get_encSecKey(random_str, second_params, third_params):
    # random_str = 'AmazingUU1234567'
    # second_params = '010001'
    # third_params = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    n = int(third_params, 16)  # RSA modulus,RSA算法中大素数相乘的结果，16进制
    e = int(second_params, 16)  # RSA算法中的e，和n一起组成公钥(n,e)，16进制
    cryptor = RSA.construct((n, e))  # 构造加密器
    # 网易云JS中的encryptedString()将16为随机字符串倒序了，所以要生成与JS一样的密文，这里也要倒序，而且下面加密时，要求为字节，所以编码为ascii码
    text = random_str[::-1].encode('ascii')
    encrypt_text = cryptor.encrypt(text, '')[0]  # 网易云JS中第二个参数为空，这里也为空。查看encrypt()源码发现会返回两个值，第一个是密文，第二个值总为空
    encSecKey = binascii.b2a_hex(encrypt_text).decode('utf-8')  # encrypt_text为二进制，转为十六进制然后再解码成字符串才是最后要post的密文
    return encSecKey


def post(url,form_data):
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
   r = requests.post(url, data=form_data, headers=headers)
   return r.text

if __name__ == '__main__':
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_1311319058?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    # 下面四个参数对应JS中的四个输入参数
    first_param = '{rid: "", offset: "0", total: "true", limit: "20", csrf_token: ""}'  # 经试验rid这个字段无用
    second_params = '010001'
    third_params = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    forth_param = '0CoJUm6Qyw8W8jud'
    random_str = create_random_str(16)
    params = get_params(first_param, forth_param, random_str)
    encSecKey = get_encSecKey(random_str, second_params, third_params)
    form_data = {'params': params,
                 'encSecKey': encSecKey}
    r = requests.post(url, data=form_data, headers=headers)
    response = json.loads(r.text)
    hot_comment_list = response['hotComments']
    comment_list = response['comments']
    print(hot_comment_list)

# 下面是网易云JS中的关键代码
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
