
import mysql.connector
import xml.etree.ElementTree as et
from get_data import get_all_tag,get_last_time
import copy
import math
import re
from data_preparation import FileToList
class claculation_f:
    def __init__(self,main_window):

        self.main_window = main_window
        self.valueTable = {}
        self.functionTable = {}
        self.config = self.get_db_config("db_config.xml")
        self.cnx = self.connect_to_mysql(self.config)
        self.allTags = get_all_tag(self.cnx)
       
        self.conn = mysql.connector.connect(
        host = "10.0.0.164",
        user = "root",
        password = "123456",
        database = "soft_analyzer"
        )
        self.cursor = self.conn.cursor()

       
        



    def get_db_config(self,xml_file):
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
    
    def connect_to_mysql(self,config, attempts=3, delay=2):
        attempt = 1
        while attempt < attempts + 1:
            try:
                success = mysql.connector.connect(**config)
                self.main_window.print_message("Database connected")
                return success
            except (mysql.connector.Error, IOError) as err:
                if(attempts is attempt):
                    self.main_window.print_message("Failed to connect, exiting without a connection: %s", err)
                    return None
                attempt += 1
    
        return None
    
    def connect_to_mysql1(self,config, attempts=3, delay=2):
        attempt = 1
        while attempt < attempts + 1:
            try:
                success = mysql.connector.connect(**config)
                return success
            except (mysql.connector.Error, IOError) as err:
                if(attempts is attempt):
                    self.main_window.print_message("Failed to connect, exiting without a connection: %s", err)
                    return None
                attempt += 1
    
        return None
    
    def extractFunction_fromDB(self):
        self.valueTable = {}
        self.functionTable = {}
        sql = "SELECT left_side,right_side FROM soft_analyzer.formula"

        self.cursor.execute(sql)

        for row in self.cursor:

            name,function = row
        
            
            if function[0] == '@' and function[1] =='I':
                if '==' in function:
                    res = function.replace('==','/==/')
                elif '<=' in function:
                    res = function.replace('<=','/<=/')
                elif '<' in function:
                    res = function.replace('<','/</')
                elif '>=' in function:
                    res = function.replace('>=','/>=/')
                elif '>' in function:
                    res = function.replace('>','/>/')
                
                res = re.split(r'[,/()@]',res)
                res = [x for x in res if x != '']

            elif function[0] == '@' and function[1] =='M':
                res = re.split(r'[,()@]',function)
                res = [x for x in res if x != '']
                
            else:
                op="+-*)/("
                res=""
                for i in function:
                    if i in op:
                        res += "@" + i +"@"
                    elif i !=' ' and i != '(' and i != ')':
                        res += i
                res = res.split("@")
            self.functionTable[name] = res


    
    def doCal_byName(self,name):
        sql = "INSERT INTO soft_analyzer.variables (id,name,io,tag,value) VALUES(%s,%s,%s,%s,%s)"
        id = 0
        tag = ''
        time = None
        function = self.functionTable[name]
        op="+-*)/("
        res = copy.copy(function)
        if 'log' in function:
            index = 0
            log_op = False
            if res[0] == 'log':
                res[0] = ''
                res[1] = ''
                index = 2
                log_op = True
            while index < len(res):
                    term = str(copy.copy(res[index]))
                    if log_op == True:
                        log = []
                        while log_op:
                            term = str(copy.copy(res[index]))
                            if term == ')':
                                res[index] = ''
                                log_op = False
                            elif term not in op:
                                
                                res[index] = ''
                                if self.check_if_is_number(term) == True:
                                    log.append(term)
                                
                                elif term in self.allTags:
                                    tags = [term]
                                    tag = term
                                    log.append(get_last_time(self.cnx, [tags[0]])[0][1])
                                    time = get_last_time(self.cnx, [tags[0]])[0][2]
                                else:
                                    res[index] = ''
                                    v  = self.valueTable[term]
                                    log.append(v)
                            elif term in op:
                                res[index] = ''
                                log.append(term)
                            
                            index += 1
                        
                        log_with_value = "".join([str(item) for item in log])
                        log_val = math.log(eval(log_with_value),10)
                        res[index] = log_val
                    
                    elif term != 'log' and term not in op:
                        if self.check_if_is_number(term):
                            res[index] = term
                        elif term in self.allTags:
                            tags = [term]
                            tag = term
                            res[index] = get_last_time(self.cnx, [tags[0]])[0][1]
                            time = get_last_time(self.cnx, [tags[0]])[0][2]
                        else:
                            res[index] = self.valueTable[term]
                        index += 1

                    elif term == 'log':
                        res[index] = ''
                        res[index+1] = ''
                        index += 2
                        log_op = True
                    else:
                        index += 1
            function_with_value = "".join([str(item) for item in res])
        
        
            value = eval(function_with_value)
            self.valueTable[name] = value
            v = (id,name,0,tag,value)
            id+=1

            self.cursor.execute(sql,v)
            self.conn.commit()
        

        elif 'IF' in function:
            for index,term in enumerate(function):
                if self.check_if_is_number(term) == False and term != '>' and term != '<' and term != '==' and term != 'IF' and term != '<=' and term != '>=':
                    
                    if '*' in term or '+' in term or '-' in term or '/' in term:
                        
                        op="+-*)/("
                        res1=""
                        for i in term:
                            if i in op:
                                res1 += "@" + i +"@"
                            elif i !=' ' and i != '(' and i != ')':
                                res1 += i
                        res1 = res1.split("@")

                        for index1,term1 in enumerate(res1):
                            if self.check_if_is_number(term1) == False and term1 not in op:

                                if term1 in self.allTags:
                        
                                    tags = [term1]
                                    tag = term1
                                    res1[index1] = get_last_time(self.cnx, [tags[0]])[0][1]
                                    time = get_last_time(self.cnx, [tags[0]])[0][2]
                                else:
                                    res1[index1] = self.valueTable[term1]

                            elif self.check_if_is_number(term1):
                                res1[index1] = term1
                        function_with_value = "".join([str(item) for item in res1])
                        value = eval(function_with_value)
                        res[index] = value
                    elif term in self.allTags:
                            tags = [term]
                            tag = term
                            res[index] = float(get_last_time(self.cnx, [tags[0]])[0][1])
                            time = get_last_time(self.cnx, [tags[0]])[0][2]
                    else:
                        res[index] = self.valueTable[term]
                elif self.check_if_is_number(term) == True and term != '>' and term != '<' and term != '==' and term != 'IF' and term != '<=' and term != '>=':
                    res[index] = float(term)
            result = 0
            if res[2] == '<':
                if(res[1] < res[3]):
                    result = res[-2]
                else:
                    result = res[-1]
            elif res[2] == '>':
                if(res[1] > res[3]):
                    result = res[-2]
                else:
                    result = res[-1]
            elif res[2] == '>=':
                if(res[1] >= res[3]):
                    result = res[-2]
                else:
                    result = res[-1]
            elif res[2] == '<=' :
                if(res[1] <= res[3]):
                    result = res[-2]
                else:
                    result = res[-1]      

            self.valueTable[name] = result   
            value = result
            v = (id,name,0,tag,value)
            id+=1
            self.cursor.execute(sql,v)
            self.conn.commit()
        elif 'MAX' in function or 'MIN' in function:
            for index,term in enumerate(function):
                if self.check_if_is_number(term) == False and term != 'MAX' and term!='MIN':
                    if '*' in term or '+' in term or '-' in term or '/' in term:
                        
                        op="+-*)/("
                        res1=""
                        for i in term:
                            if i in op:
                                res1 += "@" + i +"@"
                            elif i !=' ' and i != '(' and i != ')':
                                res1 += i
                        res1 = res1.split("@")

                        for index1,term1 in enumerate(res1):
                            if self.check_if_is_number(term1) == False and term1 not in op:

                                if term1 in self.allTags:
                        
                                    tags = [term1]
                                    tag = term1
                                    res1[index1] = get_last_time(self.cnx, [tags[0]])[0][1]
                                    time = get_last_time(self.cnx, [tags[0]])[0][2]
                                else:
                                    res1[index1] = self.valueTable[term1]

                            elif self.check_if_is_number(term1):
                                res1[index1] = term1
                        function_with_value = "".join([str(item) for item in res1])
                        value = eval(function_with_value)
                        res[index] = value
                    elif term in self.allTags:
                            tags = [term]
                            tag = term
                            res[index] = float(get_last_time(self.cnx, [tags[0]])[0][1])
                            time = get_last_time(self.cnx, [tags[0]])[0][2]
                    else:

                        res[index] = self.valueTable[term]
                elif self.check_if_is_number(term) == True and term != 'MAX' and term!='MIN':
                    res[index] = float(term)
            result = 0
            if function[0] == 'MAX':
                result = max(res[1:])
            else:
                result = min(res[1:])     

            self.valueTable[name] = result   
            value = result
            v = (id,name,0,tag,value)
            id+=1
            self.cursor.execute(sql,v)
            self.conn.commit()
        else:

            for index,term in enumerate(function):
                if self.check_if_is_number(term) == False and term not in op:

                    if term in self.allTags:
                        
                        tags = [term]
                        tag = term
                        res[index] = get_last_time(self.cnx, [tags[0]])[0][1]
                        time = get_last_time(self.cnx, [tags[0]])[0][2]
                    else:
                        res[index] = self.valueTable[term]

                elif self.check_if_is_number(term):
                    res[index] = term
            function_with_value = "".join([str(item) for item in res])
            
            
            value = eval(function_with_value)
            self.valueTable[name] = value
            v = (id,name,0,tag,value)
            id+=1
            self.cursor.execute(sql,v)
            self.conn.commit()

        
        return time
        
    
    def doCal_all(self):
        time = []
        for name in self.functionTable:
            time.append(self.doCal_byName(name))
        return time
    def check_if_is_number(self,number):
        try:
            float(number)
            return True
        except:
            return False
    def turn_offCursor(self):
        self.cursor.close()
        self.conn.close()
#c = claculation_f()
#c.extractFunction_fromDB()
#c.doCal_all()
#c.turn_offCursor()
#print(c.valueTable)
#print(c.functionTable)