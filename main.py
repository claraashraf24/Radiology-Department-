from warnings import resetwarnings
from flask import Flask, render_template, request, redirect, flash, url_for
from flask.templating import render_template
import mysql.connector
from functools import wraps
import pandas as pd
import numpy as np
from scanassgn import scanassign
import re

isLoggedIn=False
typeL=''
currentuser=''
mydb = mysql.connector.connect(
	host = 'localhost',
	username = 'root',
	passwd = '@Hm$d_2001',
	database = 'radiology')
mycursor = mydb.cursor(buffered =True)

app=Flask(__name__)
app.config['SECRET_KEY'] = '54aaacc75d53041c924e22910015ddda'

@app.route('/', methods = ['POST', 'GET'])
@app.route('/signin', methods = ['POST', 'GET'])
def signin():
	try:
		if request.method == 'POST':
			user = request.form['username']
			passwd = request.form['password']
			mycursor.execute("SELECT * FROM users WHERE username='" + user + "' and password='" + passwd + "'")
			data=mycursor.fetchone()
			if data is not None:
				global typeL
				_,_,password,typeL=data
				if password==passwd:
					global isLoggedIn
					global currentuser
					currentuser = user
					isLoggedIn=True
					if typeL =='d':
						flash('You are now logged in')
						return redirect(url_for('doctor'))
					elif typeL=='t':
						flash('You are now logged in')
						return redirect(url_for('technician'))
					elif typeL=='p':
						flash('You are now logged in')
						return redirect(url_for('patient'))
					elif typeL=='a':
						flash('You are now logged in')
						return redirect(url_for('admin'))
					elif typeL=='n':
						flash('You are now logged in')
						return redirect(url_for('nurse'))				
			else:
				flash('Wrong username or Password')
				return render_template('signin.html')
		else: 			
			return render_template('signin.html')
	except:
		flash('Problem logging in!')
		return render_template('signin.html')

