import mysql.connector
import logging
import time

# define logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler("./logs/log_mysql.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    while attempt < attempts + 1:
        try:
            cnx = mysql.connector.connect(**config)
            logger.info("Database connected.")
            return cnx
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