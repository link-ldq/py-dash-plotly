import random;
import time  # 引入time模块

import pymysql

# config;
LENGTH = 10000;
LIMIT_MIN = 0;
LIMIT_MAX = 1000;
HOUR = 1000 * 60 * 60;
DAY = HOUR * 24;
# 时间戳
ticks = int(time.time() * 1000) - 365 * DAY;

# 时间转换
def getTime(t):
  return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t/1000))

# mock 数据 「时间戳|值」
def mock(t):
  # mock 数据
  list = [];
  for item in range(LENGTH):
    t+= HOUR;
    value = {'num':random.randint(LIMIT_MIN,LIMIT_MAX),'time':(t)}
    list.append(value);
  return list

# print(mock(ticks));
# 建立连接
db = pymysql.connect(host='127.0.0.1',
                     user='linktest',
                     password='054545',
                     database='linktest')                    
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# SQL 插入语句
for item in mock(ticks):
  strt = item['time']
  num = str(item['num'])
  print(num, strt)
  cursor.execute('insert into dash values( %s,  %s)' % \
             (num,strt))
  db.commit()
  amount = cursor.fetchall()

# 使用 execute()  方法执行 SQL 查询 
sql = '''SELECT * FROM dash''';
# print(getSql(mock(ticks), sql))
cursor.execute(sql);
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

print (data)
 
# 关闭数据库连接
db.close()