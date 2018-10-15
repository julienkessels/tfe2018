from neo4j.v1 import GraphDatabase
import sql


'''
Neo4j Queries
'''
def neo_delete_all(tx):
    tx.run("MATCH (n)"
    "DETACH DELETE n")

def neo_create_user_nodes(tx, user_id, last_name):
    print("Adding user: ", user_id, last_name)
    tx.run("MERGE (a:User {id: $user_id, last_name: $last_name})",
    user_id=user_id, last_name=last_name)

def neo_create_question_nodes(tx, question_id, question_value):
    print("Adding question: ", question_id)
    tx.run("MERGE (a:Question {id: $question_id, value: $question_value})",
    question_id=question_id, question_value=question_value)

def neo_create_question_user_rel(tx, question_id, user_id):
    tx.run("MATCH (u:User),(q:Question) WHERE u.id = $user_id AND q.id = $question_id CREATE (u)-[r:ANSWERED]->(q)",
    question_id=question_id, user_id=user_id)


'''
Functions
'''
def delete_all():
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))
    
    with driver.session() as session:
        session.write_transaction(neo_delete_all)

def create_user_nodes():
    users = sql.db_getUsers()
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        for user in users:
            session.write_transaction(neo_create_user_nodes, user[0], user[1])

def create_question_nodes():
    questions = sql.db_getQuestions()
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        for question in questions:
            session.write_transaction(neo_create_question_nodes, question[0], question[1])

def create_user_question_relationship():
    users = sql.db_getUsers()
    for user in users:
        print(user)
        user_edges = []
        for unique_quiz in sql.db_getUniqueQuizesForUser(user):
            for question in sql.db_questionsForQuiz(unique_quiz):
                user_edges.append(question)

        unique_user_edges = list(set(user_edges))
        for unique_edge in unique_user_edges:
            with driver.session() as session:
                session.write_transaction(neo_create_question_user_rel, unique_edge[0], user[0])
