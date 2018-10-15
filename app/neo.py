# -*- coding: utf-8 -*-

from neo4j.v1 import GraphDatabase
import sql
import helper

from operator import itemgetter

'''
'
' Queries
'
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

def neo_create_question_user_rel(tx, question_id, user_id):
    tx.run("MATCH (u:User),(q:Question) WHERE u.id = $user_id AND q.id = $question_id CREATE (u)-[r:ANSWERED]->(q)",
    question_id=question_id, user_id=user_id)

def neo_get_question_ids_for_user_id(tx, user_id):
    res = tx.run("MATCH (a:User {id: $user_id})-[r]->(b:Question) Return b", user_id=int(user_id))
    return [record["b"]["id"] for record in res]

def neo_get_users_for_question_id(tx, question_id):
    res = tx.run("MATCH (a:User)-[r]->(b:Question {id: $question_id}) Return a", question_id=int(question_id))
    return [record["a"]["id"] for record in res]

'''
'
' Functions
'
'''
def delete_all():
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        session.write_transaction(neo_delete_all)

def create_user_nodes():
    users = sql.db_get_users()
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        for user in users:
            session.write_transaction(neo_create_user_nodes, user[0], user[1])

def create_question_nodes():
    questions = sql.db_get_questions()
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        for question in questions:
            session.write_transaction(neo_create_question_nodes, question[0], question[1])

def create_user_question_relationship():
    users = sql.db_get_users()
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    for user in users:
        print(user)
        user_edges = []
        for unique_quiz in sql.db_get_unique_quizes_for_user(user):
            for question in sql.db_questions_for_quiz(unique_quiz):
                user_edges.append(question)

        unique_user_edges = list(set(user_edges))
        for unique_edge in unique_user_edges:
            with driver.session() as session:
                session.write_transaction(neo_create_question_user_rel, unique_edge[0], user[0])

def get_most_similar_user(user_id):
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        my_question_ids = session.write_transaction(neo_get_question_ids_for_user_id, user_id)
        similar_users = []
        for question_id in my_question_ids:
            user_ids = session.write_transaction(neo_get_users_for_question_id, question_id)
            similar_users.extend(user_ids)
        mapped = []
        for user in similar_users:
            mapped.append((str(user), 1))
        reduced = helper.reduce(mapped)
        reduced.sort(key=itemgetter(1))
        return int(reduced[-2:-1][0][0])

def get_tutorial_question_ids(my_user_id, similar_user_id):
    #driver = GraphDatabase.driver("bolt://0.0.0.0:7687", auth=("neo4j", "test"))
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "root"))

    with driver.session() as session:
        my_question_ids = session.write_transaction(neo_get_question_ids_for_user_id, my_user_id)
        other_question_ids = session.write_transaction(neo_get_question_ids_for_user_id, similar_user_id)
        tutorial_question_ids = [x for x in other_question_ids if x not in my_question_ids]
        return tutorial_question_ids
