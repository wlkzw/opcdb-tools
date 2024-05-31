# import random
# import time
from get_config import get_db_config
from DB_connect import connect_to_mysql

def write(cnx, data):
    sql = ("INSERT INTO tag_data_send "
           "(tag_id, tag_code, data_type, value, todo_time, result, create_time, update_time) "
       "VALUES (5, %s, 1, %s, NOW(), 0, NOW() + 10, NOW())")
    
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.executemany(sql, data)
            cnx.commit()

# if __name__ == "__main__":
#     config = get_db_config("db_config.xml")
#     cnx = connect_to_mysql(config)
#     count = 0
#     while True:
#         data = [("write_test.float", round(random.uniform(0, 100), 2))]
#         write(cnx, data)
#         time.sleep(60)
#     cnx.close()