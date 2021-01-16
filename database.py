import yaml
from sqlalchemy import create_engine
from urllib.parse import quote_plus

with open('config.yml', 'r') as ymlConf:
    configuration = yaml.safe_load(ymlConf)
    database = configuration['database']


def create_db():
    engine_db = setup_mysql_engine_no_db(database['username'],
                                         database['password'],
                                         database['host'],
                                         database['port'])
    existing_databases = engine_db.execute('SHOW DATABASES;')
    existing_databases = [d[0] for d in existing_databases]
    if database['database'] in existing_databases:
        engine_db.execute('DROP DATABASE {0}'.format(database['database']))
    engine_db.execute('CREATE DATABASE {0}'.format(database['database']))
    engine_db.dispose()


def create_tables(base):
    engine_db = setup_mysql_engine_default()
    base.metadata.create_all(engine_db)
    engine_db.dispose()


def setup_mysql_engine_no_db(user, password, host, port):
    conn_str_aurora_marketing = 'mysql+pymysql://{user}:{password}@{host}:{port}'
    return create_engine(conn_str_aurora_marketing.format(
        user=user,
        password=quote_plus(password),
        host=quote_plus(host),
        port=port
    ), encoding="utf-8", echo=False)


def setup_mysql_engine_default():
    user = database['username']
    password = database['password']
    host = database['host']
    port = database['port']
    database_name = database['database']

    conn_str_aurora_marketing = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    return create_engine(conn_str_aurora_marketing.format(
        user=user,
        password=quote_plus(password),
        host=quote_plus(host),
        port=port,
        database=database_name
    ), encoding="utf-8", echo=False)
