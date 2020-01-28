# 新型冠状病毒防疫人员统计平台

​    全国新型肺炎疫情正在掀起一场没有硝烟的战役。 本项目—新型冠状病毒防疫人员统计平台，旨在帮助各单位组织及时统计并掌握人员的健康信息。单位人员可每天定期进行地理位置信息打卡和防疫状态上报，组织管理者可通过平台的管理界面，全面了解本组织人员防疫情况和人员分布情况。

## 使用方式

1. github 拉取代码到本地

2. 安装依赖文件

    ```shell
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
    ```

3. 复制config.template.yaml为config.yaml

    ```shell
    cp config.template.yamp config.yaml
    ```

4. 修改数据库相关参数

5. 执行 创建数据库 (一次操作)
   
    ```shell
    python main.py --t 
    ```
    
6. 初始化数据(一次操作)

    ```shell
    python main.py --init
    ```

7. 启动web服务
   
    ```shell
    python main.py 
    ```
