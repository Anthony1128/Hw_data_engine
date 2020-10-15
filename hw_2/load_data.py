import psycopg2
import csv
import time

start_time = time.time()

csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)

with open('P9-ConsumerComplaints.csv', 'r') as file:
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

conn = psycopg2.connect("host=localhost dbname=hw2_test user=anthony")
cur = conn.cursor()
cur.execute(create_table)

with open('P9-ConsumerComplaints.csv', 'r') as file:
    reader = csv.reader(file, dialect='mydialect')
    next(reader)
    for row in reader:
        insert = 'INSERT INTO consumercomplaints VALUES (DEFAULT, '
        for id_c, column in enumerate(row):
            if not column:
                column = 'None'
            if id_c == len(first_line) - 1:
                insert += '$$' + column + '$$' + ');'
            # elif id_c == 0:
            else:
                insert += '$$' + column + '$$, '
        cur.execute(insert)

conn.commit()
print(f'time of performance: {time.time() - start_time} seconds')
cur.close()
conn.close()
