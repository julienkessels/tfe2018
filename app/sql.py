# -*- coding: utf-8 -*-

import mysql.connector
import config
mydb = mysql.connector.connect(**config.extern_config)
mycursor = mydb.cursor()

'''
'
' Helper Functions to create Neo4J DB
'
'''
def db_get_user_id(lastname):
    mycursor.execute("SELECT entity_id FROM field_data_field_user_lastname WHERE field_user_lastname_value = '%s'" % lastname)
    result = mycursor.fetchall()
    return str(result[0][0])

def db_get_users():
    mycursor.execute("SELECT entity_id, field_user_lastname_value FROM field_data_field_user_lastname")
    result = mycursor.fetchall()
    return result

def db_get_user_firstname(entity_id):
    mycursor.execute("SELECT field_user_firstname_value FROM field_data_field_user_firstname WHERE entity_id = '%s'" % entity_id)
    result = mycursor.fetchall()
    return str(result[0][0])

def db_get_user_lastname(entity_id):
    mycursor.execute("SELECT field_user_lastname_value FROM field_data_field_user_lastname WHERE entity_id = '%s'" % entity_id)
    result = mycursor.fetchall()
    return str(result[0][0])

def db_get_questions():
    mycursor.execute("SELECT entity_id, body_value FROM field_data_body")
    result = mycursor.fetchall()
    return result

def db_get_question_text(entity_id):
    mycursor.execute("SELECT body_value FROM field_data_body WHERE entity_id = '%s'" % str(entity_id))
    result = mycursor.fetchall()
    return result[0][0]

def db_get_unique_quizes_for_user(user):
    mycursor.execute("SELECT result_id FROM quiz_node_results WHERE uid = '%s'" % str(user[0]))
    result = mycursor.fetchall()
    unique_quiz = list(set(result))
    return unique_quiz

def db_questions_for_quiz(quiz):
    mycursor.execute("SELECT question_nid FROM quiz_node_results_answers WHERE result_id = '%s'" % str(quiz[0]))
    result = mycursor.fetchall()
    return result

def db_get_answers_for_question(question_id):
    mycursor.execute("SELECT answer, score_if_chosen FROM quiz_multichoice_answers WHERE question_nid = '%s'" % str(question_id))
    result = mycursor.fetchall()
    return result[:4]

def db_get_question_skill_difficulty(question_id):
    mycursor.execute("SELECT field_multichoice_skill_tid FROM field_data_field_multichoice_skill WHERE entity_id = '%s'" % str(question_id))
    skill_tid = mycursor.fetchall()[0][0]

    mycursor.execute("SELECT name FROM taxonomy_term_data WHERE tid = '%s'" % str(skill_tid))
    skill = mycursor.fetchall()[0][0]

    mycursor.execute("SELECT field_multichoice_difficulty_value FROM field_data_field_multichoice_difficulty WHERE entity_id = '%s'" % str(question_id))
    difficulty = mycursor.fetchall()[0][0]

    return skill + " - " + difficulty


'''
'
' Other Queries
'
'''
