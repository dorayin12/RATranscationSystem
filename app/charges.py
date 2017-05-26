import MySQLdb as dbapi
import sys
import os
import glob
import csv
import base64
import smtplib
from datetime import datetime, timedelta
import time


##name the file
daypoint1  = datetime.now() - timedelta(days=300)  #last week today
day1       = daypoint1.strftime('%Y-%m-%d') #end
daypoint2  = datetime.now()  #today
day2       = daypoint2.strftime('%Y-%m-%d') #start
name_str   = 'RACharges_' + daypoint1.strftime('%m%d%y') + '-' + daypoint2.strftime('%m%d%y')
csvname    = name_str + '.csv'#show only date
csvpath    = 'C:/tmp/' +  csvname

#'/var/www/statmathsales/reports/' + name_str
print day1
print day2
print csvpath


dbServer='localhost'
dbSchema='rasale'
dbUser='root'
dbPass=''

dbQuery = '(SELECT "charge form", "date", "buyer", "email", "account", "sub-account", "obj code", "sub obj", "units", "amount", "description")\
            UNION ALL\
            (SELECT orders.form_number, orders.date_soldon, users.user_name, users.email, \
                    accounts.account_number, accounts.sub_account, \
                    orders.obj_code, sub_objcode, quantity, total_cost, item_title\
            FROM rasale.users, rasale.accounts, rasale.orders\
            WHERE users.id_user = accounts.id_user and accounts.id_acc_auto=orders.id_acc_auto and date_soldon BETWEEN %s AND %s\
            AND orders.sales_type = "RA" \
            ORDER BY users.id_user ASC, accounts.id_acc_auto ASC);' #ORDER DOESN'T WORK HERE


db=dbapi.connect(host=dbServer,user=dbUser, passwd=dbPass)
cursor=db.cursor()
cursor.execute(dbQuery, (day1, day2))      
result=cursor.fetchall()

f = open(csvpath,"wb")
c = csv.writer(f)
for row in result:
    c.writerow(row)
f.close()                  #close the csv to sent as attachment (highly important)
print "Data has been successfully written in a CSV file!"

#Wait
time.sleep(10) 



##Send an email
filename = csvname
filepath = csvpath
# Read a file and encode it into base64 format
fo = open(filepath, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64

sender = 'researchanalytics@iu.edu'
reciever = 'wsang@indiana.edu'

marker = "AUNIQUEMARKER"

body ="""
This is the weekly report of software sale information from Research Analytics.
The excel report is attached to thie email for review.
If you have questions please reply to this email or direct your questions to Kevin Wilhite at kwilhite@indiana.edu.
"""
# Define the main headers.
part1 = """From: Research Analytics <researchanalytics@iu.edu>
To: Finance Office <finance@iu.com>
Subject: Weekly software sales report
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3

try:
   smtpObj = smtplib.SMTP('mail-relay.iu.edu')
   smtpObj.sendmail(sender, reciever, message)
   print "Successfully sent email"
except Exception:
   print "Error: unable to send email"

