# AntiSARI
## 赋能企业，帮助企业能够快速了解员工的地点信息

## 使用方式 
1.github 拉取代码到本地

2.安装依赖文件  
```shell script
 pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```
3.复制config.template.yaml为config.yaml
```shell script
cp config.template.yamp config.yaml
```
4.修改 数据库相关参数

5.执行  python  main.py --t  创建数据库  (一次操作)

6.执行 python main.py --init  初始化数据(一次操作)

7.执行python main.py  启动web服务

