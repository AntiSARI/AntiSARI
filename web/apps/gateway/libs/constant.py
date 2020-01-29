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

apply_view_template = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[event]]></MsgType>
  <Event><![CDATA[VIEW]]></Event>
  <EventKey><![CDATA[{EventKey}]]></EventKey>
</xml>
"""


apply_news_template_start = """
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[news]]></MsgType>
  <ArticleCount>{ArticleCount}</ArticleCount>
  <Articles>
"""

apply_news_template_item = """
    <item>
      <Title><![CDATA[{Title}]]></Title>
      <Description><![CDATA[{Description}]]></Description>
      <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
      <Url><![CDATA[{Url}]]></Url>
    </item>
"""

apply_news_template_end = """
  </Articles>
</xml>
"""