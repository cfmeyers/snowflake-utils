import configparser
from typing import List, Dict, Generator
import os

import snowflake.connector
from snowflake.connector import DictCursor


def get_sf_connection(connection_name: str):
    path_to_snowflake_config = os.path.expanduser('~/.snowsql/config')
    config = configparser.ConfigParser()
    config.read(path_to_snowflake_config)
    creds = config[connection_name]
    con = snowflake.connector.connect(
        user=creds['username'],
        password=creds['password'],
        account=creds['accountname'],
        database=creds['dbname'],
        warehouse=creds['warehousename'],
        role=creds['rolename'],
    )
    return con


def get_dict_cursor_from_connection(con) -> DictCursor:
    return con.cursor(DictCursor)


def get_dict_cursor(connection_name: str) -> DictCursor:
    con = get_sf_connection(connection_name, role)
    return con.cursor(DictCursor)


def get_results_from_query(
    query: str, cursor: DictCursor
) -> Generator[List[Dict], None, None]:
    initial_results = cursor.execute(query)
    for result in initial_results:
        yield {k.lower(): v for k, v in result.items()}
