import mysql.connector
from flask import Flask, render_template, request, redirect, flash, url_for
from flask.templating import render_template
import mysql.connector
import pandas as pd
import numpy as np



def scanassign(scandate, scantype, id):
	scandate = scandate.replace('-','')
	mydb = mysql.connector.connect(
		host = 'localhost',
		username = 'root',
		passwd = '@Hm$d_2001',
		database = 'radiology'
	)
	mycursor = mydb.cursor(buffered =True)
	drid = -1; nurid = -1; roomid = -1
	extradr = -1; extranur = -1; extraroom = -1
	
	#doctors
	mycursor.execute(f'SELECT * FROM DoctorHours WHERE DATE={scandate} ORDER BY Dr_ID DESC LIMIT 1')
	drhrs = mycursor.fetchone()
	mycursor.execute(f"SELECT ID, HOURS FROM Doctors ORDER BY ID")
	dr = mycursor.fetchall()
	df = pd.DataFrame(dr)
	if (drhrs):
		df1 = df[1].where(df[0] == drhrs[1])
		mycursor.execute(f"SELECT COUNT(DR_ID) FROM DoctorHours WHERE DATE ='{scandate}'")
		drc = mycursor.fetchall()
		if (drc[0][0] == 0):
			i = 0
		else:
			i = drc[0][0] - 1
		if int(drhrs[2]) < df1[i]:
			drid = drhrs[1]
			extradr = 0
		else:
			extradr = 1
			mycursor.execute(f"SELECT ID FROM Doctors WHERE ID > {drhrs[1]} ORDER BY ID LIMIT 1")
			drid = mycursor.fetchone()
	else:
		extradr = 1
		mycursor.execute("SELECT ID FROM Doctors")
		drid = mycursor.fetchone()


	#nurses
	mycursor.execute(f'SELECT * FROM NurseHours WHERE DATE={scandate} ORDER BY NUR_ID DESC LIMIT 1')
	nurhrs = mycursor.fetchone()
	mycursor.execute(f"SELECT ID, HOURS FROM Nurses ORDER BY ID")
	nur = mycursor.fetchall()
	df = pd.DataFrame(nur)
	if (nurhrs):
		df1 = df[1].where(df[0] == nurhrs[1])
		mycursor.execute(f"SELECT COUNT(NUR_ID) FROM NurseHours WHERE DATE ='{scandate}'")
		nurc = mycursor.fetchall()
		if (nurc[0][0] == 0):
			i = 0
		else:
			i = nurc[0][0] - 1
		if int(nurhrs[2]) < df1[i]:
			nurid = nurhrs[1]
			extranur = 0
		else:
			extranur = 1
			mycursor.execute(f"SELECT ID FROM Nurses WHERE ID > {nurhrs[1]} ORDER BY ID LIMIT 1")
			nurid = mycursor.fetchone()
	else:
		extranur = 1
		mycursor.execute("SELECT ID FROM Nurses")
		nurid = mycursor.fetchone()

	#rooms
	mycursor.execute(f'SELECT * FROM RoomHours WHERE DATE={scandate} ORDER BY ROOM_ID DESC LIMIT 1')
	roomhrs = mycursor.fetchone()
	mycursor.execute(f'''
		SELECT Rooms.ID, Rooms.HOURS 
		FROM Rooms 
		JOIN Machines ON Rooms.MACHINE_ID=Machines.ID 
		WHERE Machines.TYPE="{scantype}" AND Rooms.AVAILABLE = '1'
		ORDER BY Rooms.ID''')
	rooms = mycursor.fetchall()
	df = pd.DataFrame(rooms)
	if (roomhrs):
		df1 = df[1].where(df[0] == roomhrs[1])
		mycursor.execute(f"SELECT COUNT(ROOM_ID) FROM RoomHours WHERE DATE ='{scandate}'")
		roomc = mycursor.fetchall()
		if (roomc[0][0] == 0):
			i = 0
		else:
			i = roomc[0][0] - 1
		if int(roomhrs[2]) < df1[i]:
			roomid = roomhrs[1]
			extraroom = 0
		else:
			extraroom = 1
			mycursor.execute(f'''
				SELECT Rooms.ID, Rooms.HOURS 
				FROM Rooms 
				JOIN Machines ON Rooms.MACHINE_ID=Machines.ID 
				WHERE Machines.TYPE="{scantype}" AND Rooms.ID > {roomhrs[1]} AND Rooms.AVAILABLE = '1'
				ORDER BY Rooms.ID
			''')
			roomid = mycursor.fetchone()
	else:
		extraroom = 1
		mycursor.execute(f'''
		SELECT Rooms.ID 
		FROM Rooms 
		JOIN Machines ON Rooms.MACHINE_ID=Machines.ID 
		WHERE Machines.TYPE="{scantype}" AND Rooms.AVAILABLE = '1'
		ORDER BY Rooms.ID''')
		roomid= mycursor.fetchone()


	if isinstance(drid, tuple):
		drid=drid[0]
	if isinstance(nurid, tuple):
		nurid=nurid[0]
	if isinstance(roomid, tuple):
		roomid=roomid[0]


	if (drid) and (nurid) and (roomid):
		sql = 'INSERT INTO current_scans(PAT_ID, DATE, TYPE, DR_ID, NUR_ID, ROOM_ID) VALUES (%s, %s, %s, %s, %s, %s)'
		val = (id[0], scandate, scantype, int(drid), int(nurid), int(roomid))
		mycursor.execute(sql, val)
		mydb.commit()
		mycursor.execute(f'''
			INSERT INTO Scan_History(ID, PAT_ID, TYPE, DATE, DR_ID, NUR_ID)
			SELECT ID, PAT_ID, TYPE, DATE, DR_ID, NUR_ID FROM current_scans
			WHERE current_scans.ID NOT IN (SELECT ID FROM Scan_History)
		''')
		mydb.commit()
		if (extradr == 1):
			sql = 'INSERT INTO DoctorHours(DATE, DR_ID, HOURS_USED) VALUES (%s, %s, %s)'
			val = (scandate, int(drid), 1)
			mycursor.execute(sql, val)
			mydb.commit
		elif (extradr == 0):
			mycursor.execute(f"UPDATE DoctorHours SET HOURS_USED = {drhrs[2] + 1} WHERE DR_ID = {drhrs[1]}")
			mydb.commit()
		
		if (extranur == 1):
			sql = 'INSERT INTO NurseHours(DATE, NUR_ID, HOURS_USED) VALUES (%s, %s, %s)'
			val = (scandate, int(nurid), 1)
			mycursor.execute(sql, val)
			mydb.commit()
		elif (extranur == 0):
			mycursor.execute(f"UPDATE NurseHours SET HOURS_USED = {nurhrs[2] + 1} WHERE NUR_ID = {nurhrs[1]}")
			mydb.commit()

		if (extraroom == 1):
			sql = 'INSERT INTO RoomHours(DATE, ROOM_ID, HOURS_USED) VALUES (%s, %s, %s)'
			val = (scandate, int(roomid), 1)
			mycursor.execute(sql, val)
			mydb.commit()
			mycursor.execute(f'''
				SELECT MACHINE_ID
				FROM Rooms
				WHERE ID = {roomid}
			''')
			machid = mycursor.fetchone()
			mycursor.execute(f'''
				SELECT Machines.USES
				FROM Machines
				JOIN Rooms ON Machines.ID = Rooms.MACHINE_ID
				WHERE Rooms.ID = {roomid}
			''')
			uses = mycursor.fetchone()
			uses = uses[0] + 1
			mycursor.execute(f"UPDATE Machines SET USES = {uses} WHERE ID = {machid[0]}")
			mydb.commit()
		elif (extraroom == 0):
			mycursor.execute(f"UPDATE RoomHours SET HOURS_USED = {roomhrs[2] + 1} WHERE ROOM_ID = {roomhrs[1]}")
			mydb.commit()
			mycursor.execute(f'''
				SELECT MACHINE_ID
				FROM Rooms
				WHERE ID = {roomhrs[1]}
			''')
			machid = mycursor.fetchone()
			mycursor.execute(f'''
				SELECT Machines.USES
				FROM Machines
				JOIN Rooms ON Machines.ID = Rooms.MACHINE_ID
				WHERE Rooms.ID = {roomhrs[1]}
			''')
			uses = mycursor.fetchone()
			uses = uses[0] + 1
			mycursor.execute(f"UPDATE Machines SET USES = {uses} WHERE ID = {machid[0]}")
			mydb.commit()
	else:
		flash('Failed to reserve, no more room in this day!')