import configparser
from typing import List, Dict, Generator
import os

import snowflake.connector
from snowflake.connector import DictCursor


path_to_snowflake_config = os.path.expanduser('~/.snowsql/config')
config = configparser.ConfigParser()
config.read(path_to_snowflake_config)
ACCOUNT = config['connections.prod_etl']['accountname']
USER = config['connections.prod_etl']['username']
PASSWORD = config['connections.prod_etl']['password']


def get_sf_connection(database: str = 'RTR_QA', role: str = 'ANALYST_ROLE'):
    con = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        database=database,
        warehouse='ANALYST_WAREHOUSE',
        role=role,
    )
    return con


def get_dict_cursor_from_connection(con) -> DictCursor:
    return con.cursor(DictCursor)


def get_dict_cursor(database: str = 'RTR_QA', role: str = 'ANALYST_ROLE') -> DictCursor:
    con = get_sf_connection(database, role)
    return con.cursor(DictCursor)


def get_results_from_query(
    query: str, cursor: DictCursor
) -> Generator[List[Dict], None, None]:
    initial_results = cursor.execute(query)
    for result in initial_results:
        yield {k.lower(): v for k, v in result.items()}
