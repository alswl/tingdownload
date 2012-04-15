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

## 自动下载脚本tingdownload ##

早上下了几首音乐，就顺手写了一个脚本，用来批量从Badu Ting下载音乐。

代码在[github-tingdownload](https://github.com/alswl/tingdownload)

## 需要 ##

* Python 2 (仅在Python2.7下测试)
* BeautifulSoup(已包含在目录下)
* simplejson（已删除，我还是用原装json吧，省掉一个包）
* 一点点Python基础
* Linux/Windows（我在Linux没问题，Windows应该也可以）

## 使用方法 ##

在Shell(命令行)里输入下面随便一个命令，就会在当前目录下面出现 `musics` 文件夹，
里面就有下载好的音乐。

使用说明

    usage: tingdownload.py [-h] [--input INPUT] [Keyword [Keyword ...]]

    A script to download music from ting.baidu.com.

    positional arguments:
      Keyword

    optional arguments:
      -h, --help            show this help message and exit
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
█▓▒░alswl@x201█▓▒░ ~/dev/project/python/tingdownload/ ./tingdownload.py 黄昏\ 周传雄 考试什么 --input ~/a.txt
> Start download 黄昏 周传雄...
# Info: File "/home/alswl/dev/project/python/tingdownload/musics/周传雄-黄昏.mp3" exists.
> Start download 考试什么...
# Info: File "/home/alswl/dev/project/python/tingdownload/musics/徐良-考试什么的去死吧.mp3" exists.
> Start download 还过得去...
> Start download 不敢太幸福...
> Start download 小情歌...
# Failed: Too more result found for keyword 小情歌.
> Start download 爱情靠不住...

== Download success (4) ==
黄昏 周传雄
考试什么
还过得去
不敢太幸福

== Download failed for too many result (1) ==
小情歌
</pre>

Enjoy it.

Powered by [@alswl](http://log4d.com)

<!--vim: set ft=markdown expandtab nosmartindent:-->
