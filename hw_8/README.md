Commands:

1. `docker-compose -f docker-compose.yml up -d`

2. `docker-compose -f docker-compose.yml logs -f`

3. `curl -XPOST localhost:8083/connectors -d @pg_source.json -H 'content-type:application/json'`

4. `curl -XPOST localhost:8083/connectors -d @es_sink.json -H 'content-type:application/json'`
   
5. `python3 main.py`