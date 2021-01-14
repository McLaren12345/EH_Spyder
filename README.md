# E站学习资料下载器(爬虫)

### 1. 概述
本程序用于批量从E站(表站)下载学习资料，支持列表自动化下载，错误日志提醒，多线程下载的功能。

### 2.使用方法
2.1 修改`config.ini`文件中的下载目录，多线程下载的线程数，其余信息目前暂时用不到，可以忽略，下载地址不填则自动下载至程序所在目录的Download文件夹下，线程不填默认15。

2.2 将资料的网站填入download.txt文件中，一行写一个网址，否则会出错。

2.3 在PyCharm或其他IDE中运行`main.py`即可，错误与警告信息会写入`log.txt`文件夹下。

### 备注
日志部分有3种警告级别：
>1.INFO：如果该资料已经下载过(仅检测下载目录)，则不再下载，并输出INFO信息；
>
>2.WARNING：如果一个资料中的某张图片下载出错，报警告，会打印出文件的网址与页码；
>
>3.ERROR：如果资料本身存在问题（网址错误等）会报错误，打印资料的网址以供检查。