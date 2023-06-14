import json
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from kafka import KafkaProducer
from sqlalchemy import create_engine, text

app = FastAPI()
producer = KafkaProducer(bootstrap_servers='kafka:9092')

db_host = os.environ.get('db_host')
db_port = int(os.environ.get('db_port'))
db_name = os.environ.get('db_name')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_password')

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)


@app.get("/set_data")
async def set_data(data: str):
    try:
        json_data = json.loads(data)
        producer.send('json_topic', value=json.dumps(json_data).encode())
        return {'json_data': json_data}
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON'}


@app.get("/get_data")
async def get_data():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT * FROM data_table'))

        data = {}
        for row in result:
            data[row[1]] = row[2]

    return {'data': data}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Fastapi Listener',
        version='1.0',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
