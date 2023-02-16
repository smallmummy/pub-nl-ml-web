# encoding: UTF-8
import requests
import json
import time
import traceback
import copy
import argparse
import logging


class general_wx_corp:

    def __init__(self, corp_id, app_id, app_secret):
        # log filename
        self.LOG_FILE_NAME = "/tmp/wx_corp.log"
        self.RE_TRY_INVOKE_API = 3

        self.corp_id = corp_id
        self.app_id = app_id
        self.app_secret = app_secret

        self.access_token = None

        self.MSG_TEMPLATE = {
            "msgtype": "text",
            "agentid": self.app_id,
            "text": {
                "content": "no message set"
            },
            "safe": 0
        }
        

        # 初始化日志模块
        self.logger = logging.getLogger('main_wx_logger')
        self.logfile = self.LOG_FILE_NAME
        self.rotateHandler = logging.FileHandler(self.logfile)
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        self.rotateHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.rotateHandler)
        self.logger.setLevel(logging.INFO)

    def http_get_request(self, url, params, add_to_headers=None):
        try:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,id;q=0.2,zh-TW;q=0.2",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
            }
            if add_to_headers:
                headers.update(add_to_headers)

            postdata = params

            i = 0
            re_invoke_API = False

            while (i < self.RE_TRY_INVOKE_API and re_invoke_API is False):

                if (i != 0):
                    self.logger.info("invoke http failed!,sleep 0 seconds to do times:{0} retry!".format(i))

                data_proxy = ""
                self.logger.info(
                    "invoke http_get_request,postdata:{0}"
                    .format(postdata)
                )

                response = requests.post(
                    url, postdata, headers=headers, timeout=10, 
                    proxies=data_proxy
                )

                if response.status_code == 200:
                    # print("ok")
                    # 增加错误处理，如果返回的数据中有error，则提示详细info
                    re_invoke_API = True
                    return response.json()
                else:
                    # wrong status_code, need retry
                    self.logger.info('warning!the wrong status code!need retry, info: status_code:{0},text:{1}'.format(
                        response.status_code, response.text))
                    re_invoke_API = False

                i += 1

            if (re_invoke_API is False):
                # after MAX retry, still failed!warning
                self.logger.info('http error:after MAX retry, still failed!warning')

            return response.json()
        except Exception:
            self.logger.error(traceback.format_exc())

    def http_post_request(self, url, params, add_to_headers=None):

        try:
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,id;q=0.2,zh-TW;q=0.2",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
            }
            if add_to_headers:
                headers.update(add_to_headers)
            
            postdata = params
            i = 0
            re_invoke_API = False

            while (i < self.RE_TRY_INVOKE_API and re_invoke_API is False):

                if (i != 0):
                    self.logger.info(
                        "invoke http failed!,sleep 0 seconds to do times:{0} retry!"
                        .format(i)
                    )

                data_proxy = ""

                self.logger.info(
                    "invoke http_get_request,postdata:{0}"
                    .format(postdata)
                )

                response = requests.post(
                    url, postdata, headers=headers, timeout=10, 
                    proxies=data_proxy
                )

                if response.status_code == 200:
                    # print("ok")
                    # 增加错误处理，如果返回的数据中有error，则提示详细info
                    re_invoke_API = True
                    return response.json()
                else:
                    # wrong status_code, need retry
                    self.logger.info('warning!the wrong status code!need retry, info: status_code:{0},text:{1}'.format(
                        response.status_code, response.text))
                    re_invoke_API = False

                i += 1

            if (re_invoke_API is False):
                # after MAX retry, still failed!warning
                self.logger.info('http error:after MAX retry, still failed!warning')

            return response.json()
        except Exception:
            self.logger.error(traceback.format_exc())

    def get_access_token(self):
        try:
            url = XXX

            re_tmp = self.http_get_request(url, "")
            print(re_tmp)
            print(url)

            self.access_token = re_tmp['access_token']
            self.last_get_token_time = int(time.time())
            self.token_expire = re_tmp['expires_in']
        except Exception:
            self.logger.error(traceback.format_exc())

    def is_token_valid(self):
        if self.access_token is None:
            return False
        elif (int(time.time()) - self.last_get_token_time) > (self.token_expire - 200):
            return False
        else:
            return True

    def send_message(self, toparty='@all', touser='@all', msg="no msg set"):
        if not self.is_token_valid():
            self.get_access_token()

        body = copy.deepcopy(self.MSG_TEMPLATE)
        text = body.setdefault("text", {})
        text["content"] = msg

        if toparty is not None:
            body["toparty"] = toparty

        if touser is not None:
            body["touser"] = touser

        url = XXX

        data = self.http_post_request(url, json.dumps(body))
        #print(data)
        if data is None:
            return
        elif data["errcode"] != 0:
            pass
        else:
            pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--corp_id', required=True, help='corp id')
    parser.add_argument('--app_id', required=True, help='app id')
    parser.add_argument('--app_secret', required=True, help='app secret')
    parser.add_argument('--content', required=True, help='msg content')
    parser.add_argument('--touser', default='@all', help='touser')
    parser.add_argument('--toapp', default='btc', help='toapp')
    parser.add_argument('--toparty', default='@all', help='toparty')

    args = parser.parse_args()
    wx = general_wx_corp(
        corp_id=args.corp_id,
        app_id=args.app_id,
        app_secret=args.app_secret
    )

    wx.logger.info("args are:{0}".format(args))

    wx.send_message(
        touser=args.touser,
        toparty=args.toparty,
        msg=args.content
    )




