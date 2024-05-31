import mysql.connector
import logging
import time
from datetime import datetime
import xml.etree.ElementTree as et
import random
import string

import schedule
import time

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

def insert_tagValue(cnx,id, tag_code, io_property, value_status, dcs_collect_time, create_time):
    sql = ("INSERT INTO tag_data_received (tag_id, tag_code, io_property, value, value_status, dcs_collect_time, create_time)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
       )
    tag_id = 1
    for tag in (tag_code):
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                random_value = random.uniform(0, 100)
                cursor.execute(sql,(tag_id, tag, io_property, random_value, value_status, dcs_collect_time, create_time))
                tag_id += 1
            cnx.commit()

if __name__ == "__main__":
    config = get_db_config("db_config.xml")
    cnx = connect_to_mysql(config)

    characters = string.ascii_letters + string.digits

    random_tags = ['PID001','PID002','PID003','PID004','PID005','PID006','PID007','PID008','PID009','PID010','PID011']

    id = 0


    while True:
        
        insert_tagValue(cnx,id,random_tags , 0, 1, datetime.now().replace(microsecond=0) ,datetime.now().replace(microsecond=0) )
        id+=11
        print(f"--- {datetime.now().replace(microsecond=0)} --- Values received.")
        time.sleep(60)
    