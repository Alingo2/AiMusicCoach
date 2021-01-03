#逐一导入文件
import json
obj_r=open("./examples.json")
data=json.load(obj_r)
guitar_data=[]
for file_data in data.items():
    if file_data[1]['instrument_family']==3 and file_data[1]["instrument_source_str"]=="acoustic":
        guitar_data.append([file_data[1]['note_str'],file_data[1]['pitch']])
print(len(guitar_data))
#print(features)
