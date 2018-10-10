from flask import Flask, render_template, request
import mysql.connector
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/question_list', methods=["POST"])
def question_list():
    mycursor.execute("SELECT entity_id FROM field_data_field_user_lastname WHERE field_user_lastname_value = '%s'" % request.values.get('user'))
    result = mycursor.fetchall()
    return str(result[0][0])


if __name__ == '__main__':
    
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'editx'
    }
    '''

    config = {
     'host':"localhost",
     'user':"root",
     'passwd':"root",
     'database':"blabla",
     'port':'8889'
    }
    '''
    mydb = mysql.connector.connect(**config)
    mycursor = mydb.cursor()
    app.run(host='0.0.0.0')
