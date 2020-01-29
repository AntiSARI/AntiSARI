# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: constant.py
@Software: PyCharm
@Time :    2020/1/29 上午8:54
"""
apply_txt_template = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[{Content}]]></Content>
</xml>
"""

apply_image_template = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[image]]></MsgType>
  <Image>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
  </Image>
</xml>
"""

apply_voice_template = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[voice]]></MsgType>
  <Voice>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
  </Voice>
</xml>
"""

apply_video_template = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[video]]></MsgType>
  <Video>
    <MediaId><![CDATA[{MediaId}]]></MediaId>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
  </Video>
</xml>
"""