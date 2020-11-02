import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent

config_path = BASE_DIR / 'config' / 'api.yaml'

def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
        config['client_max_size'] = config['max_size_in_mb'] * 1024**2

    return config

config = get_config(config_path)
# print(config)

