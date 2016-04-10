import shutil
import tempfile
import requests
from gifbot.config.constants import *
from wechat_sdk import WechatConf, WechatBasic

# see http://wechat-python-sdk.com/quickstart/official/
wechat_api_client_conf = WechatConf(
   token=WECHAT_TOKEN,
   appid=WECHAT_APP_ID,
   appsecret=WECHAT_APP_SECRET,
   encrypt_mode=WECHAT_ENCRYPTION_MODE,
   encoding_aes_key=WECHAT_ENCODING_AES_KEY
)

wechat_api_client = WechatBasic(wechat_api_client_conf)


def upload_wechat_media_by_url(url, wechat_client_local=wechat_api_client):
    """
    :param url: the URL of the image to be uploaded
    :param wechat: Wechat API client
    :return: media ID returned by Wechat
    """

    extension = url.split('.')[-1]
    dot_extension = '.' + extension

    # download to file system
    download_response = requests.get(url, stream=True)
    temp_file = tempfile.NamedTemporaryFile(suffix=dot_extension, prefix='gifbot-tmp-image-', delete=False)
    temp_filepath = temp_file.name
    shutil.copyfileobj(download_response.raw, temp_file)
    temp_file.close()

    # create a new file instance
    with open(temp_filepath) as media_file:
        # upload to Wechat
        response = wechat_client_local.upload_media(media_type='image', media_file=media_file)
        return response.get('media_id')
