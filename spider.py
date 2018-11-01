import base64
import requests
from Crypto.Cipher import AES


def AES_encrypt(text, key):
    iv = '0102030405060708'
    pad = 16 - (len(text) % 16)  # 明文补足为16的倍数，如果正好是16的倍数，再补16位
    text = text + pad * chr(pad)  # 补的
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_params():
    first_param = '{rid: "", offset: "0", total: "true", limit: "20", csrf_token: ""}'
    forth_param = '0CoJUm6Qyw8W8jud'
    random_num = 'AmazingUU1234567'
    encText = AES_encrypt(first_param, forth_param).decode('utf-8')
    params = AES_encrypt(encText, random_num)
    return params


def get_encSecKey():
    encSecKey = '92f3e490cdfde651f5c5bbf0a51d94b2e96d38ce8fb5be4b675ecd20da6410d8373423ea21ee01cf1499f4414f829b410ccc238fbd67d752f80b8139d001953cc6351da7c8c8c38e6dfa9217e50a94e25c4c843de10377e750413b8ea723368929a1894b96f5671e1ff8398f7a87c14a937f0f72936d1ace4584c1e1dcb2d7ab'
    return encSecKey


if __name__ == '__main__':
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_1311319058?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    params = get_params()
    encSecKey = get_encSecKey()
    # params = 'EKzL5Y0z+46IZKBi6v/LhgB1i9wEIRNC/m2yM5KU+ClCQU4b2BSJWhWOh55093sBOkmgca5PxzleUEvzU4suO78uIvwNC2UydWEKvdaMAIGQ5PHqf4mVG+q7RoB0jo+eWdgitnfiyxnkqfqy7WD1olxkYk6DLWGCJeC10RmMZcsQSECLTD32GoskX7Qno+yx'
    # encSecKey = '92f3e490cdfde651f5c5bbf0a51d94b2e96d38ce8fb5be4b675ecd20da6410d8373423ea21ee01cf1499f4414f829b410ccc238fbd67d752f80b8139d001953cc6351da7c8c8c38e6dfa9217e50a94e25c4c843de10377e750413b8ea723368929a1894b96f5671e1ff8398f7a87c14a937f0f72936d1ace4584c1e1dcb2d7ab'
    form_data = {'params': params,
                 'encSecKey': encSecKey}
    r = requests.post(url, data=form_data, headers=headers)
    print(r.text)

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
# 	function a(a){
# 		var d,e,b="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
# 		c="";
# 		for(d=0;a>d;d+=1)
# 			e=Math.random()*b.length,e=Math.floor(e),c+=b.charAt(e);
# 		return c}
# 	function b(a,b){
# 		var c=CryptoJS.enc.Utf8.parse(b),
# 		d=CryptoJS.enc.Utf8.parse("0102030405060708"),
# 		e=CryptoJS.enc.Utf8.parse(a),
# 		f=CryptoJS.AES.encrypt(e,c,{iv:d,mode:CryptoJS.mode.CBC});
# 		return f.toString()}
# 	function c(a,b,c){
# 		var d,e;
# 		return setMaxDigits(131),d=new RSAKeyPair(b,"",c),e=encryptedString(d,a)}
# 	function d(d,e,f,g){
# 		var h={},i=a(16);
# 		return h.encText=b(d,g),h.encText=b(h.encText,i),h.encSecKey=c(i,e,f),h}
# 	function e(a,b,d,e){
# 		var f={};
# 		return f.encText=c(a+e,b,d),f}
# 	window.asrsea=d,window.ecnonasr=e}();
#
#
#
# {rid: "R_SO_4_186315", offset: "0", total: "true", limit: "20", csrf_token: ""}
#
# 010001
#
# 00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
#
# 0CoJUm6Qyw8W8jud


# https://juejin.im/post/5aa20d03518825558358d047

# https://www.cnblogs.com/nienie/p/8511999.html