def is_logged_ind(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='d':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_int(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='t':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap

def is_logged_inp(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='p':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_inn(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='n':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap	

def is_logged_ina(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if isLoggedIn==True and typeL =='a':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('signin'))
    return wrap		   

@app.route('/home')
def home():
	global typeL
	if typeL =='a':
		return redirect(url_for('admin'))
	elif typeL=='p':
		return redirect(url_for('patient'))
	elif typeL=='d':
		return redirect(url_for('doctor'))
	elif typeL=='t':
		return redirect(url_for('technician'))
	elif typeL=='n':
		return redirect(url_for('nurse'))
	else:
		flash('Unauthorized, Please login')
		return redirect(url_for('signin'))


@app.route('/registerp', methods=['POST', 'GET'])
def registerp():
	try:
		if request.method == 'POST':
			fname = request.form['fname']
			minit = request.form['minit']
			lname = request.form['lname']
			ssn = request.form['ssn']
			address = request.form['address']
			pnumber = request.form['pnumber']
			email = request.form['email']
			gender = request.form['gender']
			bdate = request.form['bdate']
			username = request.form['username']
			password = request.form['password']
		
			sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
			val = (username, password, 'p')
			mycursor.execute(sql,val)
			mydb.commit()

			sql1 = 'SELECT ID FROM Users WHERE Username=%s'
			val1 = (username,)
			mycursor.execute(sql1, val1)
			id = mycursor.fetchone()

			sql = 'INSERT INTO patients(FName, MInit, LName, SSN, ADDRESS, PNUMBER, EMAIL, ID, GENDER, BDATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
			val = (fname, minit, lname, ssn, address, pnumber, email, id[0], gender, bdate)
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('signin'))
		else:
			return render_template('registerp.html')
	except:
		flash('Problem registering, please try again using different credentials!')
		return render_template('registerp.html')

@app.route('/patient', methods=['POST', 'GET'])
@is_logged_inp
def patient():
	try:
		if request.method == 'POST':
			scantype = request.form['Mtype']
			scandate = request.form['scandate']

			sql1 = 'SELECT ID FROM Users WHERE Username=%s'
			global currentuser
			val1 = (currentuser,)
			mycursor.execute(sql1, val1)
			id = mycursor.fetchone()
		
			#Scan assignment system
			scanassign(scandate, scantype, id)
		
			return redirect(url_for('patient'))
		else:
			return render_template('patient.html')
	except:
		flash('Failed to reserve scan, report issue to IT from the contact link above')
		return render_template('patient.html')
     

@app.route('/admin', methods=['GET', 'POST'])
@is_logged_ina
def admin(): 
	try:
		if request.method == 'POST':
			fname = request.form['fname']
			minit = request.form['minit']
			lname = request.form['Lname']
			ssn = request.form['DSSN']
			address = request.form['address']
			email = request.form['email']
			pnumber = request.form['pnumber']
			gender = request.form['gender']
			bdate = request.form['Bdate']
			hours = request.form['hours']
			username = request.form['username']
			password = request.form['password']
		
			sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
			val = (username, password, 'd')
			mycursor.execute(sql,val)
			mydb.commit()
		
			sql1 = 'SELECT ID FROM Users WHERE Username=%s'
			val1 = (username,)
			mycursor.execute(sql1, val1)
			id = mycursor.fetchone()
			sql = "INSERT INTO doctors (SSN, FName, MInit, LName, ADDRESS, PNUMBER,  GENDER, BDATE, ID, EMAIL, HOURS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			val = (ssn, fname, minit, lname, address, pnumber, gender, bdate, id[0], email, hours)    
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('admin'))
		else:
			return render_template('admin.html')
	except:
		flash('Failed to do task, report issue to IT from the contact link above')
		return render_template('admin.html')

@app.route('/admin/add-nurse', methods = ['GET', 'POST'])
def addnurse():
	try:
		if request.method == 'POST':
			fname = request.form['fname']
			minit = request.form['minit']
			lname = request.form['Lname']
			ssn = request.form['SSN']
			bdate = request.form['nBdate']
			address = request.form['address']
			pnumber = request.form['npnumber']
			gender = request.form['gender']
			hours = request.form['hours']
			email = request.form['email']
			username = request.form['username']
			password = request.form['password']
			sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
			val = (username, password, 'n')
			mycursor.execute(sql,val)
			mydb.commit()
			sql1 = 'SELECT ID FROM Users WHERE Username=%s'
			val1 = (username,)
			mycursor.execute(sql1, val1)
			id = mycursor.fetchone()
			sql = 'INSERT INTO nurses (FName, MInit, LName, SSN, BDATE, ADDRESS, PNUMBER, EMAIL, GENDER, ID, HOURS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
			val = (fname, minit, lname, ssn, bdate, address, pnumber, email, gender, id[0], hours)
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('addnurse'))
		else:
			return render_template('addnurse.html')
	except:
		flash('Failed to do task, report issue to IT from the contact link above')
		return render_template('addnurse.html')
	

@app.route('/admin/add-machine', methods = ['GET', 'POST'])
def addmachine():
	try:
		if request.method == 'POST':
			mtype = request.form['Mtype']
			mnumber = request.form['mnumber']
			cday = request.form['cday']
			purdate = request.form['purdate']
			sql = 'INSERT INTO machines(TYPE, MODELNO, CHECKDAYS, PURDATE, IN_USE) VALUES(%s, %s, %s, %s, %s)'
			val = (mtype, mnumber, cday, purdate, 0)
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('addmachine'))
		else:
			return render_template('addmachine.html')
	except:
		flash('Failed to do task, report issue to IT from the contact link above')
		return render_template('addmachine.html')

@app.route('/admin/add-room', methods = ['GET', 'POST'])
def addroom():
	try:
		if request.method == 'POST':
			name = request.form['rname']
			type = request.form['Mtype']
			sql= "SELECT ID FROM machines WHERE TYPE=%s AND IN_USE='0'"
			val = (type,)
			mycursor.execute(sql, val)
			id = mycursor.fetchone()
			sql = 'INSERT INTO rooms(NAME, MACHINE_ID, HOURS) VALUES (%s, %s, %s)'
			val = (name, id[0], 24)
			mycursor.execute(sql, val)
			mydb.commit()
			sql = "UPDATE machines SET IN_USE = '1' WHERE ID = %s"
			val = (id[0],)
			mycursor.execute(sql,val)
			mydb.commit()
			return redirect(url_for('addroom'))
		else:
			return render_template('addroom.html') 
	except:
		flash('Failed to do task, report issue to IT from the contact link above')
		return render_template('addroom.html')

