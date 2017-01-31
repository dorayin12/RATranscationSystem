from flask import Flask
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empdata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
from werkzeug import generate_password_hash, check_password_hash
_hashed_password = generate_password_hash(_password)
cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
data = cursor.fetchall()
 
if len(data) is 0:
    conn.commit()
    return json.dumps({'message':'User created successfully !'})
else:
    return json.dumps({'error':str(data[0])})
