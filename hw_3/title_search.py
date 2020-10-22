import psycopg2
import argparse

# DB parameters
HOST = 'localhost'
DB_NAME = 'postgres'
USER = 'postgres'


# preparing sql query SELECT for finding state
def select_query(text, table='moviesdata'):
    query = f'''
    SELECT movie_title, actor_1_name, genres, imdb_score
    FROM {table}
    WHERE to_tsvector(movie_title) @@ plainto_tsquery('{text}')
    ORDER BY imdb_score DESC;
    ;'''
    return query


def main():
    # getting company argument
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help='company name')
    args = parser.parse_args()

    # connecting to db
    conn = psycopg2.connect(host=HOST, dbname=DB_NAME, user=USER)
    cur = conn.cursor()

    # executing query to get state and maximum number of issues
    cur.execute(select_query(args.text))
    records = cur.fetchall()
    for id_r, record in enumerate(records):
        display = f'Film {id_r}\n' \
                  f'title: {record[0]}\n' \
                  f'main_actor: {record[1]}\n' \
                  f'genres: {record[2]}\n' \
                  f'IMDn_score: {record[3]}\n'

        print(display)
    # displaying the result
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
