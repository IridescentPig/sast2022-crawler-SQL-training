# Zhihu_crawler 

## 环境配置

在当前目录运行 ` pip install -r ../requirement.txt  ` 指令安装所需依赖（与 `WebVPN_crawler` 的依赖相同，只需安装一次）

## 使用说明

1. 在当前目录创建 `zhihu.json` 文件，文件格式与内容如下：

   ```json
   {
     "headers": {
       "User-Agent": "Your User-Agent", /*required*/
       "Cookie": "Your Cookie after logging in zhihu"/*required*/
     },
     "config": {
       "interval_between_board": 600,/*interval between two crawls of board, required*/
       "interval_between_question": 2/*interval between two crawls of questions, required*/
     },
     "mysql": {
       "host": "",/*server ip where your SQL service on*/
       "user": "",/*Your mysql user name*/
       "password": "",/*Your mysql user password*/
       "database": "",/*Database to save data*/
       "charset": "utf8mb4",/*charset to use, recommend utf8mb4*/
       "port": 1/*port which your sql service use*/
     }
   }
   ```

2. 使用 ` python zhihu.py` 运行爬虫程序，程序会以你设定的时间爬取知乎热榜内容，并存在指定的 ` database` 中。