import psycopg2
import csv
import time

start_time = time.time()

# creating dialect to proper csv reading
csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)

# DB parameters
HOST = 'localhost'
DB_NAME = 'hw2_test'
USER = 'anthony'


# preparing sql query CREATE TABLE from csv file
def create_tab(csv_file='P9-ConsumerComplaints.csv'):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, dialect='mydialect')
        first_line = next(reader)

    create_table = 'CREATE TABLE ConsumerComplaints (id SERIAL PRIMARY KEY,'
    for id_c, column in enumerate(first_line):
        if id_c == len(first_line) - 1:
            create_table += '"' + column + '"' + ' text);'
        elif id_c == 0:
            create_table += '"' + column + '"' + ' date, '
        else:
            create_table += '"' + column + '"' + ' text, '
    return create_table


# preparing sql query INSERT INTO table from csv file
def insert_query(csv_file='P9-ConsumerComplaints.csv', table='consumercomplaints'):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, dialect='mydialect')
        first_line = next(reader)
        for row in reader:
            insert = f'INSERT INTO {table} VALUES (DEFAULT, '
            for id_c, column in enumerate(row):
                if not column:
                    column = 'None'
                if id_c == len(first_line) - 1:
                    insert += '$$' + column + '$$' + ');'
                else:
                    insert += '$$' + column + '$$, '
            yield insert


def main():
    conn = psycopg2.connect(host=HOST, dbname=DB_NAME, user=USER)
    cur = conn.cursor()
    cur.execute(create_tab())
    for query in insert_query():
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
    print(f'time of performance: {time.time() - start_time} seconds')