@app.route('/admin/add-technician', methods = ['GET', 'POST'])
def addtechnician():
	try:
		if request.method == 'POST':
			fname = request.form['fname']
			minit = request.form['minit']
			lname = request.form['Lname']
			ssn = request.form['DSSN']
			address = request.form['address']
			pnumber = request.form['pnumber']
			gender = request.form['gender']
			bdate = request.form['bdate']
			email = request.form['email']
			username = request.form['username']
			password = request.form['password']
			sql = 'INSERT INTO users(Username, Password, Type) VALUES (%s, %s, %s)'
			val = (username, password, 't')
			mycursor.execute(sql,val)
			mydb.commit()
			sql1 = 'SELECT ID FROM Users WHERE Username=%s'
			val1 = (username,)
			mycursor.execute(sql1, val1)
			id = mycursor.fetchone()
			sql = "INSERT INTO technicians (SSN, FName, MInit, LName, ADDRESS, PNUMBER,  GENDER, BDATE, ID, EMAIL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			val = (ssn, fname, minit, lname, address, pnumber, gender, bdate, id[0], email)    
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('addtechnician'))
		else:
			return render_template('addtechnician.html') 
	except:
		flash('Failed to do task, report issue to IT from the contact link above')
		return render_template('addtechnician.html')  



