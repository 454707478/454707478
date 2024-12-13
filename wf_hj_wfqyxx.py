import requests,json,datetime,re,uuid
from config import py_mysqls
from logins import logins
session = requests.Session()

# 固定源危废经营许可证信息数据
def get_wfjyxk():
    with open("token.txt", 'r') as f:
        token = json.loads(f.read())['token']
        f.close
    with open("Authorkey.txt", 'r') as f:
        Authorkey_list = json.loads(f.read())["header_Authorkey"]
        f.close
    header_Authorkey = Authorkey_list[0]
    Authorkey = Authorkey_list[1]
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Authorization": token,
        "content-type": "application/json;charset=UTF-8",
        "referer": "https://gfgl.meescc.cn/",
        header_Authorkey: Authorkey
    }
    post_data = {"areaCode": "411422","bussUnitType": "","cerbasetype":"1","cityCode": "","countyCode": "411422","isEnable": "","licenseNo": "",
                "licenseStatus": "","licenseType": "","method": "","provinceCode": "","typeName": "","unitName": "","validBeginDate": "",
                "validEndDate": "","wasteCode":""}
    info_url = "https://gfgl.meescc.cn/hlwjjg/tCerCerbase/1/20"
    response = session.post(info_url,headers=header,json=post_data).text
    resulte = json.loads(response)
    if resulte["code"] == "100":
        code = logins()
        if code == "200":
            with open("Authorkey.txt", 'r') as f:
                Authorkey_list = json.loads(f.read())["header_Authorkey"]
                f.close
            header_Authorkey = Authorkey_list[0]
            Authorkey = Authorkey_list[1]
            with open("token.txt", 'r') as f:
                token = json.loads(f.read())['token']
                f.close
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "accept": "application/json, text/plain, */*",
                "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Authorization": token,
                "content-type": "application/json;charset=UTF-8",
                "referer": "https://gfgl.meescc.cn/",
                header_Authorkey: Authorkey
            }
            response = session.post(info_url,headers=header,json=post_data).text
            resulte = json.loads(response)
            result_obj(resulte,header)
        else:
            pass
    else:
        result_obj(resulte,header)

def result_obj(resulte,header):
    connect, cursor = py_mysqls()
    insert_into_list = []
    data_list = resulte["data"]["result"]
    for data in data_list:
        ids = data["id"]
        ID = "SYSTEM_03_" + str(ids)
        TYSHXYDM = data["orgCode"]
        POLLUTESOURCE_CODE = ids
        POLLUTESOURCE_NAME = data["unitName"]
        LICENSENUM = data["licenseNo"]
        REGION_CODE = str(data["countyCode"])+"000000"
        REGION_NAME = "睢县"
        REGADDRESS = data["residence"]
        LEGAL_REPRESENTATIVE = data["linkMan"]
        ENTERADDRESS = data["residence"]
        ENVIRON_LINKMEN = data["linkMan"]
        ENVIRON_TEL = data["linkManTel"]
        LONGITUDE = "" if "0-" in data["longitude"] else data["longitude"] 
        LATITUDE = "" if "0-" in data["latitude"] else data["latitude"]
        IS_USED = "1"
        SYSTEM = "SYSTEM_03"
        SYSTEM_CODE = "03"
        SYSTEM_NAME = "危废经营许可证"
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tuples = (ID,TYSHXYDM,POLLUTESOURCE_CODE,POLLUTESOURCE_NAME,LICENSENUM,REGION_CODE,REGION_NAME,REGADDRESS,LEGAL_REPRESENTATIVE,ENTERADDRESS,ENVIRON_LINKMEN,ENVIRON_TEL,LONGITUDE,LATITUDE,SYSTEM,SYSTEM_CODE,SYSTEM_NAME,IS_USED,times,times)
        print(tuples)
        insert_into_list.append(tuples)
    cursor.executemany("insert into t_pollutesource_converge(ID,TYSHXYDM,POLLUTESOURCE_CODE,POLLUTESOURCE_NAME,LICENSENUM,REGION_CODE,REGION_NAME,REGADDRESS,LEGAL_REPRESENTATIVE,ENTERADDRESS,ENVIRON_LINKMEN,ENVIRON_TEL,LONGITUDE,LATITUDE,SYSTEM,SYSTEM_CODE,SYSTEM_NAME,\
                       IS_USED,CREATE_TIME,UPDATE_TIME)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update POLLUTESOURCE_NAME=values (POLLUTESOURCE_NAME),LICENSENUM=values (LICENSENUM),REGION_CODE=values (REGION_CODE),\
                       REGION_NAME=values (REGION_NAME),REGADDRESS=values (REGADDRESS),LEGAL_REPRESENTATIVE=values (LEGAL_REPRESENTATIVE),ENTERADDRESS=values (ENTERADDRESS),ENVIRON_LINKMEN=values (ENVIRON_LINKMEN),ENVIRON_TEL=values (ENVIRON_TEL),\
                       LONGITUDE=values (LONGITUDE),LATITUDE=values (LATITUDE),SYSTEM=values (SYSTEM),SYSTEM_CODE=values (SYSTEM_CODE),SYSTEM_NAME=values (SYSTEM_NAME),UPDATE_TIME=values (UPDATE_TIME)",insert_into_list)
    connect.commit()
    connect.close()
    cursor.close() 
    
if __name__ == "__main__":
    get_wfjyxk()
