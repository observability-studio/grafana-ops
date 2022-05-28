#!/usr/bin/env python
from copy import deepcopy
import json
from typing import Dict, List
import boto3


sm = boto3.session.Session().client(
    service_name='secretsmanager'
)


def script_handler(events, context):
    secret_type = events['secretType']
    env = events['env']

    res = sm.list_secrets(Filters=[
        {'Key': 'tag-key', 'Values': ['env']},
        {'Key': 'tag-value', 'Values': [env]},
        {'Key': 'tag-key', 'Values': ['secret-type']},
        {'Key': 'tag-value', 'Values': [secret_type]},
    ])

    secret_data = {}
    for secret in res['SecretList']:
        merge_dicts(secret_data, get_secret(secret['Name']), no_copy=True)

    return {'secret': secret_data}


def get_secret(secret_name: str) -> dict:
    team, datasource_name = secret_name.split('/')[-2:]
    res = sm.get_secret_value(
        SecretId=secret_name
    )
    secret = json.loads(res['SecretString'])
    return {team: {datasource_name: secret}}


def merge_dicts(*from_dicts: List[Dict], no_copy: bool = False) -> Dict:
    """ no recursion deep merge of 2 dicts

    By default creates fresh Dict and merges all to it.

    no_copy = True, will merge all dicts to a fist one in a list without copy.
    Why? Sometime I need to combine one dictionary from "layers".
    The "layers" are not in use and dropped immediately after merging.
    """

    if no_copy:
        def xerox(x): return x
    else:
        xerox = deepcopy

    result = xerox(from_dicts[0])

    for _from in from_dicts[1:]:
        merge_queue = [(result, _from)]
        for _to, _from in merge_queue:
            for k, v in _from.items():
                if k in _to and isinstance(_to[k], dict) and isinstance(v, dict):
                    # key collision add both are dicts.
                    # add to merging queue
                    merge_queue.append((_to[k], v))
                    continue
                _to[k] = xerox(v)

    return result
