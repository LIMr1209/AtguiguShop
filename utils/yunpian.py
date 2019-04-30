import requests
import json


class YunPian(object):
    """
    发送验证码
    """
    def __init__(self):
        self.apikey = '4f70824dde066067241393c80c291ea6'
        self.sms_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_msg(self, mobile, code):
        data = {
            'apikey': self.apikey,
            'mobile': mobile,
            'text': '您的验证码是{}。如非本人操作，请忽略本短信'.format(code)
        }
        response = requests.post(self.sms_send_url, data=data)
        text = response.text
        result = json.loads(text)
        return result


if __name__ == '__main__':
    yp = YunPian()
    print(yp.send_msg('17635700440', '1209'))
