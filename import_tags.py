import mysql.connector
import logging
import time
from datetime import datetime
import xml.etree.ElementTree as et
from get_config import get_db_config
from DB_connect import connect_to_mysql

# define sql
add_tag = ("INSERT INTO otol_mst_tag_info "
           "(code, name, io_property, data_type, lower_limit, upper_limit, dcs_position, is_deleted, create_time) "
           "VALUES (%s, %s, 0, 1, -9999.99, 9999.99, %s, 0, %s)")

clear_table = ("TRUNCATE TABLE otol_mst_tag_info")

def read_tags(fname):
    with open(fname, 'r') as f:
        l_tags = [tag.strip() for tag in f]

    ret = l_tags
    return ret

def import_main(cnx, l_tags):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(clear_table)

            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            tag_infos = [(tag, tag, tag, date_time) for tag in l_tags]

            cursor.executemany(add_tag, tag_infos)
            cnx.commit()
            ret = f"Import success. {len(l_tags)} tags imported."

        return (0, ret)
    else:
        ret = "Database connection failed, please check database connection."
        return (1, ret)

def import_tags(fname):
    config = get_db_config("db_config.xml")
    cnx = connect_to_mysql(config, attempts=3)
    li_tags = read_tags(fname)
    result = import_main(cnx, li_tags)
    cnx.close()
    return result