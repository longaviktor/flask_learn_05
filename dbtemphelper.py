import psycopg2
import pandas as pd
from config import dbinfo2

DBI = dbinfo2()

conn = psycopg2.connect(host=DBI.dbhost(), port=DBI.dbport(), dbname=DBI.dbname(), user=DBI.dbuser(), password=DBI.dbpwd())
cursor=conn.cursor()

class DBtempHelper:
	def get_table(self):
		sqlquery="SELECT * FROM {} ORDER BY timedate DESC LIMIT 10;".format(DBI.dbutbl())
		df=pd.read_sql_query(sqlquery, conn)
		if not df.empty:
			df[df.columns[2]]=df[df.columns[2]].apply(lambda x: str(x)[0:19])
			return df.values
			
#	def add_user(self,email,salt,hashed):
#		MOCK_USERS.append({"email": email, "salt": salt, "hashed":hashed})