@app.route('/doctor', methods=['POST', 'GET'])
@is_logged_ind
def doctor():
	if 	request.method == 'POST':
		try:
			case = request.form['data']
			diag = request.form['diag']
			caseid = int(re.findall(r'\d+', case)[0])
			mycursor.execute(f"DELETE FROM current_scans WHERE ID='{caseid}'")
			mydb.commit()
			mycursor.execute(f"UPDATE Scan_History SET DIAGNOSIS='{diag}' WHERE ID = '{caseid}'")
			mydb.commit()
			return redirect(url_for('doctor'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('doctor'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
			SELECT Patients.FName, Patients.LName, current_scans.DATE, current_scans.TYPE
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Doctors On current_scans.DR_ID=Doctors.ID
			WHERE current_scans.DR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		res = mycursor.fetchall()
		mycursor.execute(f'''
			SELECT current_scans.ID
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Doctors On current_scans.DR_ID=Doctors.ID
			WHERE current_scans.DR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		val = mycursor.fetchall()
		data = val + res
		x = len(val)
		return render_template('doctor.html', data=data, x=int(x))
	
@app.route('/doctor/patient-list', methods = ['POST', 'GET'])
def dview():
	global currentuser
	mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
	resid = mycursor.fetchone()
	mycursor.execute(f'''
	SELECT Patients.FName, Patients.LName, current_scans.TYPE, current_scans.DATE
	FROM Patients 
	JOIN current_scans On Patients.ID=current_scans.PAT_ID
	JOIN Doctors On current_scans.DR_ID=Doctors.ID
	JOIN Users On Doctors.ID=Users.ID
	WHERE current_scans.DR_ID = '{resid[0]}'
	ORDER BY DATE ASC''') 
	rowheaders = ['First Name', 'Last Name', 'Scan Type', 'Scan Date']
	res = mycursor.fetchall()
	data = {
		'rowheaders': rowheaders,
		'res': res}
	return render_template('dview.html', data = data)    



@app.route('/nurse', methods=['POST', 'GET'])
@is_logged_inn
def nurse():
	if 	request.method == 'POST':
		try:
			case = request.form['data']
			diag = request.form['diag']
			caseid = int(re.findall(r'\d+', case)[0])
			mycursor.execute(f"DELETE FROM current_scans WHERE ID='{caseid}'")
			mydb.commit()
			mycursor.execute(f"UPDATE Scan_History SET DIAGNOSIS='{diag}' WHERE ID = '{caseid}'")
			mydb.commit()
			return redirect(url_for('nurse'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('nurse'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
		resid = mycursor.fetchone()
		mycursor.execute(f'''
			SELECT Patients.FName, Patients.LName, current_scans.DATE, current_scans.TYPE
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Nurses On current_scans.NUR_ID=Nurses.ID
			WHERE current_scans.NUR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		res = mycursor.fetchall()
		mycursor.execute(f'''
			SELECT current_scans.ID
			FROM current_scans
			JOIN Patients On current_scans.PAT_ID=Patients.ID
			JOIN Nurses On current_scans.NUR_ID=Nurses.ID
			WHERE current_scans.NUR_ID='{resid[0]}'
			ORDER BY DATE ASC
		''')
		val = mycursor.fetchall()
		data = val + res
		x = len(val)
		return render_template('nurse.html', data=data, x=int(x))   

@app.route('/nurse/patient-list')
@is_logged_inn
def nview():
	global currentuser
	mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
	resid = mycursor.fetchone()
	mycursor.execute(f'''
	SELECT Patients.FName, Patients.LName, current_scans.TYPE, current_scans.DATE
	FROM Patients 
	JOIN current_scans On Patients.ID=current_scans.PAT_ID
	JOIN Nurses On current_scans.NUR_ID=Nurses.ID
	JOIN Users On Nurses.ID=Users.ID
	WHERE current_scans.NUR_ID = '{resid[0]}'
	ORDER BY DATE ASC''') 
	rowheaders = ['First Name', 'Last Name', 'Scan Type', 'Scan Date']
	res = mycursor.fetchall()
	data = {
		'rowheaders': rowheaders,
		'res': res}
	return render_template('nview.html', data = data)    
		
@app.route('/nurse/report-machine', methods = ['POST', 'GET'])
@is_logged_inn
def nmachine():
	if request.method == 'POST':
		try:
			machid = request.form['machid']
			issue = request.form['issue']
			machid = int(re.findall(r'\d+', machid)[0])
			mycursor.execute(f'''INSERT INTO MIssues(MACH_ID, ISSUE) VALUES ({machid}, '{issue}')''')
			mydb.commit()
			mycursor.execute(f"UPDATE Rooms SET AVAILABLE = '0' WHERE MACHINE_ID = {machid}")
			mydb.commit()
			return redirect(url_for('nmachine'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('nmachine'))
	else:
		mycursor.execute(f'''
			SELECT Machines.ID, Machines.TYPE 
			FROM Machines 
			JOIN Rooms ON Machines.ID = Rooms.MACHINE_ID 
			WHERE Rooms.AVAILABLE = '1'
		''')
		res = mycursor.fetchall()
		data = {
			'res':res
		}
		return render_template('nmachine.html', data=data) 



@app.route('/patient/patient-scan-history')
@is_logged_inp
def phistory():
	global currentuser
	mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
	resid = mycursor.fetchone()
	mycursor.execute(f'''
	SELECT Doctors.FName, Doctors.LName, Nurses.FName, Nurses.LName, Scan_History.TYPE, Scan_History.DATE
	FROM Scan_History
	JOIN Patients On Scan_History.PAT_ID=Patients.ID
	JOIN Nurses On Scan_History.NUR_ID=Nurses.ID
	JOIN Doctors On Scan_History.DR_ID=Doctors.ID
	JOIN Users On Patients.ID=Users.ID
	WHERE Scan_History.PAT_ID = '{resid[0]}'
	ORDER BY DATE ASC''')
	rowheaders = ['Dr First Name', 'Dr Last Name', 'Nurse First Name', 'Nurse Last Name','Scan Type', 'Scan Date']
	res = mycursor.fetchall()
	data = {
		'rowheaders': rowheaders,
		'res': res
	}
	return render_template('phistory.html', data = data)    
	
@app.route('/patient/view-reservation')
@is_logged_inp
def preservation():
	global currentuser
	mycursor.execute(f"SELECT ID FROM USERS WHERE Username = '{currentuser}'")
	resid = mycursor.fetchone()
	mycursor.execute(f'''
	SELECT Doctors.FName, Doctors.LName, Nurses.FName, Nurses.LName, current_scans.TYPE, current_scans.DATE
	FROM Patients 
	JOIN current_scans On Patients.ID=current_scans.PAT_ID
	JOIN Nurses On current_scans.NUR_ID=Nurses.ID
	JOIN Doctors On current_scans.DR_ID=Doctors.ID
	JOIN Users On Patients.ID=Users.ID
	WHERE current_scans.PAT_ID = '{resid[0]}'
	ORDER BY DATE ASC''') 
	rowheaders = ['Dr First Name', 'Dr Last Name', 'Nurse First Name', 'Nurse Last Name','Scan Type', 'Scan Date']
	res = mycursor.fetchall()
	data = {
		'rowheaders': rowheaders,
		'res': res}
	return render_template('preservation.html', data = data) 



@app.route('/technician', methods = ['POST', 'GET'])
@is_logged_int
def technician():
	if request.method == 'POST':
		try:
			machid = request.form['machid']
			machid = int(re.findall(r'\d+', machid)[0])
			global currentuser
			mycursor.execute(f"SELECT ID FROM Users WHERE Username='{currentuser}'")
			techid= mycursor.fetchone()
			mycursor.execute(f"UPDATE MIssues SET TECH_ID = '{techid[0]}' WHERE MACH_ID = {machid}")
			mydb.commit()
			return redirect(url_for('technician'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('technician'))
	else:
		mycursor.execute(f"SELECT Machines.ID, Machines.TYPE, MIssues.ISSUE FROM Machines JOIN MIssues ON Machines.ID = MIssues.MACH_ID WHERE MIssues.TECH_ID IS NULL")
		res = mycursor.fetchall()
		mycursor.execute(f"SELECT Machines.ID FROM Machines JOIN MIssues ON Machines.ID = MIssues.MACH_ID WHERE MIssues.TECH_ID IS NULL")
		val = mycursor.fetchall()
		data = val + res
		x = len(val)
		return render_template('technician.html', data=data, x=x)

@app.route('/technician/treport', methods=['POST', 'GET'])
@is_logged_int
def treport():
	if request.method == 'POST':
		try:
			machid = request.form['machid']
			machid = int(re.findall(r'\d+', machid)[0])
			fix = request.form['fix']
			mycursor.execute(f'''
				INSERT INTO Issue_History(MACH_ID, TECH_ID, ISSUE)
				SELECT MACH_ID, TECH_ID, ISSUE FROM MIssues
				WHERE MIssues.ID NOT IN (SELECT ID FROM Issue_History)
			''')
			mydb.commit()
			mycursor.execute(f"DELETE FROM MIssues WHERE MACH_ID = {machid}")
			mydb.commit()
			mycursor.execute(f"UPDATE Rooms SET AVAILABLE = '1' WHERE MACHINE_ID = {machid}")
			mydb.commit()
			mycursor.execute(f"UPDATE Issue_History SET FIX = '{fix}' WHERE MACH_ID = {machid}")
			mydb.commit()
			return redirect(url_for('treport'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('treport'))
	else:
		global currentuser
		mycursor.execute(f"SELECT ID FROM Users WHERE Username='{currentuser}'")
		techid= mycursor.fetchone()
		mycursor.execute(f'''
			SELECT Machines.ID, Machines.TYPE, MIssues.ISSUE
			FROM MIssues
			JOIN Machines ON MIssues.MACH_ID = Machines.ID
			WHERE MIssues.TECH_ID = {techid[0]}
		''')
		res = mycursor.fetchall()
		mycursor.execute(f'''
			SELECT Machines.ID
			FROM MIssues
			JOIN Machines ON MIssues.MACH_ID = Machines.ID
			WHERE MIssues.TECH_ID = {techid[0]}
		''')
		val = mycursor.fetchall()
		data = val+res
		x = len(val)
		return render_template('treport.html', data=data, x=x)

@app.route('/technician/checks', methods = ['POST', 'GET'])
@is_logged_int
def tchecks():
	if request.method == 'POST':
		try:
			machid = request.form['machid']
			machid = int(re.findall(r'\d+', machid)[0])
			result = request.form['result']
			global currentuser
			mycursor.execute(f"SELECT ID FROM Users WHERE Username='{currentuser}'")
			techid= mycursor.fetchone()
			mycursor.execute(f"UPDATE Machines SET USES = 0 WHERE ID = {machid}")
			mydb.commit()
			mycursor.execute(f"INSERT INTO Issue_History(MACH_ID, TECH_ID, ISSUE, FIX) VALUES({machid}, {techid[0]}, 'Regular Check', '{result}')")
			mydb.commit()
			return redirect(url_for('tchecks'))
		except:
			flash('Failed to do task, report issue to IT from the contact link above')
			return redirect(url_for('tchecks'))
	else:
		mycursor.execute(f'''
			SELECT ID
			FROM Machines
			WHERE USES >= 15
		''')
		val = mycursor.fetchall()
		mycursor.execute(f'''
			SELECT ID, TYPE
			FROM Machines
			WHERE USES >= 15
		''')
		res = mycursor.fetchall()
		data = val + res
		x = len(val)
		return render_template('tchecks.html', data=data, x=x)

@app.route('/technician/issues')
@is_logged_int
def tissues():
	global currentuser
	mycursor.execute(f"SELECT ID FROM Users WHERE Username='{currentuser}'")
	techid= mycursor.fetchone()
	mycursor.execute(f'''
		SELECT Machines.ID, Machines.TYPE, MIssues.ISSUE
		FROM MIssues
		JOIN Machines ON MIssues.MACH_ID = Machines.ID
		WHERE MIssues.TECH_ID = {techid[0]}
	''')
	res = mycursor.fetchall()
	rowheaders = ['Machine ID', 'Machine Type', 'Issue Reported']
	data = {
		'res':res,
		'rowheaders':rowheaders
	}
	return render_template('tissues.html', data = data) 

@app.route('/about')
def about():
	return render_template('about.html') 

@app.route('/contact')
def contact():	return render_template('contact.html') 


if __name__=='__main__':
	app.run(debug=True)