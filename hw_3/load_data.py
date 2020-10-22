import os
import psycopg2
import csv
import time

start_time = time.time()

# creating dialect to proper csv reading
csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)

# DB parameters
os.environ['HOST'] = 'localhost'
os.environ['DB_NAME'] = 'postgres'
os.environ['DB_USER'] = 'postgres'
HOST = os.environ.get('HOST')
DB_NAME = os.environ.get('DB_NAME')
USER = os.environ.get('DB_USER')


# preparing sql query CREATE TABLE from csv file
def create_tab(csv_file='movie_metadata.csv'):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, dialect='mydialect')
        first_line = next(reader)

    # create_table = 'CREATE TABLE moviesdata (id SERIAL PRIMARY KEY,'
    create_table = 'CREATE TABLE moviesdata ('
    for id_c, column in enumerate(first_line):
        if id_c == len(first_line) - 1:
            # create_table += f'"{column}" int);'
            create_table += f'"{column}" int);'
        else:
            create_table += f'"{column}" text, '
    return create_table


# preparing sql query DROP COLUMN to delete not needed fields
def del_columns(csv_file='movie_metadata.csv'):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, dialect='mydialect')
        first_line = next(reader)
    query = 'ALTER TABLE moviesdata '
    for id_c, column in enumerate(first_line):
        if id_c == len(first_line) - 1:
            query += f'DROP COLUMN {column};'
        elif id_c in [11, 10, 9, 25]:
            continue
        else:
            query += f'DROP COLUMN {column}, '
    return query


def main():
    # connecting to db
    conn = psycopg2.connect(host=HOST, dbname=DB_NAME, user=USER)
    cur = conn.cursor()

    # executing queries to load data
    cur.execute(create_tab())
    query = '''
    COPY moviesdata FROM stdin WITH CSV HEADER
    DELIMITER as ','
    '''
    with open('movie_metadata.csv', 'r') as file:
        cur.copy_expert(sql=query, file=file)
    cur.execute(del_columns())
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
    print(f'time of performance: {time.time() - start_time} seconds')
