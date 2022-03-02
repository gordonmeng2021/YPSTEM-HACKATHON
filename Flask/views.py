#Contains the routings and the view functions
import re
from datetime import datetime

from sys import flags


from flask import Flask, render_template, request, redirect, flash

from . import app

#database
import sqlite3 as sql

#Plot graph imports
import datetime as DT
import matplotlib.pyplot as plt

import cv2
from threading import *
import time

@app.route("/")
def unloggedin():
    return render_template("unloggedin.html")

@app.route("/home/")
def home():
    username = "imcoolthanks"
    return render_template("home.html",username=username)

#---------------------------------open focusing function
#*******the time they focus

focusedTime = 0
notfocusedTime = 0
#Get block website info
#Hostpath
hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
reroute = "127.0.0.1"

#default
user_username = "imcoolthanks"
user_email = "queena1234@gmail.com"

@app.route("/focuz/")
def focuz():
    print("Focuz running")
    face_cascade = cv2.CascadeClassifier('Flask/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)


    def start_blocking():
        with open(hostsPath, 'r+') as file:
            content = file.read()
            for site in get_blocked_website_list(user_email):
                if site in content:
                    pass
                else:
                    file.write(reroute + " " + site + "\n")

    def focus():
        global isFocus
        isFocus = True
    
    def run():
        
        global isFocus,focusedTime,notfocusedTime,state
        state= True
    
        while state:
             
            startTimer=time.time()
            isFocus = False
    # Read the frame
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                if len(faces)<2:
                    focus()
               
            
               # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
               
        # change state if has face
               
               
            if isFocus == False:
                print("You are not focusing")
                endTimer=time.time()
                notfocusedTime += (endTimer-startTimer) 
            else:
                print("You are okay")
                endTimer=time.time()
                focusedTime += (endTimer-startTimer)
            
         
            
            k = cv2.waitKey(1) & 0xff
            if k==27:
                break
    
    
    start_blocking()
    run()
    # print("You have focused :", str(int(focusedTime)),'s')
    # print("You have not focused :", str(int(notfocusedTime)),'s')  
    return "Get back to continue"

    
@app.route("/stop/")
def stop():
    global state,focusedTime,notfocusedTime
    state=False
    flash("You have stopped FOCUZ","info")
    flash("You have focused : "+ str(int(focusedTime))+'s')
    flash("You have not focused : "+ str(int(notfocusedTime))+'s')
    
    #Inserting into database
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    query = "INSERT INTO focus_time VALUES (?,?,?)"
    cur.execute(query, [user_email, 0 , focusedTime])

    conn.commit()

    conn.close()

    with open(hostsPath, 'w') as file:
        file.write(
'''# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost

''')

    focusedTime=0
    notfocusedTime=0 
    
    return render_template("home.html")

@app.route("/puzzle/")
def puzzle():
    print("dfdfdfdfdfdfdf")
    
    return render_template("luckydraw.html",imgpath= "static/Assets/luckydraw/puzzle1-S.jpg")

@app.route("/luckydraw/")
def luckydraw():
    #Inserting into database
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    query = "INSERT INTO focus_time VALUES (?,?,?)"
    sum_time = "SELECT SUM(hours) FROM focus_time"
    cur.execute(query, [user_email, 0 , focusedTime])
    cur.execute(sum_time)

    row = cur.fetchall()
    int_row = int(row[0][0])
    conn.commit()

    conn.close()
    return render_template("luckydraw.html", int_row = int_row)


@app.route("/login/", methods = ['POST', 'GET'])
def login():                
    if request.method == 'POST':
        global user_email
        global user_username

        email = request.form.get('email') 
        password = request.form.get('password')

        success = login(email, password)
        
        if success:
            user_username = get_username(email)
            user_email = email

            return render_template("home.html")
        else:
            return render_template('login.html', error="Incorrect email or password.")

    return render_template('login.html')

@app.route("/dashboard/")
def dashboard():
    save_url = graph(user_email)
    return render_template("dashboard.html", save_url=save_url)
    

#After pressing buttons in setting page...
@app.route('/setting/', methods = ["POST", "GET"])
def unblock_or_block():
    #loading from database
    def get_user_data():
        conn = sql.connect("Flask/static/Databases/database.db")
        cur = conn.cursor()

        user_data = '''SELECT username, user.email, password, SUM(hours), MAX(days_ago), icon_photo FROM focus_time, user 
        WHERE focus_time.email = user.email '''

        cur.execute(user_data)

        row = cur.fetchall()

        conn.commit()

        username = row[0][0]
        email = row[0][1]
        pw = row[0][2]
        int_time = int(row[0][3])
        days_ago = row[0][4]
        icon_pic = row[0][5]
        #change to email
        website = get_blocked_website_list(user_email)

        conn.close()

        return website, username, email, pw, int_time, days_ago, icon_pic

    #pressing different buttons
    if request.method == "POST":
        if request.form['add_website'] == 'block':  #add website button
            new_website = request.form['website']
            add_blocked_website(user_email,new_website)
            website, username, email, pw, int_time, days_ago, icon_pic = get_user_data()
            return render_template("setting.html", website = website, username=username, email=email, password=pw, int_time = int_time, days_ago = days_ago, icon_pic = icon_pic )

        elif request.form['add_website'] == 'unblock_all':  #unblock all button
            print("Unblock all")
            unblock_all_website(user_email)  
            website, username, email, pw, int_time, days_ago, icon_pic = get_user_data()
            return render_template("setting.html", website = website, username=username, email=email, password=pw, int_time = int_time, days_ago = days_ago, icon_pic = icon_pic )

        elif request.form['add_website'] == 'unblock_one':  #unblock one website button
            print("Unblock one")
            url = request.form['url']
            print("Website to be unblocked:" + url)
            remove_blocked_website(user_email,url)
            website, username, email, pw, int_time, days_ago, icon_pic = get_user_data()
            return render_template("setting.html", website = website, username=username, email=email, password=pw, int_time = int_time, days_ago = days_ago, icon_pic = icon_pic )

    else:   #return to setting page
        website, username, email, pw, int_time, days_ago, icon_pic = get_user_data()
        return render_template("setting.html", website = website, username=username, email=email, password=pw, int_time = int_time, days_ago = days_ago, icon_pic = icon_pic )


def unblock_all_website(email):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    delete_query = "DELETE FROM blocked_website WHERE email = ?"
    cur.execute(delete_query, (email,))

    conn.commit()
    conn.close()












    
        
            
    


#-------------------- DATABASE FUNCTIONS -----------------------
#USER INFO
def create_users_info():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #username + email (unique) + password + icon_photo
    conn.execute("""CREATE TABLE user (username TEXT, email TEXT PRIMARY KEY, password TEXT, icon_photo TEXT)""")
    cur = conn.cursor()
    print("table created")
    
    #DEMO user
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, ("imcoolthanks", "queena1234@gmail.com", "1234", "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()

    conn.close()

def login(email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT password FROM user WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    true_password = cur.fetchall()[0][0]

    conn.close()

    if password == true_password:
        print("Logged in")
        return True
    else:
        print("Wrong Password")
        return False

def sign_up(username, email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()
    
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, (username, email, password, "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()
    conn.close()


#BLOCKED WEBSITE
def create_blocked_website():
    #blocked_website(email,seq_no,url)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email,seq_no,url
    conn.execute("""CREATE TABLE blocked_website (email TEXT, url TEXT )""")
    print("table created")

    #DEMO 
    cur = conn.cursor()
    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, ("queena1234@gmail.com", "https://www.youtube.com/"))
    print("user added")

    conn.commit()

    conn.close()

    print("Loading completed")

#return list of all blocked website
def get_blocked_website_list(email):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT url FROM blocked_website WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    rows = cur.fetchall()
    url_list = []

    for i in rows:
        url_list.append(i[0])

    conn.close()

    return url_list

def add_blocked_website(email, url):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    websites = get_blocked_website_list(email)
    if url in websites:
        return

    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, (email, url))
    conn.commit()

    conn.close()

def remove_blocked_website(email, url):
    
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    delete_query = "DELETE FROM blocked_website WHERE email = ? and url = ?"
    cur.execute(delete_query, (email, url))
    conn.commit()

    conn.close()

#FOCUS TIME
def create_focus_time():
    #focus_time(email,days_ago,hours)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email, days_ago, hours
    conn.execute("""CREATE TABLE focus_time (email TEXT, days_ago INTEGER, hours INTEGER )""")
    print("table created")

    #DEMO
    cur = conn.cursor()
    insert_query = """INSERT INTO focus_time (email, days_ago, hours)
                                       VALUES (?,?,?)"""
    for i in range(7):                                   
        cur.execute(insert_query, ("queena1234@gmail.com", i, i))
    print("user added")

    conn.commit()
    conn.close()
#Update Focus time at end of day !!!CHANGE
def insert_focus_time(email, today_hours):
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = "+str(today_hours)+" where email = ? and days_ago = 0"
    cur.execute(query, (email, ))

    conn.commit()
    conn.close()

#execute when 12am
def update_all_focus_time():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #all +1
    query = "UPDATE focus_time SET days_ago = days_ago + 1"
    cur.execute(query)

    query = "update focus_time set days_ago = REPLACE(days_ago, 7, 0)"
    cur.execute(query)

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = 0 where days_ago = 0"
    cur.execute(query)

    conn.commit()
    conn.close()

#graph
def graph(email):    
    today = DT.date.today()

    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #get username
    username = get_username(email)

    #get focus_time
    query = 'SELECT hours FROM focus_time WHERE email = ?'
    cur.execute(query, (email,))
    rows = cur.fetchall()
    focus_time = []

    for i in rows:
        focus_time.append(i[0])

    conn.close()

    print(focus_time)

    #Get x-axis data
    days = []
    for i in range(7):
        d = today - DT.timedelta(days=(6-i))
        days.append(d.strftime("%m/%d"))

    print(days)

    #Plot average line
    average = sum(focus_time) / len(focus_time)

    #Plot the 2 graphs
    plt.plot(days, focus_time)
    plt.axhline(y=average, color='r', linestyle='--')

    #Graph settings
    plt.axis([0, 6, 0, max(focus_time)+1]) #set axis
    plt.xlabel('Date')
    plt.ylabel('Number of hours focusing')
    plt.title('Past 7 Days Stats')

    #Save Graph
    save_url = 'Assets/graphs/'+username+'.png'
    plt.savefig('Flask/static/'+ save_url)
    return save_url

def get_username(email):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT username FROM user WHERE email = ?'
    cur.execute(query, (email,))
    username = cur.fetchall()[0][0]

    conn.close()

    return username

def get_email(username):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT email FROM user WHERE username = ?'
    cur.execute(query, (username,))
    email = cur.fetchall()[0][0]

    conn.close()

    return email

#USED FOR DEBUGGING
def list_all():
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    tables = ["user", "blocked_website", "focus_time"]

    for t in tables:
        print(t+":")
        cur.execute("SELECT * FROM "+t)

        rows = cur.fetchall()

        for row in rows:
            print(row)

        print("\n")

#Delete and restart with basic DEMOs
def reset_database():
    create_blocked_website()
    create_focus_time()
    create_users_info()
    list_all()

