# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: settings.py
@Software: PyCharm
@Time :    2019/12/5 上午10:23
"""
import yaml
import os

with open(os.path.join(os.getcwd(), 'config.yaml')) as f:
    config = yaml.safe_load(f.read())

# 系统配置映射
system = config.get('system')
JWT_EXPIRE_LIST = [int(i) for i in system.get('jwt_expire').split("*")]  # jwt 过期时间
sys_debug = system.get('debugs')
sys_secret = system.get('secret')
sys_prefix = system.get('prefix')
sys_login_url = system.get('login_url')
sys_static = system.get('static')
sys_templates = system.get('templates')
sys_static_url_prefix = system.get('static_url_prefix')
sys_xsrf_cookies = system.get('xsrf_cookies')
sys_port = system.get('port', 8080)
sys_auto_reload = system.get('auto_reload')
sys_jwt_expire = JWT_EXPIRE_LIST[0] * JWT_EXPIRE_LIST[1] * JWT_EXPIRE_LIST[2]
sys_public_key = system.get('public_key')
sys_private_key = system.get('private_key')
sys_aes_key = system.get('aes_key')
sys_aes_iv = system.get('aes_iv')


# 数据库配置映射
database = config.get('database')
db_username = database.get('username')
db_port = database.get('port') if database.get('port') else 3306
db_database = database.get('database')
db_hostname = database.get('hostname')
db_password = database.get('password')


# 中间件
middleware_list = config.get('middles') if config.get('middles') else []
