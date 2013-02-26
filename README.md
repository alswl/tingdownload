## About ##

度娘终于干了一件好事，[Baidu Ting](http://ting.baidu.com)上线了，
正版音乐免费下载，类似于[谷歌音乐](http://www.google.cn/music)。
关于音乐版权和免费的问题， 有很多问题需要取讨论，
比如说这种商业模式是否对传统唱片业产生冲击又或是有积极影响？
作为普通消费者，暂时不用考虑这些问题，先享受这些服务好了。

Baidu Ting的音乐质量是128KBps，音质算好，里面的idv3信息也勉强可以，有:

* 歌名
* 歌手
* 部分专辑名（偶尔也出现“201-8月新歌快递”这种比较山寨的字）
* 部分唱片封面图片

虽然比不上谷歌音乐连歌曲风格都准备好了，但是比杂乱无章的那些音乐mp3要好太多了。

## Download ##

早上下了几首音乐，就顺手写了一个脚本，用来批量从Badu Ting下载音乐。

代码在[github-tingdownload](https://github.com/alswl/tingdownload)

## Requirement ##

* Python 2 (仅在Python2.7下测试)
* BeautifulSoup(已包含在目录下)
* simplejson（已删除，我还是用原装json吧，省掉一个包）
* 一点点Python基础
* Linux/Windows（我在Linux没问题，Windows应该也可以）

## Usage ##

在Shell(命令行)里输入下面随便一个命令，就会在当前目录下面出现 `musics` 文件夹，
里面就有下载好的音乐。

使用说明

    usage: tingdownload.py [-h] [-a] [--input INPUT] [Keyword [Keyword ...]]
    
    A script to download music from ting.baidu.com.
    
    positional arguments:
      Keyword
    
    optional arguments:
      -h, --help            show this help message and exit
      -a, --auto_match      auto match first song
      --input INPUT, -i INPUT
                            a list file to input musics

示例：

    python tingdownload.py 老男孩 #单个文件下载
    ./tingdownload.py 老男孩 #单个文件下载（给python文件加上可执行权限）
    python tingdownload.py 老男孩 Raise\n Me\n Up # 多文件名，如果有空格，请记得加上空格反转'\n'

批量下载的话，可以准备一个列表文件，每个歌曲名用回车隔开，如下：

    还过得去
    不敢太幸福
    小情歌
    爱情靠不住
    我爱我
    你可以不用给我答案 	金莎
    没有这首歌 	后弦
        回不去了吗 	萧亚轩
        有些事现在不做 一辈子都不会做了 	五月天
        第一夫人 	张杰

将这个list文件作为输入传入执行脚本：

    python2.7 tingdownload.py --input ~/music.txt

运行结果如下，列出四种情况：

* 下载成功，如果文件已经存在，会跳过
* 下载失败，由于网络原因
* 下载失败，由于关键词不准确而出现太多结果
* 下载失败，没有关键词匹配的结果


<pre>
> Start search *NSYNC  Bye Bye Bye...
X Error, can't find song: *NSYNC Bye Bye Bye.
> Start search Britney Spears  ...Baby One More Time...
V Info, download complete.
> Start search Lady Gaga  Brown Eyes...
V Info, download complete.
> Start search Maroon 5  Won’t Go Home Without You (Acoustic Version)...
X Error, can't find song: Maroon 5 Won’t Go Home Without You (Acoustic Version).
> Start search Nightwish  Meadows of Heaven...
V Info, download complete.
> Start search Aqua Timez  小さな掌...
X Error, can't find song: Aqua Timez 小さな掌.
> Start search 蔡淳佳  女人们的咖啡...
V Info, download complete.

== Download success (26) ==
Britney Spears  ...Baby One More Time
Lady Gaga  Brown Eyes
Nightwish  Meadows of Heaven
蔡淳佳  女人们的咖啡
John Mayer  Friends, Lovers Or Nothing
Suara  夢想歌
The Ting Tings  That's Not My Name
彭青  向往
梁靜茹  一秒的天堂
Mika  Lollipop
Hot Chelle Rae  Tonight Tonight
杨千嬅  翅膀下的风
梁靜茹  还是好朋友
李玟  想你的365天
陳奕迅  与我常在
陳奕迅  1874
陳奕迅  落花流水
陳奕迅  人来人往
陳奕迅  黑暗中漫舞
Brown Eyed Girls  Abracadabra
Boyzone  Paradise
Oasis  Stand By Me
Ne-Yo  So Sick
Eminem  Mockingbird
萧敬腾  每天爱你多一些
Big Time Rush  You're Not Alone

== Download failed for not fount (29) ==
*NSYNC  Bye Bye Bye
Maroon 5  Won’t Go Home Without You (Acoustic Version)
Aqua Timez  小さな掌
소녀시대  소원을 말해봐 (Genie) - Rock Tronic Remix Ver.
Shakira  Waka Waka (Esto es África)
青山テルマ feat. SoulJa  そばにいるね
소녀시대  Perfect for you
Shakira  Waka Waka (This Time For Africa) [K MIX]
Lena  A Million and One
Gil Shaham & Goran Solscher  Moshe Variations / Th?e. Tempo
Love  せつない サミシイ 悲しいときも
NARSHA & 정성하  I`m In Love

NARSHA & 정성하  I`m In Love
소녀시대  Honey( P)
Bigbang  마지막 인사 Remix
i'm sorry , i love u  像开始一样 (instrumental)
겨울연가  그대만이(Piano Ver.)
JTL  没能传达的话语
김종국  고맙다
yozoh  바나나파티 Banana Party
ERU  흰눈
Brown Eyes  Already a Year
차태현  내 손을 놓지 마요
黄雅诗&林海  七拍子 Seven Beats
Jessie J  Price Tag (Shux Remix) [feat. Devlin]
The Jackson 5  Love You Save
张悬  宝贝(In The Night)
蘇永康  那谁没有下次 (声演：卓韵芝)
曾宝仪&萧煌奇  美丽的情歌
Nickelback  Don't Ever Let It End
</pre>


## Change Log ##

* 2013-02-25 加入 `auto_match` 选项，可以自动下载第一个匹配的歌曲

Enjoy it.

Powered by [@alswl](http://log4d.com)

<!--vim: set ft=markdown expandtab nosmartindent:-->
