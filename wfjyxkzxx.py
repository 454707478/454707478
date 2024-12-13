import requests,json,datetime,re
from config import py_mysql
from logins import logins
session = requests.Session()

# 危废经营许可证信息数据
def get_wfjyxk():
    with open("token.txt", 'r') as f:
        token = json.loads(f.read())['token']
        f.close
    with open("Authorkey.txt", 'r') as f:
        Authorkey_list = json.loads(f.read())["header_Authorkey"]
        f.close
    header_Authorkey = Authorkey_list[0]
    Authorkey = Authorkey_list[1]
    # connect, cursor = py_mysql()
    # cursor.execute("select enterprise_code,credit_code from t_hazardous_waste_enterprise")
    # connect.commit()
    # credit_info = cursor.fetchall()
    # connect.close()
    # cursor.close()  
    # credit_dict = {}
    # for credit_data in credit_info:
    #     credit_dict[credit_data[0]] = credit_data[1]
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
    connect, cursor = py_mysql()
    insert_into_list = []
    data_list = resulte["data"]["result"]
    for data in data_list:
        print(data)
        id = data["id"]
        credit_code = data["orgCode"]
        enterprise_name = data["unitName"]
        permit_code = data["licenseNo"]
        region_code = str(data["countyCode"])+"000000"
        region_name = "睢县"
        reg_address = data["residence"]
        legal_rep = data["linkMan"]
        business_address = data["residence"]
        valid_start_date = data["validBeginDate"]
        valid_end_date = data["validEndDate"]
        issuing_agency = data["licenseAward"]
        issuing_date = data["firstAwardDate"]
        contact_name = data["linkMan"]
        contact_phone = data["linkManTel"]
        longitude = "" if "0-" in data["longitude"] else data["longitude"] 
        latitude = "" if "0-" in data["latitude"] else data["latitude"]
        facility_address = data["facilitiesAddress"]
        isEnable_dict = {
            "1": "1",
            "2": "0"
        }
        permit_type_dict = {
            "3": "医疗废物经营许可证",
            "4": "危险废物收集经营许可证",
            "5": "豁免经营许可证",
            "7": "危险废物处置利用经营许可证",
            "8": "虚拟经营许可证"
        }
        hw_type_dict = {
            "0": "危险废物收集",
            "1": "同时利用和处置危险废物（不含医疗废物）",
            "2": "只处置医疗废物",
            "3": "同时利用处置危险废物及处置医疗废物",
            "4": "只利用危险废物（不含医疗废物）",
            "5": "只处置危险废物（不含医疗废物）"
        }
        permit_type = data["licenseType"]
        hw_type = data["bussUnitType"]
        waste_url = "https://gfgl.meescc.cn/hlwjjg/tCerCerbaseWaste/wastelist/"+id
        waste_data = session.post(waste_url,headers=header).text
        waste_data_list = json.loads(waste_data)["data"]
        wf_code_list = []
        wf_type_list = []
        for waste_data in waste_data_list:
            wf_code_list.append(re.sub(r'[\u4e00-\u9fa5]','',waste_data["wasteCode"]))
            wf_type_list.append(re.sub(r'[\u4e00-\u9fa5]','',waste_data["wasteType"]))
        wf_code = ""
        for i in list(set(wf_code_list)):
            wf_code += i+","
        wf_code = wf_code.strip(",")
        wf_type = ""
        for i in list(set(wf_type_list)):
            wf_type += i+","
        wf_type = wf_type.strip(",")
        enabled_status = isEnable_dict[data["isEnable"]]
        is_used = "1"
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return
        tuples = (id,credit_code,enterprise_name,permit_code,region_code,region_name,reg_address,legal_rep,business_address,valid_start_date,
                  valid_end_date,issuing_agency,issuing_date,contact_name,contact_phone,longitude,latitude,facility_address,permit_type,hw_type,wf_code,wf_type,enabled_status,is_used,times,times)
        print(tuples)
        insert_into_list.append(tuples)
    cursor.executemany("insert into t_hazardous_waste_permit(id,credit_code,enterprise_name,permit_code,region_code,region_name,reg_address,legal_rep,business_address,valid_start_date,\
                    valid_end_date,issuing_agency,issuing_date,contact_name,contact_phone,longitude,latitude,facility_address,permit_type,hw_type,wf_code,wf_type,enabled_status,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    on duplicate key update enterprise_name=values (enterprise_name),permit_code=values (permit_code),region_code=values (region_code),region_name=values (region_name),reg_address=values (reg_address),legal_rep=values (legal_rep),\
                    business_address=values (business_address),valid_start_date=values (valid_start_date),valid_end_date=values (valid_end_date),issuing_agency=values (issuing_agency),issuing_date=values (issuing_date),contact_name=values (contact_name),\
                    contact_phone=values (contact_phone),longitude=values (longitude),latitude=values (latitude),facility_address=values (facility_address),update_time=values (update_time),region_code=values (region_code),permit_type=values (permit_type),hw_type=values (hw_type),\
                    wf_code=values (wf_code),wf_type=values (wf_type),enabled_status=values (enabled_status)",insert_into_list)
    connect.commit()
    connect.close()
    cursor.close() 
    
if __name__ == "__main__":
    get_wfjyxk()
