import psycopg2
import argparse

# DB parameters
HOST = 'localhost'
DB_NAME = 'hw2_test'
USER = 'anthony'


# preparing sql query SELECT for finding state
def select_query(company, table='consumercomplaints'):
    query = f'''
    select "State Name", count("Complaint ID")
    from {table}
    where "Company" = '{company}'
    group by "State Name"
    having count("Complaint ID") = (
        select max(mycount) 
        from (select "State Name", count("Complaint ID") as mycount
            from {table}
            where "Company" = '{company}'
            group by "State Name") 
        as bar);'''
    return query


# preparing sql query SELECT for getting issues with with related attributes
def list_query(company, state, table='consumercomplaints'):
    query = f'''
    select "Issue", 
        "Sub Issue", 
        "Consumer Complaint Narrative", 
        "Company Response to Consumer"
    from {table}
    where "Company" = '{company}' and "State Name" = '{state}';'''
    return query


def main():
    # getting company argument
    parser = argparse.ArgumentParser()
    parser.add_argument('company', help='company name')
    args = parser.parse_args()

    # connecting to db
    conn = psycopg2.connect(host=HOST, dbname=DB_NAME, user=USER)
    cur = conn.cursor()

    # executing query to get state and maximum number of issues
    cur.execute(select_query(args.company))
    record = cur.fetchone()
    state = record[0]
    n_issues = record[1]

    # executing query to get issues with with related attributes
    cur.execute(list_query(args.company, state))
    records = cur.fetchall()
    list_issues = [i[0] for i in records]

    # displaying the result
    print(args.company, 'has', n_issues, 'issues:\n')
    print("Issue, Sub Issue, Consumer Complaint, Company Response")
    for id_i, issue in enumerate(list_issues):
        print(id_i, issue)
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()




