from gifbot.config.constants import *
from wechat_sdk import WechatConf, WechatBasic

# see http://wechat-python-sdk.com/quickstart/official/
wechat_api_client_conf = WechatConf(
   token=WECHAT_TOKEN,
   appid=None,
   appsecret=None,
   encrypt_mode=WECHAT_ENCRYPTION_MODE,
   encoding_aes_key=WECHAT_ENCODING_AES_KEY
)

wechat_api_client = WechatBasic(wechat_api_client_conf)

def upload_wechat_media_by_url(url, wechat=wechat_api_client):
   """
   :param url: the URL of the image to be uploaded
   :param wechat: Wechat API client
   :return: media ID returned by Wechat
   """
   return ''