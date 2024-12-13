import requests,json,datetime
from config import py_mysql
from logins import logins
session = requests.Session()

# 企业信息数据
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
        data_list = resulte["data"]["result"]
        insert_into_list = []
        for data in data_list:
            id = data["qyid"]
            enterprise_code = data["qybh"]
            enterprise_name = data["dwmc"]
            # enterprise_type = data[""]
            credit_code = "" if data["tyshxydm"] == "无" else data["tyshxydm"]
            region_code = str(data["dwszqx"])+"000000"
            region_name = "睢县"
            longitude = "" if "-" in data["jd"] else data["jd"]
            latitude = "" if "-" in data["wd"] else data["wd"]
            try:
                legal_rep = data["fddbr"]
            except:
                legal_rep = ""
            try:
                legal_phone = data["fddbrdh"]
            except:
                legal_phone = ""
            try:
                contact = "" if data["lxr"] == "无" else data["lxr"]
            except:
                contact = ""
            try:
                contact_phone = "" if data["lxrsj"] == "无" else data["lxrsj"]
            except:
                contact_phone = ""
            try:
                reg_address = data["zcdz"]
            except:
                reg_address = ""
            try:
                industry_code = data["hyfl4"]
                industry_name = industry_dict[industry_code]
            except:
                industry_code = ""
                industry_name = ""
            try:
                discharge_permit = data["pwwj"]
            except:
                discharge_permit = ""
            enterprise_type = filter_qylx_type(data)
            is_used = "1"
            times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tuples = (int(id),enterprise_code,enterprise_name,credit_code,region_code,region_name,industry_code,industry_name,longitude,latitude,legal_rep,legal_phone,contact,contact_phone,reg_address,discharge_permit,enterprise_type,is_used,times,times)
            insert_into_list.append(tuples)
            print(tuples)
        cursor.executemany("insert into t_hazardous_waste_enterprise(id,enterprise_code,enterprise_name,credit_code,region_code,region_name,industry_code,industry_name,longitude,latitude,legal_rep,legal_phone,contact,contact_phone,reg_address,discharge_permit,enterprise_type,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                        on duplicate key update region_code=values (region_code),longitude=values (longitude),industry_code=values (industry_code),industry_name=values (industry_name),latitude=values (latitude),legal_rep=values (legal_rep),legal_phone=values (legal_phone),contact=values (contact),contact_phone=values (contact_phone),reg_address=values (reg_address),\
                        update_time=values (update_time),credit_code=values (credit_code),discharge_permit=values (discharge_permit),enterprise_type=values (enterprise_type)",insert_into_list)
        connect.commit()
    connect.close()
    cursor.close()

def filter_qylx_type(data):
    enterprise_type = ""
    try:
        if data["sfwfcsy"] == "1":
            # enterprise_type += qylx_type_dict["sfwfcsy"]
            enterprise_type += "sfwfcsy,"
    except:
        enterprise_type += ""
    try:
        if data["sfyfcsy"] == "1":
            # enterprise_type += qylx_type_dict["sfyfcsy"]
            enterprise_type += "sfyfcsy,"
    except:
        enterprise_type += ""
    try:
        if data["sfybgycsy"] == "1":
            # enterprise_type += qylx_type_dict["sfybgycsy"]
            enterprise_type += "sfybgycsy,"
    except:
        enterprise_type += ""
    try:
        if data["sfwfjy"] == "1":
            # enterprise_type += qylx_type_dict["sfwfjy"]
            enterprise_type += "sfwfjy,"
    except:
        enterprise_type += ""
    try:
        if data["sfwfys"] == "1":
            # enterprise_type += qylx_type_dict["sfwfys"]
            enterprise_type += "sfwfys,"
    except:
        enterprise_type += ""
    try:
        if data["sfwswncsy"] == "1":
            # enterprise_type += qylx_type_dict["sfwswncsy"]
            enterprise_type += "sfwswncsy,"
    except:
        enterprise_type += ""
    try:
        if data["sfsjqy"] == "1":
            # enterprise_type += qylx_type_dict["sfsjqy"]
            enterprise_type += "sfsjqy,"
    except:
        enterprise_type += ""  
    try:
        if data["sfdcjzzyd"] == "1":
            # enterprise_type += qylx_type_dict["sfdcjzzyd"]
            enterprise_type += "sfdcjzzyd,"
    except:
        enterprise_type += ""
    try:
        if data["sfwkk"] == "1":
            # enterprise_type += qylx_type_dict["sfwkk"]
            enterprise_type += "sfwkk,"
    except:
        enterprise_type += ""
    try:
        if data["sfdzfwcjqy"] == "1":
            # enterprise_type += qylx_type_dict["sfdzfwcjqy"]
            enterprise_type += "sfdzfwcjqy,"
    except:
        enterprise_type += ""
    return enterprise_type.strip(",")

if __name__ == "__main__":
    get_info()