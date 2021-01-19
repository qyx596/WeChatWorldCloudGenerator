# WeChatWorldCloudGenerator
**根据iOS微信客户端数据库生成与某人的聊天词云**
### 1 获取iOS聊天记录数据库
首先使用iMazing或爱思助手等工具进行iOS整机备份，之后进入备份中的如下路径：

	/var/mobile/Applications/com.tencent.xin/Documents/
你应该会看到这些文件

/README_IMAGES/image1.png


然后进入找到以你微信号的MD5值命名的文件夹（类似图中打码的两个文件夹，一般只有一个，如果你登陆过多个微信账号，这种文件夹也会有多个），进入这个文件夹下的'DB'文件夹

/README_IMAGES/image2.png

这里的***message_整数.sqlite***文件为聊天记录保存的数据库，可能会有多个，所需要的聊天内容可能保存在其中任何一个文件上，建议一次性全部导出，***WCDB_Conntact.sqlite***文件则为联系人信息，其中的联系人wechatID将会被MD5处理后作为对应聊天记录数据库中的表名，也一并导出。
### 2 生成词云 
#### 2.1 准备文件
将上一步获取的数据库文件拷贝至本项目文件夹中名为***WECHATFILES***的文件夹中，并根据注释修改***generator.py***文件中相关常量的值。生成词云形状图片和色相也能通过相关常量修改。

/README_IMAGES/image3.png

***以上所有值都不能为空***
#### 2.2 环境配置
```bash
pip install -r requirements.txt
```
#### 2.3 运行
```bash
python generator.py
```
生成的词云图片保存在本项目主目录下名为***result.png***
### TODO
- [ ] 引导式运行
- [ ] 自动从备份中获取iOS微信数据库
- [ ] 优化代码