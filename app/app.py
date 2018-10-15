# -*- coding: utf-8 -*-

from __future__ import division
from flask import Flask, render_template, request
import mysql.connector
import json
import math
import os
import neo
import sql
from random import shuffle

app = Flask(__name__)

neo.delete_all()
neo.create_user_nodes()
neo.create_question_nodes()
neo.create_user_question_relationship()


tutorial_question_ids = []
my_fullname = ""
similar_user_fullname = ""
similar_user_fullname = ""
tutorial_count = 1

@app.route('/')
def index():
    global tutorial_count
    tutorial_count = 1
    return render_template('index.html')

@app.route('/question_list', methods=["POST"])
def question_list():
    user_id = sql.db_get_user_id(request.values.get('user'))
    return user_id

@app.route('/tutorial', methods=["POST"])
def tutorial():
    global my_fullname
    global similar_user_fullname
    global tutorial_question_ids
    global tutorial_count

    if request.values.get('next') != "next":
        my_user_id = sql.db_get_user_id(request.values.get('last_name'))

        # get my data
        my_lastname = sql.db_get_user_lastname(my_user_id)
        my_firstname = sql.db_get_user_firstname(my_user_id)
        my_fullname = my_firstname + " " + my_lastname

        # get other data
        similar_user_id = neo.get_most_similar_user(my_user_id)
        similar_user_lastname = sql.db_get_user_lastname(similar_user_id)
        similar_user_firstname = sql.db_get_user_firstname(similar_user_id)
        similar_user_fullname = similar_user_firstname + " " + similar_user_lastname

        # get list of questions
        tutorial_question_ids = neo.get_tutorial_question_ids(my_user_id, similar_user_id)
        shuffle(tutorial_question_ids)
        if (len(tutorial_question_ids) > 15):
            tutorial_question_ids = tutorial_question_ids[:15]
        else:
            print(len(tutorial_question_ids))

        # get next question
        question_id = tutorial_question_ids[tutorial_count]
        question_text = sql.db_get_question_text(question_id)
        question_answers_result = sql.db_get_answers_for_question(question_id)
        question_answers = list(zip(*question_answers_result)[0])
        question_answers_result = list(zip(*question_answers_result)[1])
        question_right_answer_index = str(question_answers_result.index(max(question_answers_result))+1)
        question_skill_difficulty = sql.db_get_question_skill_difficulty(question_id)
        percentage = str(math.ceil(tutorial_count/len(tutorial_question_ids)*100)) + "%"

        return render_template('tutorial.html', similar_user_fullname=similar_user_fullname, my_fullname=my_fullname, question_text=question_text, question_answers=question_answers, question_skill_difficulty=question_skill_difficulty, percentage=percentage, question_right_answer_index=question_right_answer_index, question_answers_length=len(question_answers))
    else:
        tutorial_count += 1
        if tutorial_count == len(tutorial_question_ids):
            return render_template('tutorial_finished.html', my_fullname=my_fullname)

        # get next question
        question_id = tutorial_question_ids[tutorial_count]
        question_text = sql.db_get_question_text(question_id)
        question_answers_result = sql.db_get_answers_for_question(question_id)
        question_answers = list(zip(*question_answers_result)[0])
        question_answers_result = list(zip(*question_answers_result)[1])
        question_right_answer_index = str(question_answers_result.index(max(question_answers_result))+1)
        question_skill_difficulty = sql.db_get_question_skill_difficulty(question_id)
        percentage = str(math.ceil(tutorial_count/len(tutorial_question_ids)*100)) + "%"
        return render_template('tutorial.html', similar_user_fullname=similar_user_fullname, my_fullname=my_fullname, question_text=question_text, question_answers=question_answers, question_skill_difficulty=question_skill_difficulty, percentage=percentage, question_right_answer_index=question_right_answer_index, question_answers_length=len(question_answers))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
