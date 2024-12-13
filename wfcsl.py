import requests,json,datetime,uuid
from config import py_mysql
from logins import logins
session = requests.Session()

# 危废产生量数据
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
    cursor.execute("select enterprise_code,credit_code from t_hazardous_waste_enterprise")
    connect.commit()
    credit_info = cursor.fetchall()
    credit_dict = {}
    for credit_data in credit_info:
        credit_dict[credit_data[0]] = credit_data[1]
    info_url = "https://gfgl.meescc.cn/hlwjjg/basProduceDirectory/producePage/1/200"
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
    startdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    enddate = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    data = {"accountBoundManage": "accounManageView","areaCode": "411422","code": "","enddate": "2024-12-06","name": "",
            "personsname": "","personstel": "","roleFlag": "","startdate": "2024-12-01","sysSource": "","wasteType": ""}
    response = session.post(info_url,headers=header,json=data).text
    resulte = json.loads(response)
    if resulte["code"] == "100":
        code = logins()
        if code == "200":
            get_info()
        else:
            pass
    else:
        insert_into_list = []
        page_sum = resulte["data"]["recordCount"]
        for index in range(1,page_sum+1):
            info_url = "https://gfgl.meescc.cn/hlwjjg/basProduceDirectory/producePage/{}/200".format(index)
            data_list = resulte["data"]["result"]
            insert_into_list = []
            for data in data_list:
                print(data)
                id = str(uuid.uuid4()).replace("-","")
                enterprise_code = data["enterid"]
                enterprise_name = data["enterName"]
                credit_code = credit_dict[enterprise_code]
                waste_state = "1"
                category_code = data["wastecode"]
                category_name = data["waste"]
                data_time = data["createDate"]
                actual_weight = data["inboundnum"]
                is_used = "1"
                times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tuples = (id,enterprise_code,enterprise_name,data_time,credit_code,waste_state,category_code,category_name,actual_weight,is_used,times,times)
                print(tuples)
                insert_into_list.append(tuples)
        cursor.executemany("insert into t_waste_produce_dispose(id,enterprise_code,enterprise_name,data_time,credit_code,waste_state,category_code,category_name,actual_weight,is_used,create_time,update_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                        on duplicate key update category_code=values (category_code),category_name=values (category_name),actual_weight=values (actual_weight),update_time=values (update_time)",insert_into_list)
        connect.commit()
    connect.close()
    cursor.close()

if __name__ == "__main__":
    get_info()