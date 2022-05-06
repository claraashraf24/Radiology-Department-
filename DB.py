import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="@Hm$d_2001",
)
mycursor = mydb.cursor()
mycursor.execute('DROP DATABASE IF EXISTS Radiology')
mydb.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS Radiology")
mydb.commit()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="@Hm$d_2001",
    database='Radiology'
)
mycursor = mydb.cursor()

mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    ID INT NOT NULL UNIQUE AUTO_INCREMENT,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(60) NOT NULL,
    Type VARCHAR(1) NOT NULL,
    PRIMARY KEY(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
    ID INT NOT NULL UNIQUE,
    FName VARCHAR(255) NOT NULL,
    MInit VARCHAR(255),
    LName VARCHAR(255) NOT NULL,
    SSN INT NOT NULL UNIQUE,
    GENDER VARCHAR(45) NOT NULL,
    PNUMBER INT NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    BDATE DATE NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    PRIMARY KEY(SSN),
    CONSTRAINT FK_ID
        FOREIGN KEY(ID)
        REFERENCES Users (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Doctors (
    ID INT NOT NULL UNIQUE,
    FName VARCHAR(255) NOT NULL,
    MInit VARCHAR(255),
    LName VARCHAR(255) NOT NULL,
    SSN INT NOT NULL UNIQUE,
    GENDER VARCHAR(45) NOT NULL,
    PNUMBER INT NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    BDATE DATE NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    HOURS INT NOT NULL,
    PRIMARY KEY(SSN),
    CONSTRAINT FK_ID1
        FOREIGN KEY(ID)
        REFERENCES Users (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Nurses (
    ID INT NOT NULL UNIQUE,
    FName VARCHAR(255) NOT NULL,
    MInit VARCHAR(255),
    LName VARCHAR(255) NOT NULL,
    SSN INT NOT NULL UNIQUE,
    GENDER VARCHAR(45) NOT NULL,
    PNUMBER INT NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    BDATE DATE NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    HOURS INT NOT NULL,
    PRIMARY KEY(SSN),
    CONSTRAINT FK_ID2
        FOREIGN KEY(ID)
        REFERENCES Users (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Technicians (
    ID INT NOT NULL UNIQUE,
    FName VARCHAR(255) NOT NULL,
    MInit VARCHAR(255),
    LName VARCHAR(255) NOT NULL,
    SSN INT NOT NULL UNIQUE,
    GENDER VARCHAR(45) NOT NULL,
    PNUMBER INT NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    BDATE DATE NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    PRIMARY KEY(SSN),
    CONSTRAINT FK_ID3
        FOREIGN KEY(ID)
        REFERENCES Users (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Admins (
    ID INT NOT NULL UNIQUE,
    FName VARCHAR(255) NOT NULL,
    MInit VARCHAR(255),
    LName VARCHAR(255) NOT NULL,
    SSN INT NOT NULL UNIQUE,
    GENDER VARCHAR(45) NOT NULL,
    PNUMBER INT NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    BDATE DATE NOT NULL,
    ADDRESS VARCHAR(255) NOT NULL,
    PRIMARY KEY(SSN),
    CONSTRAINT FK_ID4
        FOREIGN KEY(ID)
        REFERENCES Users (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Machines (
    ID INT NOT NULL UNIQUE AUTO_INCREMENT,
    MODELNO INT NOT NULL,
    TYPE VARCHAR(45) NOT NULL,
    PURDATE DATE NOT NULL,
    CHECKDAYS INT NOT NULL,
    IN_USE TINYINT NOT NULL,
    USES INT NOT NULL DEFAULT 0,
    PRIMARY KEY(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Changes (
    ID INT NOT NULL UNIQUE AUTO_INCREMENT,
    ADMIN_ID INT NOT NULL UNIQUE,
    DETAILS VARCHAR(255) NOT NULL,
    DATETIME DATETIME(0) NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT FK_ADMIN
        FOREIGN KEY (ADMIN_ID)
        REFERENCES Admins (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Rooms (
    ID INT NOT NULL UNIQUE AUTO_INCREMENT,
    NAME VARCHAR(255),
    MACHINE_ID INT NOT NULL UNIQUE,
    HOURS INT NOT NULL,
    AVAILABLE BOOL NOT NULL DEFAULT '1',
    PRIMARY KEY(ID),
    CONSTRAINT FK_MACHINE
        FOREIGN KEY (MACHINE_ID)
        REFERENCES Machines (ID)
    );
''')
mydb.commit()

mycursor.execute('''
    CREATE TABLE IF NOT EXISTS current_scans (
    ID INT NOT NULL UNIQUE AUTO_INCREMENT,
    PAT_ID INT NOT NULL,
    DR_ID INT NOT NULL,
    NUR_ID INT NOT NULL,
    ROOM_ID INT NOT NULL,
    TYPE VARCHAR(45) NOT NULL,
    DATE DATE NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT FK_ID6
        FOREIGN KEY(PAT_ID)
        REFERENCES Patients (ID),
    CONSTRAINT FK_ID9
        FOREIGN KEY(DR_ID)
        REFERENCES Doctors (ID),
    CONSTRAINT FK_ID10
        FOREIGN KEY(NUR_ID)
        REFERENCES Nurses (ID),
    CONSTRAINT FK_I11
        FOREIGN KEY(ROOM_ID)
        REFERENCES Rooms (ID)
    )
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Scan_History (
    ID INT NOT NULL UNIQUE,
    PAT_ID INT NOT NULL,
    DR_ID INT NOT NULL,
    NUR_ID INT NOT NULL,
    TYPE VARCHAR(45) NOT NULL, 
    DIAGNOSIS TINYTEXT,
    DATE DATE NOT NULL,
    PRIMARY KEY(ID),
    CONSTRAINT FK_ID5
        FOREIGN KEY(PAT_ID)
        REFERENCES Patients (ID),
    CONSTRAINT FK_ID11
        FOREIGN KEY(DR_ID)
        REFERENCES Doctors (ID),
    CONSTRAINT FK_ID12
        FOREIGN KEY(NUR_ID)
        REFERENCES Nurses (ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS DoctorHours (
    DATE DATE NOT NULL,
    DR_ID INT NOT NULL,
    HOURS_USED INT NOT NULL,
    CONSTRAINT FK_DRID
        FOREIGN KEY(DR_ID)
        REFERENCES Doctors(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS NurseHours (
    DATE DATE NOT NULL,
    NUR_ID INT NOT NULL,
    HOURS_USED INT NOT NULL,
    CONSTRAINT FK_NURID1
        FOREIGN KEY(NUR_ID)
        REFERENCES Nurses(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS RoomHours (
    DATE DATE NOT NULL,
    ROOM_ID INT NOT NULL,
    HOURS_USED INT NOT NULL,
    CONSTRAINT FK_ROOMID
        FOREIGN KEY(ROOM_ID)
        REFERENCES Rooms(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS MIssues (
    MACH_ID INT NOT NULL,
    TECH_ID INT,
    ISSUE TINYTEXT,
    CONSTRAINT FK_TECH
        FOREIGN KEY(TECH_ID)
        REFERENCES Technicians(ID),
    CONSTRAINT FK_MACH1
        FOREIGN KEY(MACH_ID)
        REFERENCES Machines(ID)
    );
''')
mydb.commit()
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Issue_History (
    MACH_ID INT NOT NULL,
    TECH_ID INT,
    ISSUE TINYTEXT,
    FIX TINYTEXT,
    CONSTRAINT FK_TECH1
        FOREIGN KEY(TECH_ID)
        REFERENCES Technicians(ID),
    CONSTRAINT FK_MACH2
        FOREIGN KEY(MACH_ID)
        REFERENCES Machines(ID)
    );
''')
mydb.commit()

sql = 'INSERT INTO Users (Username, Password, Type) VALUES (%s, %s, %s)'
val = ('admin', 'admin', 'a')
mycursor.execute(sql,val)
mydb.commit()
