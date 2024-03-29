import re
import pandas as pd

regex = re.compile('[\(](.*?)[\)]')

l_insertCommands = []
l_regex = []
l_timestamps = []
d_data = {
    "timestamp" : [],
          }

def sql2csv(fname):

    with open(fname, 'r', encoding='utf-8') as f:
        sql_file = f.read()
        f.close()

    commands = sql_file.split(';')

    for command in commands:
        command = command.strip()
        if (command[:6] == "INSERT"):
            index = command.find("VALUES")
            l_insertCommands.append(command[index + 7 :])

    join_command = ','.join(l_insertCommands)

    l_regex = regex.findall(join_command)

    for i in range(len(l_regex)):
        l_regex[i] = l_regex[i].split(',')

    for item in l_regex:
        tag = item[2].strip("'")
        ts = item[-1].strip("'")
        val = item[4].strip("'")
        
        if (ts not in d_data["timestamp"]):
            d_data["timestamp"].append(ts)
        
        if (tag not in d_data):
            d_data.update({tag : [val]})
        else:
            d_data[tag].append(val)

    df = pd.DataFrame(d_data)

    df.to_csv("data.csv")
    
    return f"{fname} successfully converted to data.csv."

if __name__ == "__main__":
    sql2csv("DATA.sql")