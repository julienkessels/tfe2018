import mysql.connector
import config
mydb = mysql.connector.connect(**config.extern_config)
mycursor = mydb.cursor()


def db_getUserId(lastname):
    mycursor.execute("SELECT entity_id FROM field_data_field_user_lastname WHERE field_user_lastname_value = '%s'" % lastname)
    result = mycursor.fetchall()
    return str(result[0][0])

def db_getUsers():
    mycursor.execute("SELECT entity_id, field_user_lastname_value FROM field_data_field_user_lastname")
    result = mycursor.fetchall()
    return result

def db_getQuestions():
    mycursor.execute("SELECT entity_id, body_value FROM field_data_body")
    result = mycursor.fetchall()
    return result

def db_getUniqueQuizesForUser(user):
    mycursor.execute("SELECT result_id FROM quiz_node_results WHERE uid = '%s'" % str(user[0]))
    result = mycursor.fetchall()
    unique_quiz = list(set(result))
    return unique_quiz

def db_questionsForQuiz(quiz):
    mycursor.execute("SELECT question_nid FROM quiz_node_results_answers WHERE result_id = '%s'" % str(quiz[0]))
    result = mycursor.fetchall()
    return result
