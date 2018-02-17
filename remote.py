from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from flask import request 
from flask import redirect
from flask import url_for

#from mockdbhelper import MockDBHelper as DBHelper
from dbhelper import DBHelper
from dbtemphelper import DBtempHelper
from user import User

from passwordhelper import PasswordHelper

from dashboardhelper import wol,ping,poweroff,reboot,testssh,local

DB=DBHelper()
DB2=DBtempHelper()
PH = PasswordHelper()

app = Flask (__name__)
login_manager = LoginManager(app)

app.secret_key = 'PD9QU1XyH8eokp4FDV+pvUZjZH5ICMM/cJKtggffP9yQFOq3O8Y1zRT7Go1pUytMbfxbCLqZByQKfbmoTrmp+Mefp1QP10InXsA'

##GLOBAL
###################################
restart_apache=0

####################################

@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

@app.route("/")
def home():
	return render_template("home.html")

if __name__ == '__main__':
	app.run(port=5000, debug=True)

@app.route("/login", methods=["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	stored_user = DB.get_user(email)
	if stored_user and PH.validate_password(password,stored_user['salt'],stored_user['hashed']):
		user = User(email)
		login_user(user,remember=True)
		return redirect(url_for('dashboard'))
	return home()

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/register", methods=["POST"])
def register():
	email = request.form.get("email")
	pw1 = request.form.get("password")
	pw2 = request.form.get("password2")
	if not pw1 == pw2:
		return redirect(url_for("home"))
	if DB.get_user(email):
		return redirect(url_for('home'))
	salt = PH.get_salt()
	hashed = PH.get_hash(pw1 + salt)
	DB.add_user(email,salt,hashed)
	return redirect(url_for('registration'))


@app.route("/shome")
@login_required
def shome():
	table = DB2.get_table()
	return render_template("shome.html", table = table)

@app.route("/kodi")
@login_required
def account():
	return render_template("kodi.html")

@app.route("/registration")
@login_required
def registration():
	return render_template("registration.html")

#DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
	global restart_apache
	status1_1 = ping().ping_1()
	status1_2 = testssh().testssh_1()
	#Local restart apache
	if restart_apache==1:
		restart_apache=0
		local().reapache()
	return render_template("dashboard.html",status1_1=status1_1,status1_2=status1_2)

##Storage server
##################################x
@app.route("/wol_1")
@login_required
def wol_1():
	wol().wol_1()
	return redirect("/dashboard")

@app.route("/poff_1")
@login_required
def poff_1():
	poweroff().poweroff_1()
	return redirect("/dashboard")

@app.route("/rboot_1")
@login_required
def rboot_1():
	reboot().reboot_1()
	return redirect("/dashboard")

##Local
###################################
@app.route("/localoff")
@login_required
def localoff():
	local().poweroff()
	return redirect("/dashboard")

@app.route("/localreboot")
@login_required
def localreboot():
	local().reboot()
	return redirect("/dashboard")

@app.route("/localreapache")
@login_required
def localreapache():
	global restart_apache
	restart_apache=1
	return redirect("/dashboard")
	

