from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from json import loads, dumps


def consumer_from_postgres(consumer):
    partition = TopicPartition('de-psql-source-kafka_input', 0)
    consumer.assign([partition])
    last_offset = consumer.end_offsets([partition])[partition]

    list_data = []
    for msg in consumer:
        list_data.append(msg.value['payload'])
        if msg.offset == last_offset - 1:
            break
    return list_data


def main():
    consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             value_deserializer=lambda x: loads(
                                 x.decode('utf-8')))
    list_data = consumer_from_postgres(consumer)
    print(list_data)

    data_to_topic = []
    for record in list_data:
        if record['type'] in ['type1', 'type2']:
            data_to_topic.append(record)
    print(data_to_topic)

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: dumps(
                                 x).encode('utf-8'))
    for message in data_to_topic:
        producer.send('de-enriched-data', message)


if __name__ == '__main__':
    main()



