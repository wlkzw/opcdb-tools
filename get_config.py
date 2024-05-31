import xml.etree.ElementTree as et

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