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

# define sql
add_tag = ("INSERT INTO otol_mst_tag_info "
           "(code, name, io_property, data_type, lower_limit, upper_limit, dcs_position, is_deleted, create_time) "
           "VALUES (%s, %s, 0, 1, -9999.99, 9999.99, %s, 0, %s)")

clear_table = ("TRUNCATE TABLE otol_mst_tag_info")

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

def read_tags(fname):
    with open(fname, 'r') as f:
        l_tags = [tag.strip() for tag in f]

    ret = l_tags
    logger.info("Tag infomation retrieved.")
    return ret

def import_main(cnx, l_tags):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(clear_table)
            logger.info("Table cleared.")

            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            tag_infos = [(tag, tag, tag, date_time) for tag in l_tags]

            cursor.executemany(add_tag, tag_infos)
            cnx.commit()
            ret = f"Import success. {len(l_tags)} tags imported."
            logger.info(ret)

        return (0, ret)
    else:
        ret = "Database connection failed, please check database connection."
        logger.info(ret)
        return (1, ret)

def import_tags(fname):
    config = get_db_config("db_config.xml")
    cnx = connect_to_mysql(config, attempts=3)
    li_tags = read_tags(fname)
    result = import_main(cnx, li_tags)
    cnx.close()
    return result