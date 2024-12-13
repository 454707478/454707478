import pymysql

# def py_mysql():
#     connect = pymysql.connect(
#         host="172.168.140.17",
#         user="root",
#         password="Hzf2018!@",
#         port=7001,
#         database="zhhb_hazwaste"
#     )
#     cursor = connect.cursor()
#     return connect, cursor

# def py_mysqls():
#     connect = pymysql.connect(
#         host="172.168.140.17",
#         user="root",
#         password="Hzf2018!@",
#         port=7001,
#         database="zhhb_base_merge"
#     )
#     cursor = connect.cursor()
#     return connect, cursor


def py_mysql():
    connect = pymysql.connect(
        host="192.168.1.10",
        user="root",
        password="Hzf2018!@",
        port=7001,
        database="zhhb_hazwaste"
    )
    cursor = connect.cursor()
    return connect, cursor

def py_mysqls():
    connect = pymysql.connect(
        host="192.168.1.10",
        user="root",
        password="Hzf2018!@",
        port=7001,
        database="zhhb_base_merge"
    )
    cursor = connect.cursor()
    return connect, cursor


qylx_type_dict = {
    "sfwfcsy":"危废单位,",  
    "sfyfcsy":"医疗单位,",
    "sfybgycsy":"一般固废单位,",
    "sfwfjy":"经营单位,",
    "sfwfys":"运输单位,",
    "sfwswncsy":"污水污泥单位,",
    "sfsjqy":"试点单位,",
    "sfdcjzzyd":"暂存库/集中转运点,",
    "sfwkk":"尾矿库企业,",
    "sfdzfwcjqy":"电子废物拆解企业,"
}