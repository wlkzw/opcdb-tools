import re

regex = re.compile('[\(](.*?)[\)]')
insert_data = []
data_list = []
tag_list = []


with open("DATA.sql", 'r', encoding='utf-8') as f:
    sql_file = f.read()

    f.close()

commands = sql_file.split(';')

insert_commands = []
for command in commands:
    command = command.strip()
    if(command[:6] == "INSERT"):
        index = command.find("VALUES")
        insert_commands.append(command[index + 7 :])

for command in insert_commands:
    insert_data = regex.findall(command)

for data in insert_data:
    data_list.append(re.split('\,', data))

print(data_list)
