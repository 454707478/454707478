import requests,json,datetime,uuid
from config import py_mysqls,py_mysql,qylx_type_dict
from logins import logins
session = requests.Session()

# 固定源危废经企业信息
def get_info():
    with open("token.txt", 'r') as f:
        token = json.loads(f.read())['token']
        f.close
    with open("Authorkey.txt", 'r') as f:
        Authorkey_list = json.loads(f.read())["header_Authorkey"]
        f.close
    header_Authorkey = Authorkey_list[0]
    Authorkey = Authorkey_list[1]
    connect, cursor = py_mysql()
    cursor.execute("select industry_code,industry_name from t_dict_industry_type")
    connect.commit()
    cursor.close()
    connect.close()
    industry_info = cursor.fetchall()
    industry_dict = {}
    for industry_data in industry_info:
        industry_dict[industry_data[0]] = industry_data[1]
    info_url = "https://gfgl.meescc.cn/hlwjjg/tEntEnterprise/1/200"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Authorization": token,
        "Cookie": "name=value; route=; loginToken={}".format(token),
        "origin": "https://gfgl.meescc.cn",
        "referer": "https://gfgl.meescc.cn/",
        header_Authorkey: Authorkey
    }
    data = {"approval": "","archivesFinish": "","areaCode": "411422","driverName": "","dwmc": "","dwszcs": "411400","dwszqx": "411422","dwszsf": "410000",
            "endDate": "","enterType": "","gllb": "","hyfl1": "","hyfl2": "","hyfl3": "","hyfl4": "","licenseNo": "","platenumbe": "","reportGen": "",
            "sfdzfwcjqy": "","sfksqy": "","sfsjqy": "","sfwfcsy": "","sfwfjy": "","sfwfys": "","sfwkk": "","sfwswncsy": "","sfxwqy": "","sfybgycsy": "",
            "sfyfcsy": "","sfzx": "0","sfzyd": "","startDate": "","twocf": "","yljgType": "","zzjgdm": "","": ""}
    response = session.post(info_url,headers=header,json=data).text
    resulte = json.loads(response)
    if resulte["code"] == "100":
        code = logins()
        if code == "200":
            get_info()
        else:
            pass
    else:
        connect, cursor = py_mysqls()
        data_list = resulte["data"]["result"]
        insert_into_list = []
        for data in data_list:
            ID = "SYSTEM_02_" + str(data["qybh"])
            POLLUTESOURCE_CODE = data["qybh"]
            POLLUTESOURCE_NAME = data["dwmc"]
            TYSHXYDM = "" if data["tyshxydm"] == "无" else data["tyshxydm"]
            REGION_CODE = str(data["dwszqx"])+"000000"
            REGION_NAME = "睢县"
            LONGITUDE = "" if "-" in data["jd"] else data["jd"]
            LATITUDE = "" if "-" in data["wd"] else data["wd"]
            try:
                LEGAL_REPRESENTATIVE = data["fddbr"]
            except:
                LEGAL_REPRESENTATIVE = ""
            try:
                LEGAL_REPRESENTATIVE_TEL = data["fddbrdh"]
            except:
                LEGAL_REPRESENTATIVE_TEL = ""
            try:
                ENVIRON_LINKMEN = "" if data["lxr"] == "无" else data["lxr"]
            except:
                ENVIRON_LINKMEN = ""
            try:
                ENVIRON_TEL = "" if data["lxrsj"] == "无" else data["lxrsj"]
            except:
                ENVIRON_TEL = ""
            try:
                ENTERADDRESS = data["zcdz"]
            except:
                ENTERADDRESS = ""
            try:
                TRADE_CODE = data["hyfl4"]
                TRADE_NAME = industry_dict[TRADE_CODE]
            except:
                TRADE_CODE = ""
                TRADE_NAME = ""
            try:
                LICENSENUM = data["pwwj"]
            except:
                LICENSENUM = ""
            SYSTEM = "SYSTEM_02"
            SYSTEM_CODE = "02"
            SYSTEM_NAME = "危废企业"
            IS_USED = "1"
            times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tuples = (ID,POLLUTESOURCE_CODE,POLLUTESOURCE_NAME,TYSHXYDM,REGION_CODE,REGION_NAME,LONGITUDE,LATITUDE,LEGAL_REPRESENTATIVE,LEGAL_REPRESENTATIVE_TEL,ENVIRON_LINKMEN,ENVIRON_TEL,ENTERADDRESS,TRADE_CODE,TRADE_NAME,LICENSENUM,SYSTEM,SYSTEM_CODE,SYSTEM_NAME,IS_USED,times,times)
            insert_into_list.append(tuples)
            print(tuples)
        cursor.executemany("insert into t_pollutesource_converge(ID,POLLUTESOURCE_CODE,POLLUTESOURCE_NAME,TYSHXYDM,REGION_CODE,REGION_NAME,LONGITUDE,LATITUDE,LEGAL_REPRESENTATIVE,LEGAL_REPRESENTATIVE_TEL,ENVIRON_LINKMEN,ENVIRON_TEL,ENTERADDRESS,TRADE_CODE,TRADE_NAME,LICENSENUM,SYSTEM,SYSTEM_CODE,SYSTEM_NAME,IS_USED,CREATE_TIME,UPDATE_TIME)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                        on duplicate key update REGION_CODE=values (REGION_CODE),REGION_NAME=values (REGION_NAME),LONGITUDE=values (LONGITUDE),LATITUDE=values (LATITUDE),LEGAL_REPRESENTATIVE=values (LEGAL_REPRESENTATIVE),LEGAL_REPRESENTATIVE_TEL=values (LEGAL_REPRESENTATIVE_TEL),ENTERADDRESS=values (ENTERADDRESS),TRADE_CODE=values (TRADE_CODE),TRADE_NAME=values (TRADE_NAME),LICENSENUM=values (LICENSENUM),\
                        SYSTEM=values (SYSTEM),SYSTEM_CODE=values (SYSTEM_CODE),SYSTEM_NAME=values (SYSTEM_NAME),UPDATE_TIME=values (UPDATE_TIME)",insert_into_list)
        connect.commit()
        connect.close()
        cursor.close()


if __name__ == "__main__":
    get_info()