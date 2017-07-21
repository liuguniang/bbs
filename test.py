

msg_list = [
		{'id':1,'content':'xxx','parent_id':None},
		{'id':2,'content':'xxx','parent_id':None},
		{'id':3,'content':'xxx','parent_id':None},
		{'id':4,'content':'xxx','parent_id':1},
		{'id':5,'content':'xxx','parent_id':4},
		{'id':6,'content':'xxx','parent_id':2},
		{'id':7,'content':'xxx','parent_id':5},
		{'id':8,'content':'xxx','parent_id':3},
	]

#效率太低
# for i in msg_list:
#     for j in msg_list:
#         if i['id']==j['parent_id']:
#             i['child']=[j,]
# print(msg_list)
#利用字典的哈希算法 快速查找的功能
msg_list_dict={}
for item in msg_list:
    item['child']=[]
    msg_list_dict[item['id']]=item

#  msg_list_dict中的每一行都保存的是数据的内存地址，对msg_list_dict进行操作会实际上改变msg_list
result=[]
for item in msg_list:
    pid=item['parent_id']
    if pid:
        msg_list_dict[pid]['child'].append(item)
    else:
        result.append(item)

print(result)
# [{'content': 'xxx', 'parent_id': None, 'id': 1, 'child': [{'content': 'xxx', 'parent_id': 1, 'id': 4, 'child': [{'content': 'xxx', 'parent_id': 4, 'id': 5, 'child': [{'content': 'xxx', 'parent_id': 5, 'id': 7, 'child': []}]}]}]},
#  {'content': 'xxx', 'parent_id': None, 'id': 2, 'child': [{'content': 'xxx', 'parent_id': 2, 'id': 6, 'child': []}]},
#  {'content': 'xxx', 'parent_id': None, 'id': 3, 'child': [{'content': 'xxx', 'parent_id': 3, 'id': 8, 'child': []}]}]