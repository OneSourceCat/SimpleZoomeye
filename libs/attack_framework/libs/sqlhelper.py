#coding=utf-8
import MySQLdb
class DBHelper():


	def execute_ddl_sql(self,dbname,sql):
		conn = MySQLdb.connect(
			host='localhost',
			user='root',
			passwd='',
			port=3306,
			db=dbname)
		cursor = conn.cursor()
		try:
			res = cursor.execute(sql)
			conn.commit()
			cursor.close()
			conn.close()
			return res
		except Exception, e:
			print e
			conn.rollback()
			cursor.close()
			conn.close()
			return 0

	def execute_dql_sql(self,dbname,sql,mode='single'):
		conn = MySQLdb.connect(
			host='localhost',
			user='root',
			passwd='',
			port=3306,
			db=dbname)
		cursor = conn.cursor()
		try:
			cursor.execute(sql)
			if mode == 'single':
				res = cursor.fetchone()
				cursor.close()
				conn.close()
				return res
			else:
				res = cursor.fetchall()
				conn.close()
				return res
		except Exception, e:
			cursor.close()
			conn.close
			print e

if __name__ == '__main__':
	db = DBHelper()
	# res = db.execute_sql('test','select * from user',mode='all')
	# print res
	print db.execute_ddl_sql('test',"insert into user (username,password) values('shit233','shit')")




