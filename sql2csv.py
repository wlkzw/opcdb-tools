import re
import pandas as pd
from collections import defaultdict, OrderedDict

regex = re.compile('[\(](.*?)[\)]')
li_regex = []
li_timestamps = []
dict_data = {
    "timestamp" : [],
          }

# read SQL file
def read_sql_file(fname, la_message):
    la_message.setText(la_message.text() + "\nReading SQL file...")
    with open(fname, 'r', encoding='utf-8') as f:
        sql_file = f.read()
    return sql_file

# get all INSERT commands from SQL file
# return a list of INSERT commands' VALUES
def get_insert_commands(sql_file, la_message):
    la_message.setText(la_message.text() + "\nGetting INSERT commands...")
    commands = sql_file.split(';')
    li_insertCommands = []
    for command in commands:
        command = command.strip()
        if (command[:6] == "INSERT"):
            index = command.find("VALUES")
            li_insertCommands.append(command[index + 7 :])
    return li_insertCommands

# get every value in the list of INSERT commands' VALUES using regular expression
def process_commands(li_insertCommands, la_message):
    la_message.setText(la_message.text() + "\nProcessing INSERT commands...")
    join_command = ','.join(li_insertCommands)
    li_regex = regex.findall(join_command)
    for i in range(len(li_regex)):
        li_regex[i] = li_regex[i].split(',')
    return li_regex

# check every item in values list
# seperate tag, timestamp, and value
# update progress bar as loop executes
def process_items(li_regex, pbar, la_message):
    la_message.setText(la_message.text() + "\nProcessing items...")
    dict_data = defaultdict(OrderedDict)
    # defaultdict is used to avoid KeyError 
    # (no need to check if key exists in dictionary)

    for i, item in enumerate(li_regex):
        tag = item[2].strip("'")
        ts = item[-1].strip("'")
        ts = ts[:-2] + "00"
        val = item[4].strip("'")
        
        dict_data[tag][ts] = val

        pbar.setValue(int((i + 1) / len(li_regex) * 100))

    return dict_data

# FOR DEBUGGING: get length of every key-pointed array in data dictionary

# def print_data(d_data, l_message):
#     l_message.setText(l_message.text() + "\nPrinting data array length...")
#     for key, value in d_data.items():
#         print(f"'{key}' : '{len(value)}'")

# convert dictionary to pandas dataframe
def convert_to_csv(dict_data, la_message):
    la_message.setText(la_message.text() + "\nConverting data to CSV...")
    
    # Convert each inner dictionary to a Series
    dict_data = {key: pd.Series(value) for key, value in dict_data.items()}
    
    # Convert dict_data to a DataFrame
    df = pd.DataFrame(dict_data)
    
    # Save DataFrame to a CSV file
    df.to_csv("data.csv")

def sql2csv(fname, pbar, la_message):
    sql_file = read_sql_file(fname, la_message)
    li_insertCommands = get_insert_commands(sql_file, la_message)
    li_regex = process_commands(li_insertCommands, la_message)
    dict_data = process_items(li_regex, pbar, la_message)

    # print_data(dict_data, la_message)

    convert_to_csv(dict_data, la_message)
    la_message.setText(la_message.text() + "\n" + f"{fname} successfully converted to data.csv.")
