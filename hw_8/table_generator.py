import os
import psycopg2
import uuid
from faker import Faker
from random import randint


# DB parameters
HOST = 'localhost'
DB_NAME = 'postgres'
USER = 'postgres'

UUIDs = [uuid.uuid4() for i in range(10)]
TYPEs = ['type1', 'type2', 'type3', 'type4', 'type5']


# preparing sql query CREATE TABLE
def create_tab():
    create_table = f'CREATE TABLE kafka_input ("id" int PRIMARY KEY, ' \
                   f'"name" text, ' \
                   f'"customer_id" uuid, ' \
                   f'"type" text, ' \
                   f'"time" date);'
    return create_table


def random_data(n_lines):
    data = []
    fake = Faker()
    for i in range(n_lines):
        line_id = i
        line_name = fake.name().split(' ')[0]
        line_customer = UUIDs[randint(0, 9)]
        line_type = TYPEs[randint(0, 4)]
        line_time = fake.date_time_between(start_date='-30y', end_date='now')
        data.append([line_id, line_name, line_customer, line_type, line_time])
    return data


def main():
    # connecting to db
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password='postgres', host=HOST)
    cur = conn.cursor()

    # executing query to create table and load data in it
    cur.execute(create_tab())
    for l_id, l_name, l_customer, l_type, l_time in random_data(50):
        insert_query = 'INSERT INTO kafka_input ' \
                       f'VALUES ($${l_id}$$, $${l_name}$$, $${l_customer}$$, '\
                       f'$${l_type}$$, $${l_time}$$)'
        cur.execute(insert_query)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
