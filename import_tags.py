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

file_handler = logging.FileHandler("mysql-log.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# define sql
add_tag = ("INSERT INTO otol_mst_tag_info "
           "(code, name, io_property, data_type, lower_limit, upper_limit, dcs_position, is_deleted, create_time) "
           "VALUES (%s, %s, 0, 1, -9999.99, 9999.99, %s, 0, %s)")

clear_table = ("TRUNCATE TABLE otol_mst_tag_info")


# get xml info
tree = et.parse('db_config.xml')
root = tree.getroot()

for info in root.findall('info'):
    ip = info.find('ip').text
    user = info.find('user').text
    password = info.find('password').text
    database = info.find('database').text

CONFIG = {
    'user' : user,
    'password' : password,
    'host' : ip,
    'database' : database,
    'raise_on_warnings' : True

}

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

def importTags(fname):

    cnx = connect_to_mysql(CONFIG, attempts=3)

    if cnx and cnx.is_connected():

        with cnx.cursor() as cursor:

            cursor.execute(clear_table)
            logger.info("Table cleared.")
            
            with open(fname, 'r') as f:
                tags = f.readlines()

            count = 0
            for tag in tags:
                tag = tag.strip()
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                tag_info = (tag, tag, tag, date_time)
                # print(tag_info)
                cursor.execute(add_tag, tag_info)
                count += 1

            f.close()
            cnx.commit()
            ret = f"Import success. {count} tags imported."

        return (cnx.close(), ret)
    else:
        ret = "Database connection failed, please check database connection."
        return (1, ret)
    
def readTagList(fname):
    ret_list = ""
    ret_count = 0

    with open(fname, 'r') as f:
        tags = f.readlines()

    for tag in tags:
        # tag = tag.strip()
        ret_list += tag
        ret_count += 1

    ret = (ret_list, ret_count)
    f.close()

    return ret

if __name__ == "__main__":
    importTags('tags.txt')