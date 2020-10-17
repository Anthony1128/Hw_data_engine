import psycopg2
import argparse

# start_date = '2013-07-29'
# end_date = '2013-10-29'

# DB parameters
HOST = 'localhost'
DB_NAME = 'postgres'
USER = 'postgres'


# preparing sql query SELECT
def select_query(start_date, end_date, table='consumercomplaints'):
    query = f'''
    select "Product Name", 
        count(distinct "Complaint ID") as issues_amount, 
        count(case when "Timely Response" = 'Yes' then 1 end) as t_resp, 
        count(case when "Consumer Disputed" = 'Yes' then 1 end) as c_disp
    from {table}
    where "Date Received" between '{start_date}'::date and '{end_date}'::date
    group by "Product Name"
    order by issues_amount desc;'''
    return query


def main():
    # getting date arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('start_date',
                        help='start date example input format: 2013-07-29')
    parser.add_argument('end_date',
                        help='end date example input format: 2013-10-29')
    args = parser.parse_args()

    # executing query
    conn = psycopg2.connect(host=HOST, dbname=DB_NAME, user=USER)
    cur = conn.cursor()
    cur.execute(select_query(args.start_date, args.end_date))

    # displaying the result
    records = cur.fetchall()
    print('Product Name, issues_amount, Timely Response, Consumer Disputed')
    for id_r, record in enumerate(records):
        print(id_r, record)
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
