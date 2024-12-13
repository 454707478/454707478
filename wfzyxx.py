import requests,json,datetime,time,math
from config import py_mysql
from logins import logins
session = requests.Session()

# 危废转运信息数据
def get_wfzy():
    with open("token.txt", 'r') as f:
        token = json.loads(f.read())['token']
        f.close
    with open("Authorkey.txt", 'r') as f:
        Authorkey_list = json.loads(f.read())["header_Authorkey"]
        f.close
    header_Authorkey = Authorkey_list[0]
    Authorkey = Authorkey_list[1]
    connect, cursor = py_mysql()
    cursor.execute("select enterprise_code,credit_code from t_hazardous_waste_enterprise")
    connect.commit()
    credit_info = cursor.fetchall()
    connect.close()
    cursor.close()  
    credit_dict = {}
    for credit_data in credit_info:
        credit_dict[credit_data[0]] = credit_data[1]
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
    startdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    enddate = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    post_data = {"activeName":"","areaCode":"","bjenddate":"","bjstartdate":"","citycode": "","confirmoutnum":"","countrycode":"","dataSource":"","disposal":"",
            "enddate":enddate,"enterName":"","hyfl1":"","hyfl2":"","hyfl3":"","hyfl4":"","jareaCode":"","jcitycode":"","jcountrycode":"","jprovincecode":"",
            "munitname":"","paperno":"","platenumbe":"","provincecode":"","roleType":"402822c56df60394016df60a10c70008,gfhkhqy,5442230de54703aad798dad2ad99671b,acda51bdb0c22332783271ce22aed6ca",
            "startdate":startdate,"status":"","tranManifestType":"","tranPlanNo":"","wasteType":"","wastecode":"","wastename":"","yunitname":"","ywgj":""}
    info_url = "https://gfgl.meescc.cn/hlwjjg/tBasTranManifest/1/20"
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
            page = math.ceil(resulte['data']['recordCount']/20)
            for index in range(1,page+1):
                time.sleep(3)
                result_obj(credit_dict,header,index,post_data)
        else:
            pass
    else:
        page = math.ceil(resulte['data']['recordCount']/20)
        for index in range(1,page+1):
            time.sleep(3)
            result_obj(credit_dict,header,index,post_data)

def result_obj(credit_dict,header,index,post_data):
    print(index)
    info_url = "https://gfgl.meescc.cn/hlwjjg/tBasTranManifest/{}/20".format(index)
    response = session.post(info_url,headers=header,json=post_data).text
    resulte = json.loads(response)
    data_list = resulte["data"]["result"]
    connect, cursor = py_mysql()
    insert_into_list = []
    for data in data_list:
        id = data["pkId"]
        enterprise_code = data["enterid"]
        enterprise_name = data["creator"]
        try:
            credit_code = credit_dict[enterprise_code]
        except:
            continue
        region_code = str(data["countrycode"])+"000000"
        region_name = "睢县"
        try:
            order_code = data["resPaperno"]
        except:
            order_code = ""
        order_name = ""
        initiate_unit_name = data["cunitname"]
        initiate_unit_address = data["cunitAddress"]
        initiate_user = data["clinkman"]
        phone_number = data["clinkmantel"]
        url = "https://gfgl.meescc.cn/hlwjjg/tBasTranManifest/getTranManifestDataInfo"
        datas = {"pkId": id}
        time.sleep(3)
        response = session.post(url,headers=header,json=datas).text
        resulte = json.loads(response)
        category_code_name = resulte["data"]["tranList"][0]["wasteList"][0]
        category_code = category_code_name["wastecode"]
        category_name = category_code_name["wastename"]
        actual_weight = data["tranOutSum"]
        accept_unit_name = data["junitname"]
        accept_unit_address = data["munitaddress"]
        accept_unit_phone = data["jlinkmantel"]
        order_status = data["status"]
        submission_date = data["createDate"]
        try:
            deal_time = data["ltime"]
        except:
            deal_time = ""
        try:
            finish_time = data["jtime"]
        except:
            finish_time = ""
        is_used = "1"
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tuples = (id,enterprise_code,enterprise_name,credit_code,region_code,region_name,order_code,order_name,initiate_unit_name,initiate_unit_address,initiate_user,phone_number,category_code,category_name,actual_weight,
                  accept_unit_name,accept_unit_address,accept_unit_phone,order_status,submission_date,deal_time,finish_time,is_used,times,times)
        # print(tuples)
        insert_into_list.append(tuples)
    cursor.executemany("insert into t_enterprise_hazwaste_trans(id,enterprise_code,enterprise_name,credit_code,region_code,region_name,order_code,order_name,initiate_unit_name,initiate_unit_address,initiate_user,phone_number,category_code,category_name,actual_weight,\
                    accept_unit_name,accept_unit_address,accept_unit_phone,order_status,submission_date,deal_time,finish_time,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    on duplicate key update initiate_unit_name=values (initiate_unit_name),initiate_unit_address=values (initiate_unit_address),initiate_user=values (initiate_user),phone_number=values (phone_number),category_code=values (category_code),category_name=values (category_name),\
                    actual_weight=values (actual_weight),accept_unit_name=values (accept_unit_name),accept_unit_address=values (accept_unit_address),accept_unit_phone=values (accept_unit_phone),order_status=values (order_status),submission_date=values (submission_date),\
                    deal_time=values (deal_time),finish_time=values (finish_time),update_time=values (update_time),order_name=values (order_name),region_code=values (region_code)",insert_into_list)
    connect.commit()
    connect.close()
    cursor.close() 

if __name__ == "__main__":
    get_wfzy()
