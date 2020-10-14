import psycopg2
import csv

csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_ALL, doublequote=True)

with open('P9-ConsumerComplaints.csv', 'r') as file:
    reader = csv.reader(file, dialect='mydialect')
    # for row in reader:
    print(next(reader))
    print(list(reader)[0])
    # first_line = file.readline().strip().split(',')
    # second_line = file.readlines()[1].strip().split(',')
# id SERIAL PRIMARY KEY,
# create_table = 'CREATE TABLE ConsumerComplaints ('
# for id_c, column in enumerate(first_line):
#     if id_c == len(first_line) - 1:
#         create_table += '"' + column + '"' + ' text);'
#     else:
#         create_table += '"' + column + '"' + ' text, '
#
# insert = 'INSERT INTO consumercomplaints VALUES (DEFAULT, '
# for id_c, column in enumerate(second_line):
#     if not column:
#         column = 'None'
#     if id_c == len(first_line) - 1:
#         insert += '\'' + column + '\'' + ');'
#     else:
#         insert += '\'' + column + '\', '
#
# conn = psycopg2.connect("host=localhost dbname=hw2_test user=anthony")
# cur = conn.cursor()
# cur.execute(create_table)
# with open('P9-ConsumerComplaints.csv', 'r') as f:
#     next(f)
#     cur.copy_from(f, 'ConsumerComplaints', sep=',')
# # cur.execute(insert)
# conn.commit()


