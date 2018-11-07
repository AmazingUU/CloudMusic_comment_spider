# CloudMusic_comment_spider
网易云音乐评论爬虫

https://www.cnblogs.com/nienie/p/8511999.html
1、Fiddler的代理问题
利用Fiddler在线调试的时候，直接在Chrome中刷新，发现没有抓取到core.js。
图1
查找资料，发现虽然Fiddler安装好就能用，但是抓的HTTPS过程不全，还需要在Chrome中配置一下。
配置方法：https://blog.csdn.net/Lone1013/article/details/81222556
在SwitchyOmega插件中切换为Fiddler代理后，还需要注意的是，不能直接刷新界面，这样Fiddler还是抓不到，要点SwitchyOmega中设置的代理，通过这种方式刷新界面，Fiddler就能抓到core.js了。
图2
同样使用Fiddler的AutoResponder时，将浏览器JS替换为本地JS，也要用这种方式刷新界面，consloe中才会有日志输出

2、原文中对于第二个参数encSecKey固定为同一个值，虽然可以拿到返回的数据，但是不知道用固定值爬取的数据多了，会不会直接给我IP封掉，所以还是用Python实现了encSecKey值的获取方法，代码如下：
代码1
这里用的是RSA加密，需要注意的是网易云JS中将输入的16位随机字符串倒序了，所以这里在加密之前也要将其倒序，并且转为byte类型。
获取第一个参数params时用的是AES加密，网易云JS中采用了两次加密，第二次加密直接对第一次加密结果进行加密，但在Python中第一次加密之后的结果为byte类型，第二次加密之前需要将其转为String类型，否则会报TypeError: can't concat str to bytes

3、本项目爬取云音乐飙升榜，最开始是想从界面上爬取数据，但是发现榜单歌曲也是JS动态生成的。Google后发现网易云有提供现成的接口api，直接可以用，省去分析JS的过程了。
代码2

