import psycopg2


start_date = '2013-07-29'
end_date = '2013-10-29'

query = '''
select "Product Name", 
    count(distinct "Complaint ID") as issues_amount, 
    count(case when "Timely Response" = 'Yes' then 1 end) as t_resp, 
    count(case when "Consumer Disputed" = 'Yes' then 1 end) as c_disp
from consumercomplaints
where "Date Received" between '{}'::date and '{}'::date
group by "Product Name"
order by issues_amount desc;'''.format(start_date, end_date)

conn = psycopg2.connect("host=localhost dbname=hw2_test user=anthony")
cur = conn.cursor()
cur.execute(query)
records = cur.fetchall()
for record in records:
    print(record)
cur.close()
conn.close()


