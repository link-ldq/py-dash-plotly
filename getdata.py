import random;
import pymysql

def getData():
  # 建立连接
  db = pymysql.connect(host='127.0.0.1',
                      user='linktest',
                      password='054545',
                      database='linktest')                    
  # 使用 cursor() 方法创建一个游标对象 cursor
  cursor = db.cursor()

  # 使用 execute()  方法执行 SQL 查询 
  sql = '''SELECT * FROM dash''';
  # print(getSql(mock(ticks), sql))
  cursor.execute(sql);
  results = cursor.fetchall()
  res = []
  for row in results:
      num = row[0]
      time = row[1]
      # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t/1000)) 
       # 打印结果
      res.append({'num':num,'time':time})
  # print (data)
  # 关闭数据库连接
  db.close()
  return res;
# print(getData())
