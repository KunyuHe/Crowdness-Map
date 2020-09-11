import os

import yaml


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def read_yaml(config_name, config_path):
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        raise KeyError(f"No config with name {config_name}.")
    raise FileNotFoundError(f"Config file not found at {config_path}.")
