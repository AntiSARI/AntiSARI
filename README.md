# Anti2019-nCoV小安报备平台

  全国新型肺炎疫情正在掀起一场没有硝烟的战役，举国上下团结一心应对疫情，各个单位在返程复工之际，员工健康和安全对单位的正常运营至关重要。

  Anti2019-nCoV小安报备平台，旨在为各大企业/组织/团体解决疫情期间成员行程追踪、健康状态、病患接触等信息统计和分析问题，帮助各单位组织及时统计并掌握人员的健康信息。平台提供组织注册、成员注册、成员登录、打卡定位、上报健康状态等功能，单位人员可每天定期进行地理位置信息打卡和防疫状态上报，系统根据成员提供的位置及状态数据和互联网的疫情大数据信息进行综合分析，生成成员分布热力图，组织管理者可实时了解本组织人员防疫健康情况和人员位置分布情况，识别人员健康安全状况风险。
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
