
import mysql.connector
import re
def FileToList(fname):
    toreturn = []
    with open(fname,"r") as file:
        for line in file:
            toreturn.append(line.strip())


    function = {}

    for x in toreturn:
        parts = x.split('=',1)
        function[parts[0]] = parts[1]
    return function


def check_variable(function):
    variableToInput = {}
    conn = mysql.connector.connect(
        host = "host",
        user = "username",
        password = "password",
        database = "databse"
    )
    cursor = conn.cursor()
    for name in function:
        for variable in name:
            query = "SELECT * FROM your_table WHERE name = %"
            cursor.execute(query,(name,))

            result = cursor.fetchone()

            if result == False:
                variableToInput[variable] = ''
    cursor.close()
    conn.close()
    return variableToInput


def Insert_formulaToDB(function):
    conn = mysql.connector.connect(
        host = "10.0.0.164",
        user = "root",
        password = "123456",
        database = "soft_analyzer"
    )
    id = 1
    cursor = conn.cursor()
    sql = "DELETE FROM soft_analyzer.formula"
    cursor.execute(sql)
    conn.commit()
    sql = "INSERT INTO soft_analyzer.formula (id,left_side,right_side) VALUES(%s,%s,%s)"
    for name in function:

        if function[name] != '':
            v = (id,name,function[name])
            id+=1
            cursor.execute(sql,v)
            conn.commit()

    cursor.close()
    conn.close()

def Insert_variableToDB(variableToInsert):
    sql = "INSERT INTO soft_analyzer.formula (id,name,io,tag,value) VALUES(%s,%s,%s,%s,%s)"
    conn = mysql.connector.connect(
        host = "10.0.0.164",
        user = "root",
        password = "123456",
        database = "soft_analyzer"
    )
    cursor = conn.cursor()
    for name in variableToInsert:
         for value in name:
            if value != '':
                v = (name,value)
                cursor.execute(sql,v)
                conn.commit()

    cursor.close()
    conn.close()

