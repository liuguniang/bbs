

# msg_list = [
# 		{'id':1,'content':'xxx','parent_id':None},
# 		{'id':2,'content':'xxx','parent_id':None},
# 		{'id':3,'content':'xxx','parent_id':None},
# 		{'id':4,'content':'xxx','parent_id':1},
# 		{'id':5,'content':'xxx','parent_id':4},
# 		{'id':6,'content':'xxx','parent_id':2},
# 		{'id':7,'content':'xxx','parent_id':5},
# 		{'id':8,'content':'xxx','parent_id':3},
# 	]
#
# #效率太低
# # for i in msg_list:
# #     for j in msg_list:
# #         if i['id']==j['parent_id']:
# #             i['child']=[j,]
# # print(msg_list)
# #利用字典的哈希算法 快速查找的功能
# msg_list_dict={}
# for item in msg_list:
#     item['child']=[]
#     msg_list_dict[item['id']]=item
#
# #  msg_list_dict中的每一行都保存的是数据的内存地址，对msg_list_dict进行操作会实际上改变msg_list
# result=[]
# for item in msg_list:
#     pid=item['parent_id']
#     if pid:
#         msg_list_dict[pid]['child'].append(item)
#     else:
#         result.append(item)
#
# print(result)
# [{'content': 'xxx', 'parent_id': None, 'id': 1, 'child': [{'content': 'xxx', 'parent_id': 1, 'id': 4, 'child': [{'content': 'xxx', 'parent_id': 4, 'id': 5, 'child': [{'content': 'xxx', 'parent_id': 5, 'id': 7, 'child': []}]}]}]},
#  {'content': 'xxx', 'parent_id': None, 'id': 2, 'child': [{'content': 'xxx', 'parent_id': 2, 'id': 6, 'child': []}]},
#  {'content': 'xxx', 'parent_id': None, 'id': 3, 'child': [{'content': 'xxx', 'parent_id': 3, 'id': 8, 'child': []}]}]

# def test():
#     li=[]
#     for i in range(1,6):
#         for j in range(1,6):
#             for k in range(1,6):
#                 if i !=j and j!=k and i!=k:
#                     li.append((i,j,k,))
#     print(len(li))
#
# test()

# li=[(['{}*{}={}'.format(i,j,i*j,) for j in range(1,i+1)] )for i in range(1,10)]
# print(li)

# def test():
#     return (lambda x:i*x for i in range(4))
# print([m(2) for m in test()])

# data = (('a'),('b'),('c'),('d') )
# v = list(map(lambda x,y:{x:y},data[0:2],data[2:4]))
# print(v)

# a =dict(zip(('a','b'),(1,2)))
# print(a)
#
# def add_list(l=[]):
#     l.append('end')
#     return l
# print(add_list())
# print(add_list())
#
# print(type(eval('555')))
# bool((3,'',''))

# n=5
# print(-n)
#
# li=[3,5,7,7,8,2]
# l=sorted(set(li),key=li.index)
#
# val=[1,2,1,3]
# nums=set(val)
# def checkit(num):
#     if num in nums:
#         return True
#     else:
#         return False
# for i in filter(checkit,val):
#     print(i)
#
#
# n1=['a','b','c','d']
# n2=n1
# n3=n1[:]
# n2[0]='aa'
# n3[1]='bb'
# sum=0
# for i in (n1,n2,n3):
#     if i[0]=='aa':
#         sum+=1
#     if i[1]=='bb':
#         sum+=10
# print(sum)

num=[1,2,3,4]
num.append([5,6,7,8])
print(len(num))

def hatuff(param,*param2):
    print(param)
    print(type(param2))
hatuff('apple','bananas','cherry','datas')

d=lambda p:p*2
t=lambda p:p*3
x=2
x=d(x)
x=t(x)
x=d(x)
print(x)

#单例模式
from abc import abstractmethod,ABCMeta
class Singleton(object):
     def __new__(cls, *args, **kwargs):
         if not hasattr(cls,'_instance'):
             cls._instance=super(Singleton,cls).__new__()
         return cls._instance


#工厂模式
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self,money):
        pass

class Alipay(Payment):
    def pay(self,money):
        pass

class applepay(Payment):
    def pay(self,money):
        pass
class PaymentFactory:
    def  create_payment(self,method):
        if method=='Alipay':
            return Alipay()
        elif method=='applepay':
            return applepay()
        else:
            raise NameError(method)

f=PaymentFactory()
d=f.create_payment('applepay')
d.pay(100)
