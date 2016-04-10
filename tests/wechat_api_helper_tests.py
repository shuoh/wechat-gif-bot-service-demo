import unittest
from gifbot.helpers.wechat_api_helper import upload_wechat_media_by_url, wechat_api_client


class TestWechatApiHelper(unittest.TestCase):

    def setUp(self):
        pass

    def test_upload_media_success(self):
        media_id = upload_wechat_media_by_url(url='https://media0.giphy.com/media/fmNp5I53lfUuA/200w.gif',
                                              wechat_client_local=wechat_api_client)
        print media_id

        self.assertIsInstance(media_id, str)
        self.assertGreater(len(media_id), 1)
