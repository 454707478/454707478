import requests,json,datetime,time,math
from config import py_mysql
from logins import logins
session = requests.Session()

# 危废转移处理数据
def get_wfzycl():
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
                result_obj(header,index,post_data)
        else:
            pass
    else:
        page = math.ceil(resulte['data']['recordCount']/20)
        for index in range(1,page+1):
            time.sleep(3)
            result_obj(header,index,post_data)

def result_obj(header,index,post_data):
    info_url = "https://gfgl.meescc.cn/hlwjjg/tBasTranManifest/{}/20".format(index)
    response = session.post(info_url,headers=header,json=post_data).text
    resulte = json.loads(response)
    data_list = resulte["data"]["result"]
    connect, cursor = py_mysql()
    insert_into_list = []
    for data in data_list:
        id = data["pkId"]
        try:
            order_code = data["resPaperno"]
        except:
            order_code = ""
        order_name = ""
        process_unit = data["junitname"]
        process_user = data["jlinkman"]
        accopinions_dict = {
            "0": "接受",
            "1": "拒收",
            "2": "部分接受"
        }
        try:
            process_result = accopinions_dict[data["accopinions"]]
        except:
            process_result = ""
        try:
            process_time = data["receptiontime"]
        except:
            process_time = ""
        is_used = "1"
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tuples = (id,order_code,order_name,process_unit,process_user,process_result,process_time,is_used,times,times)
        print(tuples)
        insert_into_list.append(tuples)
    cursor.executemany("insert into t_haztrans_process_record(id,order_code,order_name,process_unit,process_user,process_result,process_time,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    on duplicate key update process_unit=values (process_unit),process_user=values (process_user),process_time=values (process_time),update_time=values (update_time)",insert_into_list)
    connect.commit()
    connect.close()
    cursor.close() 

if __name__ == "__main__":
    get_wfzycl()