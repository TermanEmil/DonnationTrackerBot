from dataclasses import asdict
from datetime import datetime

import pytz

import db_config
from Session import Session
from aws import get_db

_sessions_table = get_db().Table(db_config.sessions_table_name)


def get_sessions_table():
    return _sessions_table


def get_session(chat_id: int) -> Session:
    item = get_sessions_table().get_item(Key={'chat_id': chat_id})

    if 'Item' not in item:
        return Session(chat_id, form_step='RequestToStart')

    session = Session(**item['Item'])
    session.chat_id = int(session.chat_id)
    return session


def update_session(session: Session):
    table = get_sessions_table()
    session.last_updated = datetime.now(tz=pytz.UTC).isoformat()
    table.put_item(Item=asdict(session))


def create_table():
    get_db().create_table(
        TableName=db_config.sessions_table_name,
        KeySchema=[
            {
                "AttributeName": "chat_id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "chat_id",
                "AttributeType": "N"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    print(f"Table {db_config.sessions_table_name} created")
