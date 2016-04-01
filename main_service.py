# -*- coding: utf-8 -*-
import sys
import random
from flask import Flask, request
from gifbot.helpers.wechat_api_helper import wechat_api_client, upload_wechat_media_by_url
from gifbot.gif_search.search_services import GifSearchService
from wechat_sdk.messages import TextMessage, ImageMessage, VideoMessage, ShortVideoMessage, LinkMessage, \
    LocationMessage, VoiceMessage, EventMessage
from wechat_sdk.exceptions import ParseError as WechatSdkParseError

reload(sys)
sys.setdefaultencoding('utf-8')

application = Flask(__name__)


@application.route('/', methods=['GET'])
def acknowledge_wechat_auth_request():
    """
    See detail in http://mp.weixin.qq.com/wiki/8/f9a0b8382e0b77d87b3bcc1ce6fbc104.html
    """

    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    if wechat_api_client.check_signature(signature, timestamp, nonce):
        print 'Wechat service verfication passed!'
        return echostr
    else:
        return 'Hey hello! What you just said?'


@application.route('/', methods=['POST'])
def respond_to_user_message_and_event():
    """
    See detail in
    Incoming request when user sends msg - http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html
    Incoming request when user subcribes/unscribes - mp.weixin.qq.com/wiki/7/9f89d962eba4c5924ed95b513ba69d9b.html
    Expected response - http://mp.weixin.qq.com/wiki/17/f298879f8fb29ab98b2f2971d42552fd.html
    """

    # these are only required when encrypt_mode='safe'
    msg_signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    request_body = request.data
    try:
        wechat_api_client.parse_data(request_body, msg_signature, timestamp, nonce)
    except WechatSdkParseError:
        print 'Failed to parse POST data ' + request_body
        return

    incoming_data = wechat_api_client.message
    response_data = ''

    if isinstance(incoming_data, TextMessage):
        response_data = respond_to_message_with_gif(incoming_data.content)
    elif isinstance(incoming_data, ImageMessage):
        response_data = wechat_api_client.response_text(u'小样还会发图?!')
    elif isinstance(incoming_data, VoiceMessage):
        response_data = wechat_api_client.response_text(u'小样还会语音?!')
    elif isinstance(incoming_data, VideoMessage):
        response_data = wechat_api_client.response_text(u'小样还会视频?!')
    elif isinstance(incoming_data, ShortVideoMessage):
        response_data = wechat_api_client.response_text(u'小样还会小视频?!')
    elif isinstance(incoming_data, LocationMessage):
        response_data = wechat_api_client.response_text(u'我关心你在哪干嘛?!')
    elif isinstance(incoming_data, LinkMessage):
        response_data = wechat_api_client.response_text(u'小样还会链接?!')
    elif isinstance(incoming_data, EventMessage) and incoming_data.type == 'subscribe':
        greeting_text = u'%s, 我在这等你很久了, 要什么图快说' % incoming_data.source
        response_data = wechat_api_client.response_text(greeting_text)

    return response_data


def respond_to_message_with_gif(message):

    search_service = GifSearchService.get_default()
    urls = search_service.search(message)

    # randomly select one of the images
    index = random.randint(0, len(urls) - 1)
    image_url = urls[index]

    # upload image to Wechat
    media_id = upload_wechat_media_by_url(image_url)
    return wechat_api_client.response_image(media_id)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True)
