# WebVPN_crawler 

## 环境配置

在当前目录运行 ` pip install -r ../requirement.txt  ` 指令安装所需依赖（与 `Zhihu_crawler` 的依赖相同，只需安装一次）

## 使用说明

1. 在当前目录创建 `settings.json` 文件，文件格式与内容如下：

   ```json
   {
     "username": "Your student ID, like 2021XXXXXX",
     "password": "Your password, like **********"
   }
   ```

2. 使用 ` python webvpn.py` 运行爬虫程序，程序会爬取并自动计算每个学期的 `gpa` 并输出，格式为：

   ```
   2021-秋：*.**
   2022-春：*.**
   ...
   ```