#建立数据库连接
import pymysql
import re
#识别敏感数据的函数
def sensitive_data_identification(data):
    sensitive_field_rules = [  # 利用正则表达式
        r'(\d{18}|\d{17}[Xx])',  # 匹配身份证号码
        r'^[0-9a-zA-Z]{8,16}$',  # 匹配密码（8-16位数字或字母）
        r'^[1-9]\d{5}$',  # 匹配邮编（6位数字）
        r'^(\d{16}|\d{19})$',  # 匹配银行卡号码（16位或19位数字）
        r'(\d{11})',  # 匹配电话号码（11位数字）
        r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',  # 匹配邮箱地址
    ]#敏感规则
    # 循环识别
    sensitive_fields = []
    for row_index,row in enumerate(data):
        for column_index,value in enumerate(row):
            for rule in sensitive_field_rules:
                if re.match(rule, str(value)):#匹配数值
                    sensitive_fields.append((row_index, column_index))
                    break
    return sensitive_fields
#设置脱敏值
def desensitive_value(value):
    str_value=str(value)
    value_length=len(str_value)
    #计算脱敏部分长度
    desensitized_length=value_length//2
    star_position=(value_length-desensitized_length)//2
    end_position=star_position+desensitized_length
    desensitized_value=(
        str_value[:star_position]+'*'* desensitized_length+str_value[end_position:]
    )
    return desensitized_value
#动态脱敏
def desensitized_string(data,sensitive_fields):
    desensitized_data=[]
    for row_index,row in enumerate(data):#enumerate(data)返回元素的索引和值
        desensitized_row=[]
        for column_index,value in enumerate(row):
            if(row_index , column_index) in sensitive_fields:
                desensitized_value=desensitive_value(value)
                desensitized_row.append(desensitized_value)
            else:
                desensitized_row.append(value)
        desensitized_data.append(desensitized_row)
    return desensitized_data

db=pymysql.connect(host='localhost',user='root',passwd='rnm54088',db='challenges')
#创建游标,可以用来执行sql命令
cursor=db.cursor()
sql="SELECT*FROM userinfo_dynamic"
cursor.execute(sql)
result=cursor.fetchall()#获取查询结果‘
for row in result:#遍历打印每一行
    print(row)
sensitive_fields=sensitive_data_identification(result)#识别敏感数据
print("\n检测到的敏感数据:")
for row in sensitive_fields:
    print(row)
desensitized_data = desensitized_string(result, sensitive_fields)#数据脱敏
result=desensitized_data
print('\n脱敏后的数据查询结果:')
for row in result:
    print(row)
cursor.close()
db.close()



