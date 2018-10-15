from flask import Flask, render_template, request
import mysql.connector
import json
import os
import neo
import sql
app = Flask(__name__)

neo.delete_all()
#neo.create_user_nodes()
#neo.create_question_nodes()
#neo.create_user_question_relationship()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question_list', methods=["POST"])
def question_list():
    user_id = sql.db_getUserId(request.values.get('user'))
    return user_id


if __name__ == '__main__':
    app.run(host='0.0.0.0')
