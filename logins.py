import requests,execjs,json,base64,hashlib
from chaojiying import Chaojiying_Client
session = requests.Session()

def logins():
    e = "010001"
    t = ""
    a = "00b0fa2cf63bf2f29b44105e4b61213e5020dad9d55853934762f283f20b7bc8ba70d9ff8f471f89150f7e7bbfd106fc82f354336636ed47498ee131fb24426dcff9a9d6086703a629b7cf9fa98808695471a9798b19f02d48990724ad3f71b7c8a5909368d4880b460c49d8c4596ec8e8aa047c986a803b4904aa455947790431"
    header_md5 = "Authorkey"
    md5 = hashlib.md5()  # 创建一个md5对象
    md5.update(header_md5.encode('utf-8'))  # 使用utf-8编码数据
    header_Authorkey = md5.hexdigest()  # 返回加密后的十六进制字符串
    obj = execjs.compile(open(r"psw_decrypted.js", encoding='utf-8').read()).call('XRcO',e,t,a)
    password, Authorkey = obj["psw"], obj["authorkey"]
    with open("Authorkey.txt", "w") as f:
        Authorkey_dict = {}
        Authorkey_dict["header_Authorkey"]=[header_Authorkey,Authorkey]
        f.write(json.dumps(Authorkey_dict))
        f.close
    Image_url = "https://gfgl.meescc.cn/hlwjjg/admin/getImage"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Connection": "close" 
    }
    response = session.get(Image_url,headers=header).text
    result = json.loads(response)
    message = result['message']
    data = result['data']
    if message == '成功':
        imgData = data['imgData']
        img = base64.b64decode(imgData)
        authImage = data['authImage']
        with open("captcha.jpg", "wb") as f:
            f.write(img)
            f.close
        vcode = Chaojiying_Client('aury2020', 'AY2020..', '964775').run()
        login_url = "https://gfgl.meescc.cn/hlwjjg/admin/login"
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "referer": "https://gfgl.meescc.cn/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
        data = {
            "account": "411422_2021",
            "authimage": authImage,
            "password": password,
            "vcode": vcode,
            "zwId": ""
        }
        response = session.post(login_url,headers=header,json=data).text
        result = json.loads(response)
        message = result["message"]
        if message == '成功':
            token = result["data"]["token"]
            with open("token.txt", 'w', encoding='utf-8') as f:
                f.write(json.dumps({"token":token}))
                f.close
            return "200"
        else:
            pass
    else:
        pass

# if __name__ == "__main__":
#     logins()
