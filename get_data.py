import mysql.connector
import logging
import time
from datetime import datetime
import xml.etree.ElementTree as et

# define logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler("import_tags_log.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_db_config(xml_file):
    tree = et.parse(xml_file)
    root = tree.getroot()

    for info in root.findall('info'):
        ip = info.find('ip').text
        user = info.find('user').text
        password = info.find('password').text
        database = info.find('database').text

    config = {
        'user' : user,
        'password' : password,
        'host' : ip,
        'database' : database,
        'raise_on_warnings' : True
    }

    return config

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    while attempt < attempts + 1:
        try:
            success = mysql.connector.connect(**config)
            logger.info("Database connected.")
            return success
        except (mysql.connector.Error, IOError) as err:
            if(attempts is attempt):
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err, attempt, attempts,
            )
            time.sleep(delay ** attempt)
            attempt += 1
    
    return None

def get_all(cnx, l_tags):
    sql = ("SELECT tag_code, value, create_time FROM tag_data_received "
       "WHERE tag_code = %s")
    length = len(l_tags)
    for i in range(length - 1):
        sql = sql + " OR tag_code = %s"

    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql, l_tags)
            data= cursor.fetchall()
            return data
        
def get_last(cnx, tag):
    sql = ("SELECT tag_code, value, create_time FROM tag_data_received "
       "WHERE tag_code = %s "
       "ORDER BY id DESC LIMIT 1")

    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql, tag)
            data = cursor.fetchall()
            return data

def get_last_time(cnx, tag):
    sql = ("SELECT tag_code, value, dcs_collect_time FROM tag_data_received "
       "WHERE tag_code = %s "
       "ORDER BY dcs_collect_time DESC LIMIT 1")

    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql, tag)
            data = cursor.fetchall()
            return data
        
def get_data(cnx, tag, start_time, end_time):
    sql = ("SELECT tag_code, value, create_time FROM tag_data_received "
       "WHERE tag_code = %s AND create_time BETWEEN %s AND %s")
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql, (tag, start_time, end_time))
            data = cursor.fetchall()
            return data

def get_all_tag(cnx):
    sql = ("SELECT code FROM otol_mst_tag_info")

    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql)
            data= cursor.fetchall()
    all_tags = []

    for tags in data:
        all_tags.append(tags[0])
    return all_tags

def modify_tagValue(cnx,new_val,tag_code):
    sql = ("UPDATE tag_data_received SET value = %s WHERE tag_code = %s"
       )
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(sql,(new_val,tag_code))
        cnx.commit()

if __name__ == "__main__":
    config = get_db_config("db_config.xml")
    cnx = connect_to_mysql(config)
    tags = ["PID001"]
    # modify_tagValue(cnx,5,'3FIC104OD')
    # data = get_all(cnx, tags)
    # print(data)
    data = get_last(cnx, [tags[0]])
    print(data)
    # data = get_data(cnx, tags[0], datetime(2024, 4, 11, 22, 55, 11), datetime(2024, 4, 11, 22, 55, 11))
    # print(data)
    # data = get_all_tag(cnx)
    # print(data)
    cnx.close()