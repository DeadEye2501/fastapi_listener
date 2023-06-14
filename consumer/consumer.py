import json
import os
from kafka import KafkaConsumer
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


bootstrap_servers = 'kafka:9092'
topic = 'json_topic'

db_host = os.environ.get('db_host')
db_port = int(os.environ.get('db_port'))
db_name = os.environ.get('db_name')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class DataTable(Base):
    __tablename__ = 'data_table'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)


Base.metadata.create_all(engine)


def message_reader():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers
    )

    while True:
        for message in consumer:
            data = message.value.decode('utf-8')
            data = json.loads(data)

            for k, v in data.items():
                record = DataTable(key=k, value=v)
                session.add(record)
                session.commit()


message_reader()
