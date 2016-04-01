from flask import Flask, request
from gifbot.helpers.wechat_api_helper import wechat_api_client

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


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)
