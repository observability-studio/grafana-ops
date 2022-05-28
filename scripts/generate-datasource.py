#!/usr/bin/env python
import json
import os
from posixpath import basename
import sys
import yaml
from pathlib import Path


def generate_datasource(team_dir: str, provision_dir: str, secret: dict) -> None:
    datasources = []
    team = team_dir.split(os.sep)[-1]

    datasource_files = [f.path for f in os.scandir(team_dir) if f.is_file()]
    for file in datasource_files:
        datasource_key = basename(Path(file).with_suffix(''))
        datasource_secret = secret[datasource_key] if datasource_key in secret.keys() else {}

        raw_data = None
        with open(file) as stream:
            raw_data = stream.read()
        if raw_data:
            for key in datasource_secret.keys():
                raw_data = raw_data.replace(f'@{team}/{datasource_key}:{key}', datasource_secret[key])
            datasources.append(yaml.safe_load(raw_data))

    dest_file = os.sep.join([provision_dir, f'{team}.yaml'])
    with open(dest_file, 'w') as f:
        yaml.dump({'apiVersion': 1, 'datasources': datasources}, f)


if __name__ == '__main__':
    # ./datasources
    datasource_dir = sys.argv[1]
    # secret data as json string
    secret = json.loads(sys.argv[2])
    # /var/lib/grafana/provisioning/datasources
    gf_provision_dir = sys.argv[3]

    directories = [d.path for d in os.scandir(datasource_dir) if d.is_dir()]
    for dir in directories:
        team = dir.split(os.sep)[-1]
        team_secret = secret[team] if team in secret.keys() else {}
        generate_datasource(team_dir=dir, provision_dir=gf_provision_dir, secret=team_secret )
