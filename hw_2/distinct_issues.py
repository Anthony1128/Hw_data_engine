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
    from {table} as c
    where "Company" = '{company}'
    group by "State Name"
    having count(distinct "Complaint ID") = (
    select max(mycount) 
    from (select "State Name", count(distinct "Complaint ID") as mycount
    from {table}
    where "Company" = '{company}'
    group by "State Name") as bar);'''
    return query


# preparing sql query SELECT for getting list of distinct issues
def list_query(company, state, table='consumercomplaints'):
    query = f'''
    select distinct "Issue" 
    from {table}
    where "Company" = '{company}' and "State Name" = '{state}';'''
    return query


# preparing an answer in convenient way
def prepare_answer(company, state, n_issues, list_issues):
    answer = {
        'company': company,
        'state': state,
        'amount_i': n_issues,
        'list_i': list_issues
    }
    return answer


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

    # executing query to get a list of distinct issues
    cur.execute(list_query(args.company, state))
    records = cur.fetchall()
    list_issues = [i[0] for i in records]

    # getting an answer in convenient way
    answer = prepare_answer(args.company, state, n_issues, list_issues)
    print(answer['company'], 'has', answer['amount_i'], 'issues:\n')
    for issue in answer['list_i']:
        print(issue)
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

