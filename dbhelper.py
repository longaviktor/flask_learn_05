import psycopg2
import pandas as pd
from config import dbinfo

DBI = dbinfo()

conn = psycopg2.connect(host=DBI.dbhost(), port=DBI.dbport(), dbname=DBI.dbname(), user=DBI.dbuser(), password=DBI.dbpwd())
cursor=conn.cursor()

class DBHelper:
	def get_user(self,email):
		sqlquery="SELECT * FROM {} WHERE {} = %s;".format(DBI.dbutbl(),DBI.dbutbl_id())
		sqldata=(email,)
		cursor.execute(sqlquery, sqldata)
		df=pd.DataFrame(cursor.fetchall())
		if not df.empty:
			return {"email": df.loc[0][0], "salt": df.loc[0][1], "hashed" : df.loc[0][2]}
			
#	def add_user(self,email,salt,hashed):
#		MOCK_USERS.append({"email": email, "salt": salt, "hashed":hashed})
