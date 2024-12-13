import requests,json,datetime,time,math
from config import py_mysql
from logins import logins
session = requests.Session()

# 危废转移转运数据
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
        transport_code = data["planno"]
        license_plate = data["platenumbe"]
        driver_name = data["drivername"] 
        departure_time = data["starttime"]
        try:
            arrival_time = data["arrivetime"]
        except:
            arrival_time = ""
        transport_start_time = departure_time
        transport_arrival_time = arrival_time
        transport_start_weight = data["tranOutSum"]
        try:
            transport_arrival_weight = data["receptionmassSum"]
        except:
            transport_arrival_weight = None
        transport_status = data["status"]
        is_used = "1"
        times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tuples = (id,order_code,transport_code,license_plate,driver_name,departure_time,arrival_time,transport_start_time,transport_arrival_time,
                  transport_start_weight,transport_arrival_weight,transport_status,is_used,times,times)
        print(tuples)
        insert_into_list.append(tuples)
    cursor.executemany("insert into t_haztrans_transport_record(id,order_code,transport_code,license_plate,driver_name,departure_time,arrival_time,transport_start_time,transport_arrival_time,\
                    transport_start_weight,transport_arrival_weight,transport_status,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    on duplicate key update driver_name=values (driver_name),departure_time=values (departure_time),arrival_time=values (arrival_time),transport_start_time=values (transport_start_time),\
                    transport_arrival_time=values (transport_arrival_time),transport_start_weight=values (transport_start_weight),transport_arrival_weight=values (transport_arrival_weight),update_time=values (update_time)",insert_into_list)
    connect.commit()
    connect.close()
    cursor.close() 

if __name__ == "__main__":
    get_wfjyxk()